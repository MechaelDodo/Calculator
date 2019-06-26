import unittest
import sys
sys.path.append(r'C:\Users\admin\AppData\Local\Programs\Python\Python37-32\mypyt\calculator_module\myCalculator_forGit\Calculator\math_modules')
from mathcheck import *
from mathexception import *
from mathconvert import *


class Test_mathconvert(unittest.TestCase):

    def test_convert_digit(self):
        convert = Convert(['3', '3', '+', '1', '1'])
        convert.convert_digit()
        self.assertEqual(convert.list_expression, ['33', '+', '11'])
        
    def test_convert_float(self):
        convert = Convert(['3', '.', '3', '+', '1', '.', '1'])
        convert.convert_float()
        self.assertEqual(convert.list_expression, ['3.3', '+', '1.1'])

    def test_convert_const(self):
        convert = Convert(['e'])
        convert.convert_const()
        self.assertEqual(convert.list_expression, ['2.718281828459045'])

    def test_normalization(self):
        value = ['2.0']
        value = Convert.normalization(value)
        self.assertEqual(value, 2)

if __name__ == '__main__':
    unittest.main()

