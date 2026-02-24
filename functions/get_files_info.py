import os

def get_files_info(working_directory, directory="."):
    """
    Returns a string representation of the contents of the target directory,
    ensuring the directory is within the permitted working_directory.
    """
    try:
        # Get absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # Construct the full path to the target directory safely
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # Security check: Ensure target_dir is inside working_dir_abs
        try:
            common = os.path.commonpath([working_dir_abs, target_dir])
            if common != working_dir_abs:
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        except ValueError:
            # Handles cases where commonpath fails (e.g. different drives on Windows)
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the path is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # List contents
        items = os.listdir(target_dir)
        output_lines = []
        
        for item in items:
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            try:
                file_size = os.path.getsize(item_path)
            except OSError:
                file_size = 0 # Fallback for special files or inaccessible ones
            
            output_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: {str(e)}"

# OpenAI Tool Definition
tools_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
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