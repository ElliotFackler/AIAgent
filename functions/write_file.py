import os

#TODO write new write_file schema

def write_file(working_directory: str, file_path: str, content: str) -> str:

    # Check that the file exists and is located within the permitted working directory
        try:
            directory_path = os.path.abspath(working_directory)
            full_file_path = os.path.normpath(os.path.join(directory_path, file_path))
    
            if os.path.commonpath([directory_path, full_file_path]) != directory_path:
                return f"Error: Cannot write to {full_file_path} as it is outside the permitted working directory"
            if os.path.isdir(full_file_path):
                return f'Error: Cannot write to "{full_file_path}" as it is a directory'
        except Exception as e:
            return f"Error: {e}" 

        # Make sure that all the parent directories exist
        os.makedirs(os.path.dirname(full_file_path), exist_ok = True)

        # Write to the chosen file
        with open(full_file_path, "w") as file:
             file.write(content)

        return f'Successfully wrote to "{full_file_path}" ({len(content)} characters written)'