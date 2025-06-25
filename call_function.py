from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    if not function_call_part:
        raise AttributeError('please provide the `function_call_part` argument')
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    for func_name, fn in available_functions.items():
        if func_name == function_call_part.name:
            result = fn("./calculator", **function_call_part.args)
            return types.Content(
                role = "tool",
                parts = [
                    types.Part.from_function_response(
                        name = function_call_part.name,
                        response = {
                            "result": result,
                        },
                    ),
                ],
            )
    return types.Content(
        role = "tool",
        parts = [
            types.Part.from_function_response(
                name = function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
            )
        ],
    )

available_functions = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

if __name__ == '__main__':
    class Function_call_part:
        def __init__(self, name, args):
            self.name = name
            self.args = args
    f = Function_call_part("run_python_file", {"file_path":"main.py"})
    print(call_function(f, verbose=False))

