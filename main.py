import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY missing from .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# Use stepfun/step-3.5-flash:free as it's a reliable free model that supports reasoning
MODEL = "stepfun/step-3.5-flash:free"

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Chatbot with tool calling support")
    parser.add_argument("user_prompt", type=str, help="User prompt to send to the AI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    try:
        if args.verbose:
            print(f"--- Calling Model: {MODEL} ---")
        
        # Start conversation history
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt}
        ]

        # API call with tools provided
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=available_functions,
            temperature=0,
            extra_body={"reasoning": {"enabled": True}}
        )

        message = response.choices[0].message
        
        # Check for tool calls
        if hasattr(message, 'tool_calls') and message.tool_calls:
            function_results = []
            for tool_call in message.tool_calls:
                # Use the call_function dispatcher
                function_call_result = call_function(tool_call, verbose=args.verbose)
                
                # Validation logic as requested by the assignment
                if not function_call_result.parts:
                    raise Exception("Function call result has no parts")
                
                part = function_call_result.parts[0]
                if not hasattr(part, 'function_response') or part.function_response is None:
                    raise Exception("Function call result part has no function_response")
                
                if not hasattr(part.function_response, 'response') or part.function_response.response is None:
                    raise Exception("FunctionResponse has no response field")

                # Collect result part
                function_results.append(part)

                # Verbose printing of the result
                if args.verbose:
                    print(f"-> {part.function_response.response}")
        else:
            # If no tool calls, print the text response
            print(message.content)

        if args.verbose and response.usage:
            print(f"\nPrompt tokens: {response.usage.prompt_tokens}")
            print(f"Completion tokens: {response.usage.completion_tokens}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
