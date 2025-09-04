import unittest

# This is a placeholder for the student's code module,
# which will be imported dynamically by the autograder.
# We give it a known name, `student_code`.
import student_code

class TestProblemSet(unittest.TestCase):
    """
    A collection of unit tests to verify the student functions.
    """

    def test_add_numbers_positive(self):
        """Tests the add_numbers function with positive integers."""
        self.assertEqual(student_code.add_numbers(2, 3), 5)

    def test_add_numbers_negative(self):
        """Tests the add_numbers function with negative integers."""
        self.assertEqual(student_code.add_numbers(-5, -10), -15)

    def test_add_numbers_mixed(self):
        """Tests the add_numbers function with negative integers."""
        self.assertEqual(student_code.add_numbers(100, -20), 80)
    