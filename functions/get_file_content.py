import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory,file_path)
    absolutefullpath = os.path.abspath(full_path)
    absoluteworkdir = os.path.abspath(working_directory)
    if not absolutefullpath.startswith(absoluteworkdir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, "r") as f:
            filecontentstring = f.read(MAX_CHARS)
            nextchar = f.read(1)
        if nextchar:
            filecontentstring = filecontentstring + f'[...File "{file_path}" truncated at 10000 characters]'
        return filecontentstring
    except Exception as e:
        return(f"Error: {e}")
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="gets the content of the specificed file restricted to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file to read, relative to the working directory",
            ),
        },
    ),
)




        

