# -*- coding: utf-8 -*-
"""
Filename: main.py
Description: A credit analysis program
Authors:
    - Dirceu de Medeiros Teixeira
    - Chng Zuo En Calvin
    - Kelvin Thein
    - Melani Sugiharti The
Date Created: 2024-11-05
Last Modified: 2024-11-05
Version: 1.0

Usage:
    python main.py

Dependencies:
    List any external dependencies or libraries.

License:
    MIT License
"""


from enum import Enum, auto
import re
import unittest
from unittest.mock import patch
import subprocess
import sys
from unittest.runner import TextTestResult

# This can be used in the future to build the gui mode
REQUIRED_MODULES = ['streamlit', 'pandas']  # Add more modules as needed


class TestBorrowerDetails(unittest.TestCase):

    def test_validate_full_name_valid(self):
        valid_names = [
            "John Doe",
            "Dirceu de Medeiros Teixeira",
            "José Silva",
            "Marie Curie",
            "René Descartes",
            "Müller",
            "李小龙",
            "Иван Иванович"
        ]
        for name in valid_names:
            self.assertTrue(validate_full_name(name), f"'{name}' should be valid")

    def test_validate_full_name_invalid(self):
        invalid_names = [
            "123 John",
            "John_Doe",
            "John@Doe",
            "",
            " "
        ]
        for name in invalid_names:
            self.assertFalse(validate_full_name(name), f"'{name}' should be invalid")

    def test_get_age_status(self):
        self.assertEqual(get_age_status(20), BorrowStatus.REJECTED, "Age 20 should be REJECTED")
        self.assertEqual(get_age_status(65), None, "Age 65 should be ACCEPTED")
        self.assertEqual(get_age_status(21), None, "Age 21 should be ACCEPTED")
        self.assertEqual(get_age_status(66), BorrowStatus.REJECTED, "Age 66 should be REJECTED")

    def test_get_guarantor_score(self):
        self.assertEqual(get_guarantor_score(1), 5, "1 guarantor should give a score of 5")
        self.assertEqual(get_guarantor_score(2), 4, "2 guarantors should give a score of 4")
        self.assertEqual(get_guarantor_score(3), 3, "3 guarantors should give a score of 3")
        self.assertEqual(get_guarantor_score(4), 2, "4 guarantors should give a score of 2")
        self.assertEqual(get_guarantor_score(5), 1, "More than 4 guarantors should give a score of 1")

    def test_grade_score_enum(self):
        self.assertEqual(GradeScore.A.value, 1, "GradeScore A should have value 1")
        self.assertEqual(GradeScore.B.value, 2, "GradeScore B should have value 2")
        self.assertEqual(GradeScore.Z.value, 26, "GradeScore Z should have value 26")

    @patch('builtins.input', side_effect=["123 John", "John Doe"])
    def test_get_borrower_name_invalid(self):
        result = get_borrower_full_name(INPUT_FULL_NAME_MESSAGE)
        self.assertEqual(result, "John Doe", "The function should return the valid name after invalid attempts")

    @patch('builtins.input', side_effect=["John Doe"])
    def test_get_borrower_name(self):
        result = get_borrower_full_name(INPUT_FULL_NAME_MESSAGE)
        self.assertEqual(result, "John Doe", "The function should return the valid name immediately")

class TestResult(TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_cases = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_cases.append(f"{test} - PASSED")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_cases.append(f"{test} - FAILED")

    def addError(self, test, err):
        super().addError(test, err)
        self.test_cases.append(f"{test} - ERROR")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_cases.append(f"{test} - SKIPPED")


def install_missing_modules():
    """
    Install missing modules automatically using pip.
    """
    for module in REQUIRED_MODULES:
        try:
            __import__(module)
        except ImportError:
            print(f"{module} is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])


def run_tests():
    """
    Manually add test cases to the test suite and run unit tests
    before executing the main program.
    """
    print("Running tests...")

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBorrowerDetails))

    runner = unittest.TextTestRunner(verbosity=2, resultclass=TestResult)
    result = runner.run(suite)

    total_tests = result.testsRun
    passed_tests = total_tests - len(result.failures) - len(result.errors)

    print("\nTest Summary:")
    print(f"Total Tests Run: {total_tests}")
    print(f"Tests Passed: {passed_tests}/{total_tests}")

    if result.wasSuccessful():
        print("All tests passed.")
    else:
        print("Some tests failed or encountered errors.")

    for test_case in result.test_cases:
        print(test_case)

def print_header():
    header = f"""
    #################################################
    #  Script: main.py
    #  Description: A credit analysis program
    #  Authors: 
    #    - Dirceu de Medeiros Teixeira
    #    - Chng Zuo En Calvin
    #    - Kelvin Thein
    #    - Melani Sugiharti The
    #  Date Created: 2024-11-05
    #  Last Modified: 2024-11-05
    #  Version: 1.0
    ##################################################
    ##################################################
    #               
    #               Credit Analysis
    # 
    ##################################################
    """
    print(header)

INPUT_FULL_NAME_MESSAGE = "Please enter the borrower's full name: "
INVALID_NAME_MESSAGE = "Invalid full name. Please enter a valid full name (First and Last name) without numbers."


def get_borrower_full_name(input_message):
    while True:
        borrower_full_name = input(input_message)
        if validate_full_name(borrower_full_name):
            return  borrower_full_name
        else:
            print(INVALID_NAME_MESSAGE)

# This regex validates names with letters and spaces only, in any language
def validate_full_name(name: str) -> bool:
    pattern = r"^[^\W\d_]+(?: [^\W\d_]+)*$"
    return bool(re.match(pattern, name, re.UNICODE))


class GradeScore(Enum):
    A = 1
    B = 2
    C = 3
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()


def get_age_status(age):
    if age < 21 or age >  65: return BorrowStatus.REJECTED

class BorrowStatus(Enum):
    ACCEPTED = auto()
    REJECTED = auto()

class ClientBankStatus(Enum):
    NEW_BANK = 4
    EXISTING_TO_A_BANK = 2

class EntityType(Enum):
    SOLE_PROPRIETORSHIP = 3
    LIMITED_PARTNERSHIP = 2
    COMPANY_LIMITED = 1


def get_guarantor_score(guarantors: int) -> int:
    if guarantors > 4:
        return 1

    match guarantors:
        case 1:
            return 5
        case 2:
            return 4
        case 3:
            return 3
        case 4:
            return 2


def borrow_details():
    return ""

def main():
    print_header()
    print(get_borrower_full_name(INPUT_FULL_NAME_MESSAGE))
if __name__ == "__main__":
    run_tests()
    main()
