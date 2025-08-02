import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    functions = {"get_file_content": get_file_content,
                 "get_files_info": get_files_info,
                 "run_python_file": run_python_file,
                 "write_file": write_file,
    }   
    if function_call_part.name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )        
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    func = functions[function_call_part.name]
    result = func(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )   


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. 


All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

If a user asks you to run, read, or write a file, ALWAYS use your available tools and NEVER reply with a direct answer or ask for clarification, even if the filename seems ambiguous.
Assume 'tests.py' refers to the file './calculator/tests.py', and use the tool to attempt running it if asked.

"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file
        
    ]
)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
args = sys.argv[1:]

if not args:
    print("you entered nothing")
    sys.exit(1)

messages = [types.Content(role="user", parts=[types.Part(text=" ".join(sys.argv[1:]))])]
response = client.models.generate_content(
    model ='gemini-2.0-flash-001',
    contents = messages,
    config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt), 
)

verbose = False
if "--verbose" in sys.argv:
    verbose = True
    print(f"User prompt: {' '.join(sys.argv[1:])}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if not response.function_calls and response.text:
    print(response.text)

if response.function_calls is not None:
    for function in response.function_calls:
        result = call_function(function, verbose=verbose)
        if verbose:
            try:
                print(f"-> {result.parts[0].function_response.response}")
            except Exception as e:
                print(f"Error extracting function response: {e}")
      
    
    





