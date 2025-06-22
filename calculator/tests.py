# tests.py

import unittest
from unittest.mock import patch
import io

from pkg.calculator import Calculator
# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

def find_num_dirs_files(lines):
    num_dirs = 0
    num_files = 0
    for line in lines:
        isDir = line.find('is_dir=True')
        if isDir >= 0:
            num_dirs += 1
        else:
            num_files += 1
    return num_dirs, num_files

class TestGetFilesInfo(unittest.TestCase):
    def test_current_dir(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            get_files_info("calculator", ".")
            lines = fake_out.getvalue().split('\n')[:-1]
            num_dirs, num_files = find_num_dirs_files(lines)
            self.assertEqual(5, len(lines))
            self.assertEqual(3, num_dirs)
            self.assertEqual(2, num_files)

    def test_child_dir(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            get_files_info("calculator", "pkg")
            self.assertIn("render.py: file_size=768 bytes, is_dir=False", fake_out.getvalue())
            self.assertIn("__pycache__: file_size=128 bytes, is_dir=True", fake_out.getvalue())
            self.assertIn("calculator.py: file_size=1739 bytes, is_dir=False", fake_out.getvalue())

    def test_non_found(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            get_files_info("calculator", "/bin")
            self.assertIn("Error:", fake_out.getvalue())
            self.assertIn("was not found", fake_out.getvalue())

    def test_file(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            get_files_info("calculator", "main.py")
            self.assertIn("Error:", fake_out.getvalue())
            self.assertIn("is not a directory", fake_out.getvalue())

    def test_going_down(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            get_files_info("calculator", "../")
            self.assertIn("Error:", fake_out.getvalue())
            self.assertIn("outside", fake_out.getvalue())

if __name__ == "__main__":
    unittest.main()