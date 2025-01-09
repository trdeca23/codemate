import os
from dotenv import load_dotenv
import google.generativeai as genai
from get_dir_structure import get_structure_in_target_dir
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

# Load environment variables from the .env file
load_dotenv()

# Gemini interaction
genai.configure(api_key=os.environ['API_KEY'])
enable_automatic_function_calling = False  # Warning: Do not use `enable_automatic_function_calling=True` in production applications as there are no data input verification checks for automatic function calls.
model = genai.GenerativeModel(model_name='gemini-1.5-pro',  # "gemini-1.5-pro", "gemini-1.5-flash"
                              tools=TOOLS)

chat = model.start_chat(enable_automatic_function_calling=enable_automatic_function_calling)

# # Example calls:
# message = "Help me build a toy app that can be used as a 'calculator' that 'adds' and 'subtracts' colors together. \
#     Use the read_all_files function to see exactly where the project is up to now, and then FOLLOWING THAT intention, use the write_file function to create new files or overwrite existing ones as needed, and use the read_file function to confirm that your files are being written correctly."
# message = "Can you write a simple web browser implementation (e.g., that uses uvicorn and whatever else is needed) and a requirements.txt file as well as a README."
# message = "First, try and test each of the API functions you have available to make sure they work. For example, let me know how many files are in the target directory you have access to. \
#     Then use the available functions (e.g., write_file) to create a toy app that can be used as a 'calculator' that 'adds' and 'subtracts' colors together, including a small front-end UI that can run in the browser. \
#     You can pretend that you will have access to any environment you need, and in fact you should write a requirements.txt file that includes the libraries you will need, including uvicorn and \
#     whatever else would be needed to create some basic web browser UI. You should also write a README.py and a simple main.py script."
# message = """Can you test each of the API functions you have available to make sure each works. Start by looking at the \
#     target directory structure, then read the README, and then read all the files ..do not test the write_file function yet though."""  # TODO: Later the message should be injected by the user
# message = "You are helping me build a library that leverage Gemini to facilitate paired programming between an AI and a human (i.e., human-in-the-loop AI programming). Please use the functions at your dissposal to read the README and see the directory structure. After that, use read_file to take a close look at write_file.py and how it imports the TARGET_DIR so that the write_file function within it is limited to accessing only files within the TARGET_DIR. Once you understand how it's done there, please use the read_file and write_file functions to update file_system_opearations.py so that it imports TARGET_DIR and so as so limit the relative_path to be within the TARGET_DIR"
# message = 'Read the readme to understand the point of the library in the target directory, as well as all the files. You should then test the code to make sure it functions as intended and make suggestions for improvements'
# message = "Read the readme, test all the functions, and let me know how you would improve the main.py file"

# TODO: Everything from here down should exist within a while == True loop so that the user can keep asking questions and getting help

message = input("Enter a question for AI\n")
# TODO: Append the message to a .txt or .csv file so that we can track these in the TARGET_DIR
response = chat.send_message(message)

if not enable_automatic_function_calling:
    # Print out each of the function calls requested from this single call.
    response_parts = []
    for part in response.parts:
        if fn := part.function_call:
            args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
            print()
            print("Function requested by AI:")
            print(f"{fn.name}({args})")
            if fn.name not in TOOLNAMES_SUBSET_HUMAN_NOT_REQUIRED:
                user_input = input("Do you want to allow this code to execute? (yes/no): ")
                if user_input.lower() != "yes":
                    val = "Access denied. User blocked function from running"
                    response_parts.append(genai.protos.Part(function_response=genai.protos.FunctionResponse(name=fn.name, response={"result": val})))
                    print("Function not called")
                    continue
            val = locals()[fn.name](**fn.args)
            response_parts.append(genai.protos.Part(function_response=genai.protos.FunctionResponse(name=fn.name, response={"result": val})))
            print("Function called")
            # responses['read_file'] = read_file_in_target_dir(relative_path=fn.args['relative_path'])

    response = chat.send_message(response_parts)

print(response.text)
print()
print("NOTE: Remember to routinely look over any changes that have been made and commit or discard them.")
print()
