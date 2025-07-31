import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    absoluteworkdir = os.path.abspath(working_directory)
    absolutefullpath = os.path.abspath(full_path)
    if not absolutefullpath.startswith(absoluteworkdir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    files = os.listdir(full_path)
    strings = []
    for file in files:
        try:
            newpath = os.path.join(full_path,file)
            size = os.path.getsize(newpath)
            isdir = os.path.isdir(newpath)
            string = (f"- {file}: file_size={size} bytes, is_dir={isdir}")
            strings.append(string)
        except Exception as e:
            return(f"Error: {e}")
    return "\n".join(strings)
    
