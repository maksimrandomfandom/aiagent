import os

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
    

    