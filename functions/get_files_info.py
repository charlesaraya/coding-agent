import os

def get_files_info(working_directory, directory=None):
    # ensure we stay in the current dir
    if directory.startswith('../'):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return
    if directory == '.':
        _scandir(working_directory)
        return
    # walk until the spot the directory
    for (root, dirs, files) in os.walk(working_directory):
        # its a file, throw error
        if directory in files:
            print(f'Error: "{directory}" is not a directory')
            return
        # its a dir, scan and print file info
        if directory in dirs:
            _scandir(root+"/"+directory)
            return
    print(f'Error: "{directory}" was not found')

def _scandir(path):
    with os.scandir(path) as dirs:
        for dir in dirs:
            print(f"{dir.name}: file_size={dir.stat().st_size} bytes, is_dir={dir.is_dir()}")

def find_num_dirs_files(lines):
    num_dirs = 0
    num_files = 0
    for line in lines:
        isDir = line.find('is_dir=True')
        if isDir:
            num_dirs += 1
        else:
            num_files += 1
    return num_dirs, num_files

if __name__ == "__main__":
    get_files_info("calculator", ".")