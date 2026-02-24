import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    """
    Reads the content of a file within the permitted working_directory,
    truncating it if it exceeds MAX_CHARS.
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
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        except ValueError:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the path is a regular file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file with truncation
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            
            # Check if there's more content
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                
        return content

    except Exception as e:
        return f"Error: {str(e)}"

# OpenAI Tool Definition
tools_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a file within the permitted working_directory, truncating it if it exceeds MAX_CHARS",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
