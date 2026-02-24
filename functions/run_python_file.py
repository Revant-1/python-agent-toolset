import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    """
    Executes a Python file within the permitted working_directory.
    Includes security checks, timeout, and output capture.
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
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        except ValueError:
             return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the path exists and is a regular file
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check if it's a Python file
        if not file_path.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build the command
        command = ["python", full_path]
        if args:
            command.extend(args)

        # Run the process
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Build output string
        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"

# OpenAI Tool Definition
tools_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the permitted working_directory with a 30s timeout and output capture",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python script to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the script",
                },
            },
            "required": ["file_path"],
        },
    },
}
