import unittest
import sys
sys.path.append(r'C:\Users\admin\AppData\Local\Programs\Python\Python37-32\mypyt\calculator_module\myCalculator_forGit\Calculator\math_modules')
from mathconvert import *
from mathtransform import *
from mathsigns import *
from mathexpression import *


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


class Test_mathtransform(unittest.TestCase):

    def test_sign_transformation(self):
        transformer = Transformer(['2', '<', '=', '3'])
        transformer.sign_transformation()
        self.assertEqual(transformer.list_expression, ['2', '<=', '3'])

    def test_sub_transformation(self):
        transformer = Transformer(['-', '5', '+', '1'])
        transformer.sub_transformation()
        self.assertEqual(transformer.list_expression, ['-5', '+', '1'])

    def test_space_transformation(self):
        transformer = Transformer(['5', ' ', '+', '1'])
        transformer.space_transformation()
        self.assertEqual(transformer.list_expression, ['5', '+', '1'])

    def test_math_transformation(self):
        transformer = Transformer(['a', 'b', 's', '(', '2', '-', '10', ')'])
        transformer.math_transformation()
        result = ['abs', '(', '2', '-', '10', ')']
        self.assertEqual(transformer.list_expression, result)


class Test_mathexpression(unittest.TestCase):

    def test_expression_evaluation(self):
        proccessor = Proccessor(['3', '+', '1'])
        proccessor.expression_evaluation(DICT_ADD_SUB)
        self.assertEqual(proccessor.list_expression, ['4.0'])

    def test_expression_evaluation_math(self):
        proccessor = Proccessor(['abs', '-5'])
        proccessor.expression_evaluation_math(DICT_ABS)
        self.assertEqual(proccessor.list_expression, ['5.0'])

    def test_expression_evaluation_computemath(self):
        data = ['abs', '(', '-2', ')', '+', 'abs', '(', '-3', ')']
        proccessor = Proccessor(data)
        proccessor.expression_evaluation_computemath()
        self.assertEqual(proccessor.list_expression, ['2.0', '+', '3.0'])

    def test_bracketspriority(self):
        proccessor = Proccessor(['3', '-', '(', '2', '+', '10', ')', '-', '1'])
        proccessor.bracketspriority()
        result = ['3', '-', '12.0', '-', '1']
        self.assertEqual(proccessor.list_expression, result)

    def test_comparison(self):
        proccessor = Proccessor(['2', '+', '3', '>=', '4'])
        proccessor.comparison()
        self.assertEqual(proccessor.list_expression, True)


if __name__ == '__main__':
    unittest.main()
