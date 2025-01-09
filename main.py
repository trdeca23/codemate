import os
from dotenv import load_dotenv
import google.generativeai as genai
from get_dir_structure import get_structure_in_target_dir
import json
from read_all_files import read_all_files_in_target_dir
from read_file import read_file_in_target_dir
from write_file import write_file_in_target_dir
from file_system_operations import (make_directory_in_target_dir,
                                    delete_file_in_target_dir,
                                    move_file_in_target_dir,
                                    copy_file_in_target_dir,
                                    local_code_execution)

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

MODELS_BY_PREFERENCE = ["gemini-1.5-pro", "gemini-1.0-pro", "gemini-1.5-flash"]

def log_message(message, filepath="interaction_log.txt"):
    try:
        with open(filepath, "a") as f:
            f.write(message + "\n")
        return True
    except Exception as e:
        print(f"Error logging message: {e}")
        return False

model_index = 0
ai_reminders = ''
n_calls = 0

if os.path.exists("ai_reminders.txt"):
    with open("ai_reminders.txt", "r") as f:
        ai_reminders = f.read()

# Load environment variables from the .env file
load_dotenv()
# Gemini interaction
genai.configure(api_key=os.environ['API_KEY'])
enable_automatic_function_calling = False  # Warning: Do not use `enable_automatic_function_calling=True` in production applications as there are no data input verification checks for automatic function calls.

model = genai.GenerativeModel(model_name=MODELS_BY_PREFERENCE[model_index],
                              tools=TOOLS)  # TODO: increment model_index and re-instantiate model anytime error is raised in send_message call due to daily token limit: google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted (e.g. check quota).

chat = model.start_chat(enable_automatic_function_calling=enable_automatic_function_calling)

while True:
    message = input("Enter a question for AI (or type 'exit' to quit):\n")
    if message.lower() == "exit":
        break
    # TODO: implement an `elif message.lower() == "help":` that allows user to then type actions that bypass AI, including: 1. 'refresh' action which causes chat to be re-initialized in case token count is getting too high (i.e., by calling `chat = model.start_chat(...); continue`)

    log_message(f"User: {message}")
    if n_calls == 0:
        message = message + ai_reminders

    response = chat.send_message(message)
    n_calls += 1

    if not enable_automatic_function_calling:
        finished = False
        while not finished:
            response_parts_fn = []
            for part in response.parts:
                if fn := part.function_call:
                    args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
                    print(f"\nFunction requested by AI: \033[94m{fn.name}\033[0m({args})")

                    if fn.name not in TOOLNAMES_SUBSET_HUMAN_NOT_REQUIRED:
                        user_input = input("Do you want to allow this code to execute? (yes/no): ")
                        if user_input.lower() != "yes":
                            result = "Access denied. User blocked function from running."
                            print("\033[91mFunction not called.\033[0m")
                            log_message(f"AI: Function {fn.name} not called (user denied). ")
                            response_parts_fn.append(genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(name=fn.name, response={"result": result})
                            ))
                            continue

                    try:
                        result = locals()[fn.name](**fn.args)
                        print(f"\033[92mFunction '{fn.name}' called successfully.\033[0m")
                        log_message(f"AI: Called function {fn.name}")

                    except Exception as e:
                        result = f"Error executing function '{fn.name}': {e}"
                        print(f"\033[91m{result}\033[0m")
                        log_message(f"AI: Error calling function {fn.name}: {e}")

                    response_parts_fn.append(genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(name=fn.name, response={"result": result})
                    ))

                if tx := part.text:
                    print(f"\033[93m{tx}\033[0m")
                    log_message(f"AI: {tx[:100]}..")
                    print("\n\033[95mNOTE: Remember to routinely look over any changes and commit or discard them.\033[0m\n")

            if response_parts_fn:
                print("\033[96mReturning information from function call/s to AI\033[0m")
                response = chat.send_message(response_parts_fn)
                # TODO: Troubleshoot below error. Could it have to do with the escape characters now added to this file for the color-coding?
                # Traceback (most recent call last):
                # File "<string>", line 1, in <module>
                # File "c:\Users\decandia_te\AppData\Local\miniconda3\envs\wcp\lib\site-packages\google\generativeai\generative_models.py", line 588, in send_message
                #     self._check_response(response=response, stream=stream)
                # File "c:\Users\decandia_te\AppData\Local\miniconda3\envs\wcp\lib\site-packages\google\generativeai\generative_models.py", line 616, in _check_response
                #     raise generation_types.StopCandidateException(response.candidates[0])
                # google.generativeai.types.generation_types.StopCandidateException: finish_reason: MALFORMED_FUNCTION_CALL
                n_calls += 1
                if (len(response.parts) == 1) & (response.parts[0].function_call.name == ''):
                    finished = True
            else:
                finished = True

    print(f"\033[93m{response.text}\033[0m")
    log_message(f"AI: {response.text[:100]}..")
    print("\n\033[95mNOTE: Remember to routinely look over any changes and commit or discard them.\033[0m\n")
