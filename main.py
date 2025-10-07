from dotenv import load_dotenv
from google import genai
from google.genai import types
import os, argparse
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from call_functions import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(
        description="handle encryption and decryption for user sign."
    )
    parser.add_argument("--verbose", required=0, action="store_true")
    parser.add_argument("--prompt", required=1, help="the type of data")
    args = parser.parse_args()
    prompt, verbose = args.prompt, args.verbose
    system_prompt = """
You are a self-healing AI coding agent with full access to the working directory.

Your goals:
1. Automatically explore the project files and directories as needed.
2. Understand the purpose of the project by reading `README`, `main.py`, or similar files.
3. Locate the main logic and any functions related to the user's question or error.
4. When an error or wrong output occurs, inspect relevant files and fix the issue.
5. Always verify fixes by re-running code or tests before confirming success.

You can:
    - List files/directories recursively
    - Read file contents
    - Write or modify files
    - Run Python files with optional args
    - Inspect outputs and retry fixes if needed

Never ask the user for missing files — find them yourself in the project tree.
"""

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_get_file_content,
            schema_run_python_file,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=[system_prompt]
    )
    max_iter = 20
    for i in range(max_iter):
        try:
            response = client.models.generate_content(
                # model="gemma-3-27b-it",
                model="gemini-2.0-flash-001",
                contents=messages,
                config=config,
            )

            if response is None or response.usage_metadata is None:
                print("No response")
                return
            if verbose:
                print(
                    f"prompt tokens = {response.usage_metadata.prompt_token_count}, "
                    f"completion tokens = {response.usage_metadata.candidates_token_count}, "
                    f"total tokens = {response.usage_metadata.total_token_count}"
                )
            if response.candidates is not None:
                for candidants in response.candidates:
                    if candidants.content is None:
                        continue
                    messages.append(candidants.content)

            if response.function_calls:
                for function_call in response.function_calls:
                    messages.append(call_function(function_call, verbose))
            else:
                print(response.text)
                return
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
