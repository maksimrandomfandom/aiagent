import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory,file_path)
    absolutefullpath = os.path.abspath(full_path)
    absoluteworkdir = os.path.abspath(working_directory)
    if not absolutefullpath.startswith(absoluteworkdir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolutefullpath):
        try:
            os.makedirs(os.path.dirname(absolutefullpath),exist_ok=True)
        except Exception as e:
            return(f"Error: {e}")
    with open(absolutefullpath, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="overwrites the specified file with the response, restricted to the working directory ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file to write on, relative to the working directory",
            
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description= "the content to write to the file",
            )
        },
    ),
)
    

    