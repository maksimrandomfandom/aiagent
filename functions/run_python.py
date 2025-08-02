import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory,file_path)
    absolutefullpath = os.path.abspath(full_path)
    absoluteworkdir = os.path.abspath(working_directory)
    if not absolutefullpath.startswith(absoluteworkdir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolutefullpath):
        return f'Error: File "{file_path}" not found.'
    if not absolutefullpath.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python",absolutefullpath]
        if args:
            commands.extend(args)
        result = subprocess.run(commands,capture_output=True,text=True,timeout=30,cwd=absoluteworkdir)
        
        output = []
        stdout = (f"STDOUT: {result.stdout}")
        stderr = (f"STDERR: {result.stderr}")
        if result.stdout:
            output.append(stdout)
        if result.stderr:
            output.append(stderr)
        
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
            return f"Error: executing python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the specified python file restricted to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file to run, relative to the working directory",
            ),
        },
    ),
)

    