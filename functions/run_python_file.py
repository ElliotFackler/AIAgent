import os
import subprocess
import sys

schema_run_python_file = {
        "type": "function",
        "function": {
            "name": "run_python_file",
            "description": "Execute a python file and return its output",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "file path to location of specified file, relative to the working directory (default is the working directory itself)",
                },
                    "args": {
                        "type": "array",
                        "description": "A list of arguments to be used in the function",
                        "items": {"type": "string"},
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str: # Locate a python file and run it

    # Check that the file exists and is located within the permitted working directory
        try:
            directory_path = os.path.abspath(working_directory)
            full_file_path = os.path.normpath(os.path.join(directory_path, file_path))
    
            if os.path.commonpath([directory_path, full_file_path]) != directory_path:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            if not os.path.isfile(full_file_path):
                return f'Error: "{file_path}" does not exist or is not a regular file'
            if not full_file_path.endswith('.py'):
                 return f'Error: "{file_path}" is not a Python file'
        except Exception as e:
            return f"Error: {e}" 

        command = [sys.executable, full_file_path]

        if args != None:
             command.extend(args)

        completedProcess = subprocess.run(command, cwd=os.path.dirname(full_file_path), capture_output=True, text = True, timeout=30)

        # Check if the file has returned a value or not
        output = ""
        if completedProcess.returncode != 0:
            output = f"Process exited with code {completedProcess.returncode}. "

        if completedProcess.stdout is None and completedProcess.stderr is None:
            output += "No output produced"
        else:
            output += f"STDOUT: {completedProcess.stdout}"
            output += f"STDERR: {completedProcess.stderr}"

        return output