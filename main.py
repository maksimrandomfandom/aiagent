import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import call_function, available_functions

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

for candidate in response.candidates:
    messages.append(candidate.content)

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
      
    
    





