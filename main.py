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


def print_header():
    header = """
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
    #################################################
    """
    print(header)

def get_borrower_name():
    return validate_full_name(input("Name of Borrower -> "))

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
if __name__ == "__main__":
    main()
    unittest.main()

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

    @patch('builtins.input', return_value="John Doe")
    def test_get_borrower_name(self, mock_input):
        self.assertTrue(get_borrower_name(), "John Doe should be a valid name")

    @patch('builtins.input', return_value="123 John")
    def test_get_borrower_name_invalid(self, mock_input):
        self.assertFalse(get_borrower_name(), "123 John should be invalid")