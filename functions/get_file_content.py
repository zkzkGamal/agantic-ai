import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f"error : {file_path} is not a subdirectory of {working_directory}"

    try:
        with open(abs_file_path, 'r') as file:
            content = file.read(MAX_CHARS)
            if len(content) >= MAX_CHARS:
                content += {
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                }
            return content
    except FileNotFoundError:
        return f"error : {file_path} not found"
    except Exception as e:
        return f"error : {e}"
    
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="GEt the content of the file as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory",
            ),
        },
    ),
)