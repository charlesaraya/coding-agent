# tests.py

import unittest
from unittest.mock import patch
import io

from functions.write_file_content import write_file

class TestGetFilesInfo(unittest.TestCase):
    def test_write_file_success(self):
        working_dir = "calculator"
        file_paths = ["lorem.txt", "pkg/morelorem.txt"]
        contents = ["wait, this isn't lorem ipsum", "lorem ipsum dolor sit amet"]
        for path, content in zip(file_paths, contents):
            out = write_file(working_dir, path, content)
            self.assertTrue(out.startswith('Successfully'))

    def test_not_allowed(self):
        working_dir = "calculator"
        file_path = "/tmp/temp.txt"
        content = "this should not be allowed"
        out = write_file(working_dir, file_path, content)
        self.assertTrue(out.startswith('Error:'))

if __name__ == "__main__":
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    unittest.main()