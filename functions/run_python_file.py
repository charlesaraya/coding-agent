import os
from subprocess import run

def run_python_file(working_directory, file_path, cli_args=""):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: File "{file_path}" is not a python file.'
    try:
        if isinstance(cli_args, str):
            cli_args.strip('"').strip("'")
        completed_process = run(args=["python3", abs_file_path, cli_args], capture_output=True, timeout=30, text=True)
        if completed_process.returncode != 0:
            return f'Process exited with code {completed_process.returncode}'
        if not completed_process:
            return "No output produced."
        return f'STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}'
    except Exception as e:
        print(f"Error: executing Python file: {e}")


if __name__ == '__main__':
    print(run_python_file("calculator", "nonexistent.py"))
