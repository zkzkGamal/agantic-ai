import os, subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f"error : {file_path} is not a subdirectory of {working_directory}"

    if not os.path.isfile(abs_file_path):
        return f"error : {file_path} not found"

    # if not os.access(abs_file_path, os.X_OK):
    # return f"error : {file_path} is not executable"

    if not abs_file_path.endswith(".py"):
        return f"error : {file_path} is not a python file"

    try:
        out = subprocess.run(
            ["python3", abs_file_path] + args,
            check=True,
            timeout=30,
            capture_output=True,
        )
        final_string = f"""
            STDOUT : {out.stdout.decode()}
            STDERR : {out.stderr.decode()}
            RETURN CODE : {out.returncode}
        """
        if out.returncode != 0:
            final_string = f"Proccess exit with code {out.returncode}"
        return final_string

    except Exception as e:
        return f"error executin file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file as python3 interpreter. Accepts all CLI args as an optional array",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of arguments to pass to the python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)
