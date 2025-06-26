from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Safely reads and returns the content of a file (up to a fixed limit) within a permitted working directory, returning error messages for invalid paths or file access issues.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The `file_path` parameter specifies the relative path (from the working_directory) to the file whose content should be read, and must reside within the permitted working directory.",
            ),
        },
    ),
)

schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
    description = "Lists files in a specified subdirectory (or working directory by default), returning their sizes and directory status, while enforcing access restrictions and handling errors.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "directory": types.Schema(
                type = types.Type.STRING,
                description = "The `directory` parameter specifies a subdirectory (relative to the working_directory) whose contents should be listed; if omitted, the contents of the working_directory itself are listed.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes the given `content` to a file located at `file_path` within the `working_directory`, creating any necessary parent directories and enforcing access restrictions.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The `file_path` parameter specifies the relative path (from working_directory) to the target file to be written; must remain within the permitted working directory.",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "The `content` parameter specifies the string data to be written to the specified file.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Executes a Python file located at `file_path` within the working_directory, ensuring it is a valid .py file and enforcing directory access restrictions, while capturing and returning the script's STDOUT output or STDERR errors.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The `file_path` specifies the relative path (from working_directory) to the Python file to be executed; must point to a .py file within the permitted working directory.",
            ),
            "cli_args": types.Schema(
                type = types.Type.STRING,
                description = "The `args` specifies any optional argument the Python file may require to be executed.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations = [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)