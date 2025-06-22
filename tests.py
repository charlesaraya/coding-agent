# tests.py

import unittest

from functions.run_python import run_python_file

class TestGetFilesInfo(unittest.TestCase):
    def test_run_file_success(self):
        working_dir = "calculator"
        file_paths = ["main.py", "tests.py"]
        expected_outputs = ["STDOUT: Calculator App", "Ran 9 tests"]
        for path, expected in zip(file_paths, expected_outputs):
            got_output = run_python_file(working_dir, path)
            self.assertTrue(expected in got_output)

    def test_file_out_of_wd(self):
        working_dir = "calculator"
        file_path = "/tmp/temp.txt"
        expected_err = "outside the permitted working directory"
        got_err = run_python_file(working_dir, file_path)
        self.assertTrue(expected_err in got_err)

    def test_file_dont_exist(self):
        working_dir = "calculator"
        file_path = "nonexistent.py"
        expected_err = "not found."
        got_err = run_python_file(working_dir, file_path)
        self.assertTrue(expected_err in got_err)

if __name__ == "__main__":
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))
    unittest.main()