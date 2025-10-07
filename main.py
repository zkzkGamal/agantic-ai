from dotenv import load_dotenv
from google import genai
from google.genai import types
import os, argparse
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.patch_file_line import schema_patch_file_lines
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
        You are an autonomous AI code repair agent.

        Your goal is to fix runtime or syntax errors in the project efficiently.

        ### Rules:
        1. **Read and Analyze Efficiently**
        - Use `get_files_info` to find files.
        - Use `get_file_content` ONLY for files likely related to the issue.
        - Keep context minimal to reduce token usage.

        2. **Fixing Logic**
        - If the problem is small (logic or minor error): use `patch_file_lines`.
        - If the file has major syntax or structural issues: rewrite the entire file once using `write_file`.

        3. **Verification**
        - After patching or rewriting, use `run_python_file` to test.
        - If successful → stop.
        - If not → analyze the new error and patch again.

        4. **Efficiency**
        - Avoid re-reading files unnecessarily.
        - Avoid explaining steps in detail — focus on function calls.
        - Minimize total token use per turn.

        5. **Response Rules**
        - Each function call must receive exactly one corresponding function response part.
        - Do not include text output with function calls.

        ### Objective:
        When fixing syntax or logic errors, instead of deleting the buggy line, comment it out and write the corrected version right below it.
        When patching, if the line was already commented or fixed earlier, skip reapplying the same fix.\
        Diagnose and fix the given project so that it runs successfully.
        """


    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_get_file_content,
            schema_run_python_file,
            schema_patch_file_lines,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=[system_prompt]
    )
    max_iter = 20
    for _ in range(max_iter):
        try:
            response = client.models.generate_content(
                # model="gemma-3-27b-it",
                model="gemini-2.5-flash",
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
                # Collect all responses for this turn
                function_responses = []
                for function_call in response.function_calls:
                    function_responses.append(call_function(function_call, verbose, return_part=True))
                
                # Combine all into a single message
                messages.append(
                    types.Content(
                        role="function",
                        parts=function_responses
                    )
                )
            else:
                print(response.text)
                return

        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    main()
