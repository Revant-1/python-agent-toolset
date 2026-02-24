import os

def write_file(working_directory, file_path, content):
    """
    Writes content to a file within the permitted working_directory.
    Creates any missing parent directories and overcomes security boundaries.
    """
    try:
        # Get absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # Construct the full path to the target file safely
        full_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Security check: Ensure full_path is inside working_dir_abs
        try:
            common = os.path.commonpath([working_dir_abs, full_path])
            if common != working_dir_abs:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        except ValueError:
             return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Check if the path is an existing directory
        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure parent directories exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write/Overwrite the file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"

# OpenAI Tool Definition
tools_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file within the permitted working_directory, creating parent directories if needed",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path where the file should be written, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
