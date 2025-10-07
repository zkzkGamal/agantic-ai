from functions.patch_file_line import patch_file_lines
from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from config import WORKING_DIRECTORY
from google.genai import types


def call_function(function_call_part, verbose=False, return_part=False):
    function_name = function_call_part.name
    function_arguments = function_call_part.args

    if verbose:
        print(f"\ncalling function {function_name} with arguments {function_arguments}\n")
    else:
        print(f"\n  calling function {function_name}\n")

    try:
        if function_name == "get_files_info":
            result = get_files_info(WORKING_DIRECTORY, **function_arguments)
        elif function_name == "get_file_content":
            result = get_file_content(WORKING_DIRECTORY, **function_arguments)
        elif function_name == "write_file":
            result = write_file(WORKING_DIRECTORY, **function_arguments)
        elif function_name == "run_python_file":
            result = run_python_file(WORKING_DIRECTORY, **function_arguments)
        elif function_name == "patch_file_lines":
            result = patch_file_lines(WORKING_DIRECTORY, **function_arguments)
        else:
            result = {"error": f"Unknown function: {function_name}"}

        part = types.Part(
            function_response=types.FunctionResponse(
                name=function_name,
                response={"result": result},
            )
        )

        if return_part:
            return part
        else:
            return types.Content(role="function", parts=[part])

    except Exception as e:
        part = types.Part(
            function_response=types.FunctionResponse(
                name=function_name,
                response={"error": f"Exception while calling {function_name}: {str(e)}"},
            )
        )
        return part if return_part else types.Content(role="function", parts=[part])

