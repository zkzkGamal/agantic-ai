from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from config import WORKING_DIRECTORY
from google.genai import types


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_arguments = function_call_part.args
    if verbose:
        print(
            f"""
              calling function {function_name} with arguments {function_arguments}
            """
        )
    else:
        print(
            f"""
              calling function {function_name}
            """
        )

    try:
        function_response = ""
        if function_name == "get_files_info":
            function_response = get_files_info(WORKING_DIRECTORY, **function_arguments)
        elif function_name == "get_file_content":
            function_response = get_file_content(WORKING_DIRECTORY, **function_arguments)
        elif function_name == "write_file":
            function_response = write_file(WORKING_DIRECTORY, **function_arguments)
        elif function_name == "run_python_file":
            function_response = run_python_file(WORKING_DIRECTORY, **function_arguments)
        
        if function_response != "":
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result":function_response},
                    )
                ],
            )
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name} and \n {e}"},
                )
            ],
        )
