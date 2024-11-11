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

import re
import subprocess
import sys
import unittest
from enum import Enum, auto
from unittest.mock import patch
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
        self.assertEqual(invalid_guarantors_age(20), True, "Age 20 should be REJECTED")
        self.assertEqual(invalid_guarantors_age(65), False, "Age 65 should be ACCEPTED")
        self.assertEqual(invalid_guarantors_age(21), False, "Age 21 should be ACCEPTED")
        self.assertEqual(invalid_guarantors_age(66), True, "Age 66 should be REJECTED")

    def test_get_guarantor_score(self):
        self.assertEqual(get_guarantor_score(1), 5, "1 guarantor should give a score of 5")
        self.assertEqual(get_guarantor_score(2), 4, "2 guarantors should give a score of 4")
        self.assertEqual(get_guarantor_score(3), 3, "3 guarantors should give a score of 3")
        self.assertEqual(get_guarantor_score(4), 2, "4 guarantors should give a score of 2")
        self.assertEqual(get_guarantor_score(5), 1, "More than 4 guarantors should give a score of 1")

    def test_grade_score_enum(self):
        self.assertEqual(GradeScore.A.value, 1, "GradeScore A should have value 1")
        self.assertEqual(GradeScore.B.value, 2, "GradeScore B should have value 2")

    @patch('builtins.input', side_effect=["123 John", "John Doe"])
    def test_get_borrower_name_invalid(self, mock):
        result = input_borrower_full_name()
        self.assertEqual(result, "John Doe", "The function should return the valid name after invalid attempts")

    @patch('builtins.input', side_effect=["John Doe", "John Doe"])
    def test_get_borrower_name(self, mock):
        result = input_borrower_full_name()
        self.assertEqual(result, "John Doe", "The function should return the valid name immediately")

    def test_get_grade_history_score(self):
        self.assertEqual(get_grade_history_score("A"), 1, "Grade A should give a score of 1")
        self.assertEqual(get_grade_history_score("B"), 2, "Grade B should give a score of 2")
        self.assertEqual(get_grade_history_score("C"), 3, "Grade C should give a score of 3")

    def test_get_bank_status_score(self):
        self.assertEqual(get_bank_status_score(ClientBankStatus.NEW_BANK), 4, "New Bank should give a score of 4")
        self.assertEqual(get_bank_status_score(ClientBankStatus.EXISTING_TO_A_BANK), 2,
                         "Existing Bank should give a score of 2")

    def test_get_entity_type_score(self):
        self.assertEqual(get_entity_type_score(EntityType.SOLE_PROPRIETORSHIP), 3,
                         "Sole Proprietorship should give a score of 3")
        self.assertEqual(get_entity_type_score(EntityType.LIMITED_PARTNERSHIP), 2,
                         "Limited Partnership should give a score of 2")
        self.assertEqual(get_entity_type_score(EntityType.COMPANY_LIMITED), 1,
                         "Company Limited should give a score of 1")

    def test_get_borrow_history_status(self):
        self.assertEqual(get_borrow_history_status("A"), BorrowStatus.IN_PROGRESS, "Grade A should not reject")
        self.assertEqual(get_borrow_history_status("C"), BorrowStatus.IN_PROGRESS, "Grade C should not reject")
        self.assertEqual(get_borrow_history_status("D"), BorrowStatus.REJECTED, "Grade D should be rejected")
        self.assertEqual(get_borrow_history_status("Z"), BorrowStatus.REJECTED, "Grade Z should be rejected")

    def test_validate_borrower_history(self):
        self.assertTrue(validate_borrower_history("A"), "History 'A' should be valid")
        self.assertTrue(validate_borrower_history("B"), "History 'B' should be valid")
        self.assertFalse(validate_borrower_history("123"), "Numeric history should be invalid")
        self.assertFalse(validate_borrower_history(""), "Empty history should be invalid")

    def test_validate_client_bank_status_option(self):
        self.assertTrue(validate_client_bank_status_option("1"), "Option '1' should be valid")
        self.assertTrue(validate_client_bank_status_option("2"), "Option '2' should be valid")
        self.assertFalse(validate_client_bank_status_option("3"), "Option '3' should be invalid")

    def test_validate_number_input(self):
        self.assertTrue(validate_number_input("5"), "Number '5' should be valid")
        self.assertFalse(validate_number_input("-1"), "Negative numbers should be invalid")
        self.assertFalse(validate_number_input("abc"), "Non-numeric input should be invalid")

    def test_validate_entity_type(self):
        self.assertTrue(validate_entity_type("1"), "Option '1' should be valid")
        self.assertTrue(validate_entity_type("2"), "Option '2' should be valid")
        self.assertTrue(validate_entity_type("3"), "Option '3' should be valid")
        self.assertFalse(validate_entity_type("4"), "Option '4' should be invalid")

    def test_get_borrow_details_status(self):
        borrower = Borrower(
            full_name="John Doe",
            entity_type=EntityType.SOLE_PROPRIETORSHIP,
            bank_status=ClientBankStatus.NEW_BANK,
            number_of_guarantors=1,
            age_of_guarantors=30,
            borrowing_history="A"
        )
        status = get_borrow_details_status(borrower)
        self.assertEqual(status, BorrowStatus.IN_PROGRESS, "Borrower should have IN_PROGRESS status")
        self.assertEqual(borrower.borrower_score, 13,
                         "Borrower score should be 13 for Sole Proprietorship, New Bank, and 1 Guarantor")


class TestResult(TextTestResult):
    def __init__(self, *args):
        super().__init__(*args)
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
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestBorrowerDetails))

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


def print_header():
    header = f"""
    #################################################
    #  Script: main.py
    #  Run: python main.py
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
INPUT_BORROWER_HISTORY = "Please enter the borrower's borrowing history A-Z: "
INPUT_NUMBER_OF_GUARANTORS = "Please enter the number of guarantors: "
INPUT_AGE_OF_GUARANTORS = "Please enter age of guarantors: "
INPUT_CLIENT_BANK_STATUS = "Please select the client bank's status: \n(1) New bank \n(2) Existing to a bank \n > "
INPUT_ENTITY_TYPE = "Please select the client  entity status: \n(1) Sole Proprietorship \n(2) Limited Partnership \n(3) Company Limited \n > "
INVALID_NAME_MESSAGE = "Invalid full name. Please enter a valid full name (First and Last name) without numbers."
INVALID_BORROWER_HISTORY_MESSAGE = "Please enter history input A-Z or a-z format."
INVALID_NUMBER_GUARANTOR_MESSAGE = "Please enter a number upper than zero and only numbers."
ERROR_MESSAGE_CLIENT_BANK_STATUS = "Sorry! Please Choose '1' for New bank or '2' for Existing to a bank."
ERROR_UPDATE_SCORE_MESSAGE = "Invalid score. Please provide an integer value."
ERROR_MESSAGE_ENTITY_TYPE = "Sorry! Please Choose \n'1' for Sole Proprietorship or \n'2' for Limited Partnership or \n'3' for Company Limited \n."


class EntityType(Enum):
    SOLE_PROPRIETORSHIP = 3
    LIMITED_PARTNERSHIP = 2
    COMPANY_LIMITED = 1


class ClientBankStatus(Enum):
    NEW_BANK = 4
    EXISTING_TO_A_BANK = 2


class BorrowStatus(Enum):
    ACCEPTED = auto()
    REJECTED = auto()
    IN_PROGRESS = auto()


class Borrower:
    def __init__(self, full_name, entity_type, bank_status, number_of_guarantors, age_of_guarantors, borrowing_history,
                 borrower_score=0, borrower_status=BorrowStatus.IN_PROGRESS):
        self.full_name = full_name
        self.entity_type = entity_type
        self.bank_status = bank_status
        self.number_of_guarantors = number_of_guarantors
        self.age_of_guarantors = age_of_guarantors
        self.borrowing_history = borrowing_history
        self.borrower_score = borrower_score
        self.borrower_status = borrower_status

    def update_borrower_score(self, new_score):
        if isinstance(new_score, int):
            self.borrower_score += new_score
        else:
            print(ERROR_UPDATE_SCORE_MESSAGE)

    def update_borrower_status(self, new_borrow_status):
        self.borrower_status = new_borrow_status

    def display_borrower_info(self):
        info = (
            f"Borrower Name: {self.full_name}\nEntity Type: {self.entity_type}\nBank Status: {self.bank_status}\n"
            f"Number of guarantors: {self.number_of_guarantors}\nAge of guarantors: {self.age_of_guarantors}\n"
            f"Borrowing history: {self.borrowing_history}\nBorrowing score: {self.borrower_score}\n"
            f"Borrower status: {self.borrower_status}\n")
        print(info)


entity_type_dic = {"1": EntityType.SOLE_PROPRIETORSHIP,
                   "2": EntityType.LIMITED_PARTNERSHIP,
                   "3": EntityType.COMPANY_LIMITED}

client_bank_status_dic = {
    "1": ClientBankStatus.NEW_BANK,
    "2": ClientBankStatus.EXISTING_TO_A_BANK}


class GradeScore(Enum):
    A = 1
    B = 2
    C = 3


def get_grade_history_score(grade: str) -> int:
    match grade:
        case "A":
            return GradeScore.A.value
        case "B":
            return GradeScore.B.value
        case "C":
            return GradeScore.C.value


def invalid_guarantors_age(age: int) -> bool:
    return age < 21 or age > 65


def get_bank_status_score(bank_status: ClientBankStatus) -> int:
    if bank_status == ClientBankStatus.NEW_BANK:
        return 4
    return 2


def get_entity_type_score(entity_type: EntityType) -> int:
    match entity_type:
        case EntityType.SOLE_PROPRIETORSHIP:
            return 3
        case EntityType.LIMITED_PARTNERSHIP:
            return 2
        case EntityType.COMPANY_LIMITED:
            return 1


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


# -------------------------------------- Validate functions ------------------------------------------------------------

def validate_full_name(name: str) -> bool:
    pattern = r"^[^\W\d_]+(?: [^\W\d_]+)*$"
    return bool(re.match(pattern, name, re.UNICODE))


def validate_borrower_history(history: str):
    pattern = r'^[a-zA-Z]+$'
    return bool(re.match(pattern, history))


def get_borrow_history_status(history: str) -> BorrowStatus:
    pattern_status = r'^[a-cA-C]+$'
    if not re.match(pattern_status, history):
        return BorrowStatus.REJECTED
    else:
        return BorrowStatus.IN_PROGRESS


def validate_client_bank_status_option(option: str) -> bool:
    return option in client_bank_status_dic


def validate_number_input(number) -> bool:
    return number.isdigit() and int(number) >= 0


def validate_entity_type(option: str) -> bool:
    return option in entity_type_dic


# ---------------------------------- Input functions -------------------------------------------------------------------

def input_borrower_full_name() -> str:
    while True:
        borrower_full_name = input(INPUT_FULL_NAME_MESSAGE)
        if validate_full_name(borrower_full_name):
            return borrower_full_name


def input_borrower_borrowing_history() -> str:
    while True:
        borrower_borrowing_history = str(input(INPUT_BORROWER_HISTORY))
        if validate_borrower_history(borrower_borrowing_history):
            return borrower_borrowing_history
        print(INVALID_BORROWER_HISTORY_MESSAGE)


def input_client_bank_status():
    while True:
        bank_status = str(input(INPUT_CLIENT_BANK_STATUS))
        if validate_client_bank_status_option(bank_status):
            return client_bank_status_dic[bank_status]
        print(ERROR_MESSAGE_CLIENT_BANK_STATUS)


def input_entity_type():
    while True:
        entity_type = str(input(INPUT_ENTITY_TYPE))
        if validate_entity_type(entity_type):
            return entity_type_dic[entity_type]
        print(ERROR_MESSAGE_ENTITY_TYPE)


def input_number_of_guarantors() -> int:
    while True:
        number_guarantors = input(INPUT_NUMBER_OF_GUARANTORS)
        if validate_number_input(number_guarantors):
            return int(number_guarantors)
        print(INVALID_NUMBER_GUARANTOR_MESSAGE)


def input_age_of_guarantors() -> int:
    while True:
        age_guarantors = input(INPUT_AGE_OF_GUARANTORS)
        if validate_number_input(age_guarantors):
            return int(age_guarantors)
        print(INVALID_NUMBER_GUARANTOR_MESSAGE)


def get_borrow_details_status(borrower: Borrower) -> BorrowStatus:
    entity_score = get_entity_type_score(borrower.entity_type)
    borrower.update_borrower_score(entity_score)

    bank_score = get_bank_status_score(borrower.bank_status)
    borrower.update_borrower_score(bank_score)

    if borrower.number_of_guarantors < 1:
        borrower.update_borrower_status(BorrowStatus.REJECTED)
        return BorrowStatus.REJECTED
    else:
        guarantor_score = get_guarantor_score(borrower.number_of_guarantors)
        borrower.update_borrower_score(guarantor_score)

    if invalid_guarantors_age(borrower.age_of_guarantors):
        borrower.update_borrower_status(BorrowStatus.REJECTED)
        return BorrowStatus.REJECTED

    if get_borrow_history_status(borrower.borrowing_history) == BorrowStatus.REJECTED:
        borrower.update_borrower_status(BorrowStatus.REJECTED)
        return BorrowStatus.REJECTED
    else:
        history_score = get_grade_history_score(borrower.borrowing_history.upper())
        borrower.update_borrower_score(history_score)

    return borrower.borrower_status


# ----------------------------------------------------------------------------------------------------------------------

def borrow_details():
    borrower_full_name = input_borrower_full_name()
    entity_type = input_entity_type()
    client_bank_status = input_client_bank_status()
    number_of_guarantors = input_number_of_guarantors()
    age_of_guarantors = input_age_of_guarantors()
    borrower_history = input_borrower_borrowing_history()
    borrower = Borrower(borrower_full_name, entity_type, client_bank_status, number_of_guarantors, age_of_guarantors,
                        borrower_history)
    current_borrower_status = get_borrow_details_status(borrower)
    if current_borrower_status == BorrowStatus.REJECTED:
        borrower.display_borrower_info()
    elif current_borrower_status == BorrowStatus.IN_PROGRESS:
        print("continue to call other functions")


if __name__ == "__main__":
    run_tests()
    print_header()
    borrow_details()
