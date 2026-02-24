import os
import argparse
import json
import sys
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
    parser = argparse.ArgumentParser(description="Agentic Chatbot with iterative tool loop")
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

        # Iterative agent loop
        for i in range(20):
            if args.verbose:
                print(f"\n--- Iteration {i+1} ---")
            
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=available_functions,
                temperature=0,
                extra_body={"reasoning": {"enabled": True}}
            )

            assistant_msg = response.choices[0].message
            messages.append(assistant_msg)
            
            # Check for tool calls
            if hasattr(assistant_msg, 'tool_calls') and assistant_msg.tool_calls:
                for tool_call in assistant_msg.tool_calls:
                    # Execute the tool
                    function_call_result = call_function(tool_call, verbose=args.verbose)
                    
                    # Validation
                    if not function_call_result.parts:
                        raise Exception("Function call result has no parts")
                    part = function_call_result.parts[0]
                    
                    # Append result to history for the model to see in next iteration
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": json.dumps(part.function_response.response)
                    })

                    if args.verbose:
                        print(f"-> {part.function_response.response}")
            else:
                # No more tools requested, this is the final final response
                if args.verbose:
                    print("\nFinal response:")
                print(assistant_msg.content)
                return

        # If we reach here, we hit the iteration limit
        print("\nError: Maximum iteration limit (20) reached without a final response.")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
