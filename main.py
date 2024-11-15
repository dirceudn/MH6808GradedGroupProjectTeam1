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
        self.assertEqual(invalid_borrow_history_grade("A"), False, "Grade A should not reject")
        self.assertEqual(invalid_borrow_history_grade("C"), False, "Grade C should not reject")
        self.assertEqual(invalid_borrow_history_grade("D"), True, "Grade D should be rejected")
        self.assertEqual(invalid_borrow_history_grade("Z"), True, "Grade Z should be rejected")

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

    def test_validate_property_type(self):
        self.assertTrue(validate_property_type("1"), "Option '1' should be valid")
        self.assertTrue(validate_property_type("2"), "Option '2' should be valid")
        self.assertFalse(validate_property_type("5"), "Option '5' should be invalid")

    def test_validate_property_location(self):
        self.assertTrue(validate_property_location("1"), "Option '1' should be valid")
        self.assertTrue(validate_property_location("2"), "Option '2' should be valid")
        self.assertFalse(validate_property_location("4"), "Option '4' should be invalid")

    def test_validate_property_status_input(self):
        self.assertTrue(validate_property_status_input("1"), "Option '1' should be valid")
        self.assertTrue(validate_property_status_input("2"), "Option '2' should be valid")
        self.assertFalse(validate_property_status_input("3"), "Option '3' should be invalid")

    def test_validate_type_of_facility_applying_input(self):
        self.assertTrue(validate_type_of_facility_applying_input("1"), "Option '1' should be valid")
        self.assertTrue(validate_type_of_facility_applying_input("2"), "Option '2' should be valid")
        self.assertFalse(validate_type_of_facility_applying_input("3"), "Option '3' should be invalid")

    def test_get_debt_to_sales_ratio(self):
        self.assertAlmostEqual(get_debt_to_sales_ratio(50000, 100000), 50.0, msg="Ratio should be 50.0%")
        self.assertAlmostEqual(get_debt_to_sales_ratio(20000, 50000), 40.0, msg="Ratio should be 40.0%")

    def test_get_loan_to_valuation(self):
        self.assertAlmostEqual(get_loan_to_valuation(50000, 100000), 50.0, msg="Ratio should be 50.0%")
        self.assertAlmostEqual(get_loan_to_valuation(20000, 50000), 40.0, msg="Ratio should be 40.0%")

    def test_get_debt_to_income_ratio(self):
        self.assertAlmostEqual(get_debt_to_income_ratio(50000, 100000), 50.0, msg="Ratio should be 50.0%")
        self.assertAlmostEqual(get_debt_to_income_ratio(20000, 50000), 40.0, msg="Ratio should be 40.0%")


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


MIN_BORROWER_INFO_SCORE = 15

INPUT_FULL_NAME_MESSAGE = "Please enter the borrower's full name: "
INPUT_BORROWER_HISTORY = "Please enter the borrower's borrowing history A-Z: "
INPUT_NUMBER_OF_GUARANTORS = "Please enter the number of guarantors: "
INPUT_AGE_OF_GUARANTORS = "Please enter age of guarantors: "
INPUT_TOTAL_DEBT_MESSAGE = "Please enter current total debt: "
INPUT_APPLIED_LOAN_AMOUNT = "Please enter the applied loan amount: "
INPUT_TOTAL_SALES_PER_YEAR = "Please enter total sales per year: "
INPUT_CURRENT_MARKET_VALUE = "Please Current Market Value (CMV): "
INPUT_PROPERTY_TYPE = '''
Please select a property type:
    
(1) Residential Landed
(2) Residential Apartment
(3) Commercial
(4) Others

Enter the number corresponding to your choice (1-4): '''

INPUT_PROPERTY_LOCATION_TYPE = '''
Please select a property location type:

(1) Central Area
(2) Urban
(3) Suburban

Enter the number corresponding to your choice (1-3): '''

INPUT_TYPE_OF_FACILITY_APPLYING = '''
Please select a type of facility applying:

(1) Revolving Credit
(2) Term loan

Enter the number corresponding to your choice (1-2): '''

INPUT_CURRENT_PROPERTY_STATUS = '''
Please select your property status:

(1) Under construction
(2) Completed

Enter the number corresponding to your choice (1-2): '''

INPUT_ENTITY_TYPE = '''
Please select the client  entity status::

(1) Sole Proprietorship
(2) Limited Partnership
(3) Company Limited

Enter the number corresponding to your choice (1-3): '''

INPUT_CLIENT_BANK_STATUS = '''
Please select the client bank's status:

(1) New bank
(2) Existing to a bank

Enter the number corresponding to your choice (1-2): '''

INPUT_GROSS_INCOME_MESSAGE = "Please enter total income: "
INVALID_TYPE_OF_FACILITY_APPLYING_MESSAGE = " Enter the number corresponding to your choice (1-2)"
INVALID_PROPERTY_LOCATION_TYPE_MESSAGE = "Enter the number corresponding to your choice (1-3)"
INVALID_TYPE_PROPERTY_MESSAGE = "Enter the number corresponding to your choice (1-4)"
INVALID_NAME_MESSAGE = "Invalid full name. Please enter a valid full name (First and Last name) without numbers."
INVALID_BORROWER_HISTORY_MESSAGE = "Please enter history input A-Z or a-z format."
INVALID_NUMBER_GUARANTOR_MESSAGE = "Please enter a guarantor number upper than zero and only numbers."
INVALID_TOTAL_DEBT_MESSAGE = "Please enter a debt number upper than zero and only numbers."
INVALID_TOTAL_INCOME_MESSAGE = "Please enter income a number upper than zero and only numbers."
INVALID_APPLIED_LOAN_AMOUNT_MESSAGE = "Please enter applied loan amount a number upper than zero and only numbers."
INVALID_CURRENT_MARKET_VALUE = "Please enter current market value (CVM) a number upper than zero and only numbers."
INVALID_TOTAL_SALES_PER_YEAR_MESSAGE = "Please enter total sales per year a number upper than zero and only numbers."
ERROR_MESSAGE_CLIENT_BANK_STATUS = "Sorry! Please Choose '1' for New bank or '2' for Existing to a bank."
ERROR_UPDATE_SCORE_MESSAGE = "Invalid score. Please provide an integer value."
ERROR_MESSAGE_ENTITY_TYPE = "Sorry! Please Choose \n'1' for Sole Proprietorship or \n'2' for Limited Partnership or \n'3' for Company Limited \n."


class EntityType(Enum):
    SOLE_PROPRIETORSHIP = 3
    LIMITED_PARTNERSHIP = 2
    COMPANY_LIMITED = 1


class LocationProperty(Enum):
    URBAN = 3
    SUBURBAN = 2
    CENTRAL_AREA = 1


class TypeProperty(Enum):
    OTHER = 4
    COMMERCIAL = 3
    RESIDENTIAL_APARTMENT = 2
    RESIDENTIAL_LANDED = 1


class ClientBankStatus(Enum):
    NEW_BANK = 4
    EXISTING_TO_A_BANK = 2


class BorrowStatus(Enum):
    ACCEPTED = auto()
    REJECTED = auto()
    IN_PROGRESS = auto()


class CurrentPropertyStatus(Enum):
    UNDER_CONSTRUCTION = auto()
    COMPLETED = auto()


class TypeFacilityApplying(Enum):
    REVOLVING_CREDIT = 2
    TERM_LOAN = 1


class FinancialDetails:
    def __init__(self, current_total_debt, gross_income, total_sales_per_year, debt_to_sales_ration,
                 debt_to_income_ratio):
        self.current_total_debt = current_total_debt
        self.gross_income = gross_income
        self.total_sales_per_year = total_sales_per_year
        self.debt_to_sales_ration = debt_to_sales_ration
        self.debt_to_income_ratio = debt_to_income_ratio


class CollateralDetails:
    def __init__(self, current_market_value, type_of_property, current_property_status, location_of_the_property):
        self.current_market_value = current_market_value
        self.type_of_property = type_of_property
        self.current_property_status = current_property_status
        self.location_of_the_property = location_of_the_property


class FacilityDetails:
    def __init__(self, type_of_facility_applying, applied_loan_amount,
                 loan_to_valuation):
        self.type_of_facility_applying = type_of_facility_applying
        self.applied_loan_amount = applied_loan_amount
        self.loan_to_valuation = loan_to_valuation


class Borrower:
    def __init__(self, full_name, entity_type, bank_status, number_of_guarantors, age_of_guarantors, borrowing_history,
                 borrower_financial_details: FinancialDetails = None,
                 borrower_collateral_detail: CollateralDetails = None,
                 borrower_facility_details: FacilityDetails = None,
                 borrower_status=BorrowStatus.IN_PROGRESS, borrower_score=0):
        self.full_name = full_name
        self.entity_type = entity_type
        self.bank_status = bank_status
        self.number_of_guarantors = number_of_guarantors
        self.age_of_guarantors = age_of_guarantors
        self.borrowing_history = borrowing_history
        self.borrower_score = borrower_score
        self.borrower_financial_details = borrower_financial_details
        self.borrower_collateral_detail = borrower_collateral_detail
        self.borrower_facility_details = borrower_facility_details
        self.borrower_status = borrower_status

    def update_borrower_score(self):
        if invalid_guarantors_age(
                self.age_of_guarantors) or self.number_of_guarantors < 1 or invalid_borrow_history_grade(
            self.borrowing_history):
            self.borrower_status = BorrowStatus.REJECTED

        self.borrower_score = (
                get_entity_type_score(self.entity_type) +
                get_bank_status_score(self.bank_status) +
                get_guarantor_score(self.number_of_guarantors) +
                get_grade_history_score(self.borrowing_history.upper())
        )
        if self.borrower_score >= MIN_BORROWER_INFO_SCORE:
            self.borrower_status = BorrowStatus.REJECTED

    def update_borrower_status(self, new_borrow_status):
        self.borrower_status = new_borrow_status

    def display_borrower_info(self):
        info = {
            "Full Name": self.full_name,
            "Entity Type": self.entity_type.name,
            "Bank Status": self.bank_status.name,
            "Number of Guarantors": self.number_of_guarantors,
            "Age of Guarantors": self.age_of_guarantors,
            "Borrowing History": self.borrowing_history,
            "Borrower Score": self.borrower_score,
            "Current Total Debt": self.borrower_financial_details.current_total_debt,
            "Gross Income": self.borrower_financial_details.gross_income,
            "Total Sales per year": self.borrower_financial_details.total_sales_per_year,
            "Debt to Income Ratio": self.borrower_financial_details.total_sales_per_year,
            "Current Market Value CVM": self.borrower_collateral_detail.current_market_value,
            "Type of Property": self.borrower_collateral_detail.type_of_property,
            "Location of Property": self.borrower_collateral_detail.location_of_the_property,
            "Type of Facility Applying": self.borrower_facility_details.type_of_facility_applying,
            "Applied Loan Amount": self.borrower_facility_details.applied_loan_amount,
            "Loan to Valuation": self.borrower_facility_details.loan_to_valuation,
            "Status": self.borrower_status.name,
        }
        for key, value in info.items():
            print(f"{key}: {value}")


entity_type_dic = {"1": EntityType.SOLE_PROPRIETORSHIP,
                   "2": EntityType.LIMITED_PARTNERSHIP,
                   "3": EntityType.COMPANY_LIMITED}

property_type_dic = {"1": TypeProperty.RESIDENTIAL_LANDED,
                     "2": TypeProperty.RESIDENTIAL_APARTMENT,
                     "3": TypeProperty.COMMERCIAL,
                     "4": TypeProperty.OTHER}

property_location_dic = {"1": LocationProperty.CENTRAL_AREA,
                         "2": LocationProperty.URBAN,
                         "3": LocationProperty.SUBURBAN}

current_property_status_dic = {"1": CurrentPropertyStatus.UNDER_CONSTRUCTION,
                               "2": CurrentPropertyStatus.COMPLETED}

client_bank_status_dic = {
    "1": ClientBankStatus.NEW_BANK,
    "2": ClientBankStatus.EXISTING_TO_A_BANK}

type_of_facility_applying_dic = {
    "1": TypeFacilityApplying.REVOLVING_CREDIT,
    "2": TypeFacilityApplying.TERM_LOAN}


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
    if guarantors > 4 or guarantors == 0:
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


def invalid_borrow_history_grade(history: str) -> bool:
    pattern_status = r'^[a-cA-C]+$'
    return not re.match(pattern_status, history)


def validate_client_bank_status_option(option: str) -> bool:
    return option in client_bank_status_dic


def validate_number_input(number) -> bool:
    return number.isdigit() and int(number) >= 0


def validate_entity_type(option: str) -> bool:
    return option in entity_type_dic


def validate_property_type(option: str) -> bool:
    return option in property_type_dic


def validate_property_location(option: str) -> bool:
    return option in property_location_dic


def validate_property_status_input(option: str) -> bool:
    return option in current_property_status_dic


def validate_type_of_facility_applying_input(option: str) -> bool:
    return option in type_of_facility_applying_dic


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


def input_current_total_debt():
    while True:
        total_debt_input = input(INPUT_TOTAL_DEBT_MESSAGE)
        if validate_number_input(total_debt_input):
            return int(total_debt_input)
        print(INVALID_TOTAL_DEBT_MESSAGE)


def input_gross_income():
    while True:
        total_debt_input = input(INPUT_TOTAL_DEBT_MESSAGE)
        if validate_number_input(total_debt_input):
            return int(total_debt_input)
        print(INVALID_TOTAL_INCOME_MESSAGE)


def input_applied_loan_amount():
    while True:
        loan_amount = input(INPUT_APPLIED_LOAN_AMOUNT)
        if validate_number_input(loan_amount):
            return int(loan_amount)
        print(INVALID_APPLIED_LOAN_AMOUNT_MESSAGE)


def input_total_sales_per_year():
    while True:
        total_debt_input = input(INPUT_TOTAL_SALES_PER_YEAR)
        if validate_number_input(total_debt_input):
            return int(total_debt_input)
        print(INVALID_TOTAL_SALES_PER_YEAR_MESSAGE)


def input_current_market_value():
    while True:
        market_value = input(INPUT_CURRENT_MARKET_VALUE)
        if validate_number_input(market_value):
            return int(market_value)
        print(INVALID_TOTAL_SALES_PER_YEAR_MESSAGE)


def input_type_of_property():
    while True:
        property_type = str(input(INPUT_PROPERTY_TYPE))
        if validate_property_type(property_type):
            return property_type_dic[property_type]
        print(INVALID_TOTAL_SALES_PER_YEAR_MESSAGE)


def input_current_property_status():
    while True:
        property_status = str(input(INPUT_CURRENT_PROPERTY_STATUS))
        if validate_property_status_input(property_status):
            return property_status
        print(INVALID_TOTAL_SALES_PER_YEAR_MESSAGE)


def input_location_of_property():
    while True:
        property_location = str(input(INPUT_PROPERTY_LOCATION_TYPE))
        if validate_property_location(property_location):
            return property_location_dic[property_location]
        print(INVALID_TOTAL_SALES_PER_YEAR_MESSAGE)


def input_type_of_facility_applying():
    while True:
        type_of_facility_applying = str(input(INPUT_TYPE_OF_FACILITY_APPLYING))
        if validate_type_of_facility_applying_input(type_of_facility_applying):
            return type_of_facility_applying_dic[type_of_facility_applying]
        print(INVALID_TYPE_OF_FACILITY_APPLYING_MESSAGE)


def get_debt_to_sales_ratio(current_total_debt, total_sales_per_year) -> float:
    return float(current_total_debt / total_sales_per_year) * 100


def get_loan_to_valuation(applied_loan_amount, current_market_value) -> float:
    return float(applied_loan_amount / current_market_value) * 100


def get_debt_to_income_ratio(current_total_debt, gross_income) -> float:
    return float(current_total_debt / gross_income) * 100


def get_borrow_details_status(borrower: Borrower) -> BorrowStatus:
    borrower.update_borrower_score()
    return borrower.borrower_status


# ----------------------------------------------------------------------------------------------------------------------

def analyze_borrow_information():
    # borrower details
    borrower_full_name, entity_type, client_bank_status, number_of_guarantors, age_of_guarantors, borrower_history = borrow_details()

    current_total_debt, gross_income, total_sales_per_year, debt_to_sales_ratio, debt_to_income_ratio = financial_details()
    financial_borrower_details = FinancialDetails(current_total_debt, gross_income, total_sales_per_year,
                                                  debt_to_sales_ratio, debt_to_income_ratio)
    current_market_value, type_of_property, current_property_status, location_of_property = collateral_details()
    collateral_detail = CollateralDetails(current_market_value, type_of_property, current_property_status,
                                          location_of_property)
    type_of_facility_applying, applied_loan_amount = facility_details()
    loan_to_valuation = get_loan_to_valuation(applied_loan_amount, current_market_value)
    facility_detail = FacilityDetails(type_of_facility_applying, applied_loan_amount, loan_to_valuation)
    borrower = Borrower(borrower_full_name, entity_type, client_bank_status, number_of_guarantors, age_of_guarantors,
                        borrower_history, financial_borrower_details, collateral_detail, facility_detail)


def borrow_details():
    borrower_full_name = input_borrower_full_name()
    entity_type = input_entity_type()
    client_bank_status = input_client_bank_status()
    number_of_guarantors = input_number_of_guarantors()
    age_of_guarantors = input_age_of_guarantors()
    borrower_history = input_borrower_borrowing_history()
    return borrower_full_name, entity_type, client_bank_status, number_of_guarantors, age_of_guarantors, borrower_history
    # borrower = Borrower(borrower_full_name, entity_type, client_bank_status, number_of_guarantors, age_of_guarantors,
    #                   borrower_history)
    # get_borrow_details_status(borrower)
    # borrower.display_borrower_info()


def collateral_details():
    current_market_value = input_current_market_value()
    type_of_property = input_type_of_property()
    current_property_status = input_current_property_status()
    location_of_property = input_location_of_property()
    return current_market_value, type_of_property, current_property_status, location_of_property


def financial_details():
    current_total_debt = input_current_total_debt()
    gross_income = input_gross_income()
    total_sales_per_year = input_total_sales_per_year()
    debt_to_sales_ratio = get_debt_to_sales_ratio(current_total_debt, total_sales_per_year)
    debt_to_income_ratio = get_debt_to_income_ratio(current_total_debt, gross_income)
    return current_total_debt, gross_income, total_sales_per_year, debt_to_sales_ratio, debt_to_income_ratio


def facility_details():
    type_of_facility_applying = input_type_of_facility_applying()
    applied_loan_amount = input_applied_loan_amount()
    return type_of_facility_applying, applied_loan_amount


if __name__ == "__main__":
    run_tests()
    print_header()
    borrow_details()
    financial_details()
    collateral_details()
    facility_details()
