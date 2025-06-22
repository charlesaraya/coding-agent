import os

MAX_READ_STREAM = 10_000

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(abs_file_path):
        return f'Error: {abs_file_path} does not exist'
    if not os.path.isfile(abs_file_path):
        return f'Error: {abs_file_path} is not a file'
    try:
        with open(abs_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_READ_STREAM)
            if len(content) == MAX_READ_STREAM:
                content += f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error: {e}'


if __name__ == '__main__':
    out = get_file_content('calculator', '/bin/cat')
    print(out)