import os
from google.genai import types
from config import WORKING_DIRECTORY


def patch_file_lines(working_directory, file_path, patch_lines):
    """
    Safely patch specific lines in a file without overwriting unrelated content.
    Adds smart handling:
    - Avoids duplicate patches.
    - Auto-comments out invalid syntax lines before replacing.
    - Allows 'replace', 'insert_before', and 'insert_after' modes.
    """
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f"❌ error: {file_path} is outside working directory"

    if not os.path.isfile(abs_file_path):
        return f"❌ error: file '{file_path}' not found"

    try:
        with open(abs_file_path, "r") as f:
            lines = f.readlines()

        patched_count = 0
        seen_lines = set()

        # Apply patches in reverse order to keep line numbers stable
        for patch in sorted(patch_lines, key=lambda x: x["line_number"], reverse=True):
            line_no = patch.get("line_number", None)
            new_code = patch.get("new_code", "")
            mode = patch.get("mode", "replace")

            if not isinstance(line_no, int) or line_no < 1:
                continue

            # Avoid duplicate patch on the same line
            if line_no in seen_lines:
                print(f"⚠️ Skipping duplicate patch near line {line_no} in {file_path}")
                continue
            seen_lines.add(line_no)

            # Auto-comment old broken code before replacing
            if mode == "replace":
                if 1 <= line_no <= len(lines):
                    old_line = lines[line_no - 1]
                    if _is_broken_line(old_line):
                        lines[line_no - 1] = "# [auto-commented invalid line] " + old_line
                        lines.insert(line_no, new_code + "\n")
                    else:
                        lines[line_no - 1] = new_code + "\n"
                elif line_no == len(lines) + 1:
                    lines.append(new_code + "\n")

            elif mode == "insert_before" and 1 <= line_no <= len(lines):
                lines.insert(line_no - 1, new_code + "\n")

            elif mode == "insert_after" and 1 <= line_no <= len(lines):
                lines.insert(line_no, new_code + "\n")

            patched_count += 1

        with open(abs_file_path, "w") as f:
            f.writelines(lines)

        return f"✅ Patched {patched_count} line(s) in '{file_path}' successfully."

    except Exception as e:
        return f"❌ error while patching {file_path}: {e}"


def _is_broken_line(line: str) -> bool:
    """
    Heuristic to detect obviously invalid Python syntax lines.
    These will be auto-commented instead of left active.
    """
    broken_patterns = [
        "pp", "<<", ">>>", "??", "!!", "undefined", ";;", "??", "return return", "if if"
    ]
    return any(p in line for p in broken_patterns)


# ---------------------------
# Schema definition
# ---------------------------
schema_patch_file_lines = types.FunctionDeclaration(
    name="patch_file_lines",
    description=(
        "Patch specific lines in a file without overwriting unrelated content. "
        "Supports 'replace', 'insert_before', and 'insert_after' modes. "
        "Automatically comments invalid lines before fixing."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, description="Relative path to the target file."
            ),
            "patch_lines": types.Schema(
                type=types.Type.ARRAY,
                description="Array of line patches.",
                items=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "line_number": types.Schema(
                            type=types.Type.INTEGER,
                            description="The line number (1-based) where the patch applies.",
                        ),
                        "new_code": types.Schema(
                            type=types.Type.STRING,
                            description="The new code or line content to insert or replace.",
                        ),
                        "mode": types.Schema(
                            type=types.Type.STRING,
                            description='Optional. One of "replace", "insert_before", or "insert_after". Default is "replace".',
                        ),
                    },
                    required=["line_number", "new_code"],
                ),
            ),
        },
        required=["file_path", "patch_lines"],
    ),
)
