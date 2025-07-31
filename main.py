import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
args = sys.argv[1:]

if not args:
    print("you entered nothing")
    sys.exit(1)

messages = [types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),]
response = client.models.generate_content(model ='gemini-2.0-flash-001',contents = messages )

if "--verbose" in sys.argv:
    print(f"User prompt: {sys.argv[1]}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    print(response.text)




