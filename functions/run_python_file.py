import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:

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

        command = ['python', full_file_path]

        if args != None:
             command.extend(args)

        completedProcess = subprocess.run(command, cwd=os.path.dirname(full_file_path), capture_output=True, text = True, timeout=30)

        str1 = ''
        if completedProcess.returncode != 0:
             str1 = "Process exited with code X"

        if completedProcess.stdout == None and completedProcess.stderr == None:
             str1 += " No output produced"
        else:
             str1 += f" STDOUT: {completedProcess.stdout}"
             str1 += f" STDERR: {completedProcess.stdout}"

        return str1