
import unittest
import warnings
from src.rpn_calc import RpnCalculator


class TestRpnCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = RpnCalculator()

    def test_basic_operations(self):
        self.assertEqual(self.calc.evaluate_expression("2 3 +"), 5)
        self.assertEqual(self.calc.evaluate_expression("5 3 -"), 2)
        self.assertEqual(self.calc.evaluate_expression("4 3 *"), 12)
        self.assertEqual(self.calc.evaluate_expression("10 2 /"), 5.0)
        self.assertEqual(self.calc.evaluate_expression("7 3 //"), 2)
        self.assertEqual(self.calc.evaluate_expression("7 3 %"), 1)
        self.assertEqual(self.calc.evaluate_expression("2 3 **"), 8)

    def test_complex_expressions(self):
        self.assertEqual(self.calc.evaluate_expression("5 1 2 + 4 * + 3 -"), 14)
        self.assertEqual(self.calc.evaluate_expression("3 4 2 * 1 5 - / +"), 1)

    def test_unary_operations(self):
        self.assertEqual(self.calc.evaluate_expression("5 ~"), -5)
        self.assertEqual(self.calc.evaluate_expression("5 ~ 3 *"), -15)
        self.assertEqual(self.calc.evaluate_expression("2 3 ~ *"), -6)

    def test_float_operations(self):
        self.assertEqual(self.calc.evaluate_expression("3.5 2 *"), 7.0)
        self.assertAlmostEqual(self.calc.evaluate_expression("10 3 /"), 10 / 3)

    def test_brackets(self):
        self.assertEqual(self.calc.evaluate_expression("( 2 + 3 )"), 5)
        self.assertEqual(self.calc.evaluate_expression("( 5 - 2 )"), 3)
        self.assertEqual(self.calc.evaluate_expression("2 * ( 3 + 4 )"), 14)
        self.assertEqual(self.calc.evaluate_expression("( 5 + 3 ) * ( 2 + 4 )"), 48)
        self.assertEqual(self.calc.evaluate_expression("( ( 2 + 3 ) * 4 )"), 20)
        self.assertEqual(self.calc.evaluate_expression("~ ( 2 + 3 )"), -5)

    def test_warnings(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.calc.evaluate_expression("")
            self.assertEqual(len(w), 1)
            self.assertIn("Пустое выражение", str(w[0].message))

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.calc.evaluate_expression("0 0 **")
            self.assertEqual(len(w), 1)
            self.assertIn("0^0", str(w[0].message))

    def test_errors(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate_expression("5 0 /")

        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate_expression("5 0 //")

        with self.assertRaises(ValueError):
            self.calc.evaluate_expression("3 +")

        with self.assertRaises(ValueError):
            self.calc.evaluate_expression("2 3 $")

        with self.assertRaises(ValueError):
            self.calc.evaluate_expression("2 3 4 +")

        with self.assertRaises(ValueError):
            self.calc.evaluate_expression("( 2 + 3")

        with self.assertRaises(TypeError):
            self.calc.evaluate_expression("5.5 2 //")

    def test_edge_cases(self):
        self.assertEqual(self.calc.evaluate_expression("42"), 42)
        self.assertEqual(self.calc.evaluate_expression("-5 3 +"), -2)
        self.assertEqual(self.calc.evaluate_expression("0 5 +"), 5)
        self.assertEqual(self.calc.evaluate_expression("5 0 -"), 5)
        self.assertEqual(self.calc.evaluate_expression("0 5 *"), 0)
        self.assertEqual(self.calc.evaluate_expression("  2   3   +  "), 5)


if __name__ == '__main__':
    unittest.main()