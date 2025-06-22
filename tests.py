# tests.py

import unittest
from unittest.mock import patch
import io

from functions.get_file_content import get_file_content

class TestGetFilesInfo(unittest.TestCase):
    def test_file_over_max_size(self):
        file_path = "lorem.txt"
        out = get_file_content("calculator", file_path)
        suffix = f'[...File "{file_path}" truncated at 10000 characters]'
        self.assertTrue(out.endswith(suffix))

    def test_file_under_max_size(self):
        file_paths = ["main.py", "pkg/calculator.py"]
        for path in file_paths:
            out = get_file_content("calculator", path)
            suffix = f'[...File "{path}" truncated at 10000 characters]'
            self.assertFalse(out.endswith(suffix))

    def test_no_exist_file(self):
        file_path = "/bin/cat"
        out = get_file_content("calculator", file_path)
        self.assertTrue(out.startswith('Error:'))

if __name__ == "__main__":
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    unittest.main()