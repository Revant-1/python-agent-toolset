import json
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Mapping function names to implementation
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

# OpenAI Tool Definitions
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

available_functions = [
    tools_get_files_info,
    tools_get_file_content,
    tools_write_file,
    tools_run_python_file,
]

# Classes to mimic the return structure requested by the assignment
class FunctionResponse:
    def __init__(self, name, response):
        self.name = name
        self.response = response

class Part:
    def __init__(self, function_response):
        self.function_response = function_response

    @classmethod
    def from_function_response(cls, name, response):
        return cls(FunctionResponse(name, response))

class Content:
    def __init__(self, role, parts):
        self.role = role
        self.parts = parts

def call_function(tool_call, verbose=False):
    """
    Dispatcher to execute the requested tool and return a structured response.
    Injects working_directory="./calculator" for all calls.
    """
    function_name = tool_call.function.name or ""
    
    # Parse arguments
    try:
        raw_args = json.loads(tool_call.function.arguments)
        args = dict(raw_args) if raw_args else {}
    except (json.JSONDecodeError, TypeError):
        args = {}

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Inject working directory
    args["working_directory"] = "./calculator"

    # Execute function
    if function_name in function_map:
        try:
            result = function_map[function_name](**args)
            response_data = {"result": result}
        except Exception as e:
            response_data = {"error": str(e)}
    else:
        response_data = {"error": f"Unknown function: {function_name}"}

    # Return mimicking the requested Content structure
    return Content(
        role="tool",
        parts=[Part.from_function_response(function_name, response_data)]
    )
