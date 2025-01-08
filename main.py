import os
from dotenv import load_dotenv
import google.generativeai as genai
from get_dir_structure import get_dir_structure
from read_all_files import read_all_files
from read_file import read_file
from write_file import write_file

# Load environment variables from the .env file
load_dotenv()

# Gemini interaction
genai.configure(api_key=os.environ['API_KEY'])
tools = [# 'code_execution',  # The only string that can be passed as a tool is 'code_execution'
         get_dir_structure,
         read_all_files,
         read_file,
         write_file,
        ]
model = genai.GenerativeModel(model_name='gemini-1.5-pro',  # "gemini-1.5-flash"
                              tools=tools)

chat = model.start_chat(enable_automatic_function_calling=True)  # Warning: Do not use `enable_automatic_function_calling=True` in production applications as there are no data input verification checks for automatic function calls.

message = """Ok, I've written out the files as you specified, which you can look at if you'd like. \
    Can you test each of the functions you have available to make sure it works, and if it doesn't \
    then you can hopefully read the file and suggest what needs to be fixed"""  # TODO: Later the message should be injected by the user
response = chat.send_message(message)

print(response.text)

for tool_call in response.tool_calls:
    print(tool_call)
    tool_code = tool_call.function.name
    tool_args = tool_call.arguments
    print(locals()[tool_code](**tool_args)) # Execute the tool call
