import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:

    # Check that the file exists and is located within the permitted working directory
    try:
        directory_path = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(directory_path, file_path))

        if os.path.commonpath([directory_path, full_file_path]) != directory_path:
            return f"Error: Cannot read {full_file_path} as it is outside the permitted working directory"
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{full_file_path}"'
    except Exception as e:
        return f"Error: {e}" 

    
    # Read through the file up to MAX_CHARs characters (Currently set at 10,000) and return as a string
    with open(full_file_path, "r") as file:
        file_contents = file.read(MAX_CHARS)

        if file.read(1):
            file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    return file_contents
