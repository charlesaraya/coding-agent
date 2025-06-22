import os

MAX_READ_STREAM = 10_000

def get_file_content(working_directory, file_path):
    wd_path = os.path.abspath(working_directory)
    path = os.path.join(wd_path, file_path)

    # ensure we stay in the current dir
    if not path.startswith(wd_path) or file_path.startswith("../"):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(path) or not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(path, "r", encoding="utf-8") as f:
            read_data = f.read(MAX_READ_STREAM)
            if len(read_data) == MAX_READ_STREAM:
                read_data += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f'Error: {e}'

    return read_data

if __name__ == '__main__':
    read_data = get_file_content('calculator', '/bin/cat')
    print(read_data)