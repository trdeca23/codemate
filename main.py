import os
from dotenv import load_dotenv
import google.generativeai as genai
from get_dir_structure import get_dir_structure
from read_all_files import read_all_files
from read_file import read_file
from write_file import write_file

# Load environment variables from the .env file
load_dotenv()

os.chdir('../file_lib')  # TODO: Later the target directory should be injected by the user

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

chat = model.start_chat()  # Warning: Do not use `enable_automatic_function_calling=True` in production applications as there are no data input verification checks for automatic function calls.

message = """Ok, I've written out the files as you specified and added a main.py file too, \
    which you can look at if you'd like. Anything else needed? I know that you have tool_execution \
    as a tool, but you can't use that when the library isn't included in your environment, so maybe \
    it would be good to add another function which would be local_code_execution? Any other functions \
    you can think of that would be good to add?"""  # TODO: Later the message should be injected by the user
response = chat.send_message(message)

print(response.text)

for tool_call in response.tool_calls:
    print(tool_call)
    tool_code = tool_call.function.name
    tool_args = tool_call.arguments
    print(locals()[tool_code](**tool_args)) # Execute the tool call
