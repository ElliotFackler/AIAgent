import os

schema_get_files_info = {
        "type": "function",
        "function": {
            "name": "get_files_info",
            "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status. This does not read the file's content or run/execute a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = "."): # Get, label, and return the contents of a direectory
    try: 
        # Compare the permitted directory against the directory the AI agent would like to access
        path = os.path.abspath(working_directory)
        conjoinedPath = os.path.normpath(os.path.join(path, directory))

        if os.path.commonpath([path, conjoinedPath]) != path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(conjoinedPath):
            return f'Error: "{directory}" is not a directory'

    except Exception as e:
        return f"Error: {e}"

    item_info = []
    contents = os.listdir(conjoinedPath)


    # Iterate through the directory's contents and append their info to the list.
    for item in contents:
        path_to_item = os.path.join(conjoinedPath, item)
        isDir = False
        size = os.path.getsize(path_to_item)

        # Check if the item is a directory or not
        if os.path.isdir(path_to_item):
            isDir = True

        item_info.append(f"  - {item}: file_size={size} bytes, is_dir={isDir}")

    return item_info


    