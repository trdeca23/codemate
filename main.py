import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from google.generativeai.types.generation_types import StopCandidateException
from utils import (
    get_structure_in_target_dir,
    read_all_files_in_target_dir,
    read_file_in_target_dir,
    write_file_in_target_dir,
    make_directory_in_target_dir,
    delete_file_in_target_dir,
    move_file_in_target_dir,
    copy_file_in_target_dir,
    local_code_execution
    )
import json
from rich import print
from rich.console import Console
from rich.style import Style
console = Console()

TOOLS = [# 'code_execution',  # The only string that can be passed as a tool is 'code_execution'
         get_structure_in_target_dir,
         read_all_files_in_target_dir,
         read_file_in_target_dir,
         write_file_in_target_dir,
         make_directory_in_target_dir,
         delete_file_in_target_dir,
         move_file_in_target_dir,
         copy_file_in_target_dir,
         local_code_execution,
        ]

TOOLNAMES_SUBSET_HUMAN_NOT_REQUIRED = [
    "get_structure_in_target_dir",
    "read_all_files_in_target_dir",
    "read_file_in_target_dir",
    ]

MODELS_BY_PREFERENCE = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"]

ENABLE_AUTOMATIC_FUNCTION_CALLING = False  # Warning: Do not use `enable_automatic_function_calling=True` in production applications as there are no data input verification checks for automatic function calls.

model_index = 1
ai_reminders = ''
n_calls = 0

def log_message(message, filepath="interaction_log.txt"):
    try:
        with open(filepath, "a") as f:
            f.write(message + "\n")
        return True
    except Exception as e:
        console.print(f"Error logging message: {e}", style="red")
        return False

def catch_quota_error(send_message):
    def wrapper(message):
        global model_index, model, chat # Declare global variables since we may need to modify them
        max_retries = len(MODELS_BY_PREFERENCE)
        retries = 0
        while retries < max_retries:
            try:
                return send_message(message)
            except ResourceExhausted as e:
                # increment model_index and re-instantiate model if token limit 429 Resource has been exhausted
                model_index = (model_index + 1) % len(MODELS_BY_PREFERENCE)
                console.print(f"ResourceExhausted error caught: {e}, switching models to {MODELS_BY_PREFERENCE[model_index]}", style="yellow")
                model = genai.GenerativeModel(model_name=MODELS_BY_PREFERENCE[model_index], tools=TOOLS)
                history = chat.history
                chat = model.start_chat(enable_automatic_function_calling=ENABLE_AUTOMATIC_FUNCTION_CALLING, history=history)
                retries += 1
        raise RuntimeError("Quota limit reached for all models. Please check your quota, wait, and try again.")
    return wrapper

@catch_quota_error
def send_message(message):
    return chat.send_message(message)

if os.path.exists("ai_reminders.txt"):
    with open("ai_reminders.txt", "r") as f:
        ai_reminders = f.read()

# Load environment variables from the .env file
load_dotenv()
# Gemini interaction
genai.configure(api_key=os.environ['API_KEY'])

model = genai.GenerativeModel(model_name=MODELS_BY_PREFERENCE[model_index],
                              tools=TOOLS)

chat = model.start_chat(enable_automatic_function_calling=ENABLE_AUTOMATIC_FUNCTION_CALLING)

while True:
    message = input("Enter a question for AI (or type 'exit' to quit):\n")
    if message.lower() == "exit":
        break
    # TODO: implement an `elif message.lower() == "help":` that allows user to then type actions that bypass AI, including: 1. 'refresh' action which causes chat to be re-initialized in case token count is getting too high (i.e., by calling `chat = model.start_chat(...); continue`)

    log_message(f"User: {message}")
    if n_calls == 0:
        message = message + ai_reminders

    malformed_error_retries = 0
    max_malformed_error_retries = 3
    while malformed_error_retries < max_malformed_error_retries:
        try:
            response = send_message(message)
            break  # Exit loop on success
        except StopCandidateException as e:
            malformed_error_retries += 1
            error_message = f"StopCandidateException error caught (attempt {malformed_error_retries}/{max_malformed_error_retries}): {e}"
            console.print(error_message, style="yellow")
            log_message(f"ERROR: {error_message}")

    if malformed_error_retries == max_malformed_error_retries:
        console.print(
            "The AI returned a 'malformed function' error multiple times.  "
            "Please rephrase your question or try a different approach.",
            style="red"
        )
        log_message("ERROR:  Max retries exceeded for 'malformed function' error. User needs to rephrase.")
        continue  # Skip to the next iteration of the main loop

    if not ENABLE_AUTOMATIC_FUNCTION_CALLING:
        finished = False
        while not finished:
            response_parts_fn = []
            for part in response.parts:
                if fn := part.function_call:
                    args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
                    console.print(f"\nFunction requested by AI: [blue]{fn.name}[/blue]({args})", style="bold blue")

                    if fn.name not in TOOLNAMES_SUBSET_HUMAN_NOT_REQUIRED:
                        user_input = input("Do you want to allow this code to execute? (yes/no): ")
                        if user_input.lower() != "yes":
                            result = f"Access denied. User blocked function from running. User answer when asked whether they allow function to execute: {user_input}"
                            console.print("Function not called.", style="yellow")
                            log_message(f"AI: Function {fn.name} not called (user denied). ")
                            response_parts_fn.append(genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(name=fn.name, response={"result": result})
                            ))
                            continue

                    try:
                        result = locals()[fn.name](**fn.args)
                        console.print(f"Function '{fn.name}' called successfully.", style="green")
                        log_message(f"AI: Called function {fn.name}")

                    except Exception as e:
                        result = f"Error executing function '{fn.name}': {e}"
                        console.print(f"{result}", style="red")
                        log_message(f"AI: Error calling function {fn.name}: {e}")

                    response_parts_fn.append(genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(name=fn.name, response={"result": result})
                    ))

                if tx := part.text:
                    if len(response.parts) > 1:
                        console.print(f"{tx}", style="blue")
                        log_message(f"AI: {tx[:100]}..")
                        console.print("\nNOTE: Remember to routinely look over any changes and commit or discard them.\n", style="yellow")

            if response_parts_fn:
                console.print("Returning information from function call/s to AI", style="yellow")

                # TODO: Debug - find cause for below error that is often raised: protos.Candidate.FinishReason.MALFORMED_FUNCTION_CALL
                #   File "..\lib\site-packages\google\generativeai\generative_models.py", line 588, in send_message
                #     self._check_response(response=response, stream=stream)
                #   File "..\lib\site-packages\google\generativeai\generative_models.py", line 616, in _check_response
                #     raise generation_types.StopCandidateException(response.candidates[0])
                # NOTE: It is returned by the client but we should isolate the types of requests that are problematic, e.g. so far read_all_files_in_target_dir may be the most problematic

                malformed_error_retries = 0
                max_malformed_error_retries = 3
                while malformed_error_retries < max_malformed_error_retries:  # this while loop is temporary until I find cause for error
                    try:
                        response = send_message(response_parts_fn)
                        n_calls += 1
                        break  # Exit loop on success
                    except StopCandidateException as e:
                        malformed_error_retries += 1
                        error_message = f"StopCandidateException error caught (attempt {malformed_error_retries}/{max_malformed_error_retries}): {e}"
                        console.print(error_message, style="yellow")
                        log_message(f"ERROR: {error_message}")

                if (len(response.parts) == 1) & (response.parts[0].function_call.name == ''):
                    finished = True
            else:
                finished = True

    console.print(f"{response.text}", style="blue")
    log_message(f"AI: {response.text[:100]}..")
    console.print("\nNOTE: Remember to routinely look over any changes and commit or discard them.\n", style="yellow")
