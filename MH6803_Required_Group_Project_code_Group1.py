# -*- coding: utf-8 -*-
"""
Filename: MH6803_Required_Group_Project_code_Group1.py
Description: A credit analysis program
Authors:
    - Dirceu de Medeiros Teixeira
    - Chng Zuo En Calvin
    - Kelvin Thein
    - Melani Sugiharti The
Date Created: 2024-11-05
Last Modified: 2024-11-16
Version: 1.0

Usage:
    python MH6803_Required_Group_Project_code_Group1.py

Dependencies:
    List any external dependencies or libraries.

License:
    MIT License
"""

import re
import locale
import unittest
from enum import Enum, auto
from unittest.mock import patch
from unittest.runner import TextTestResult


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
        self.assertAlmostEqual(get_loan_to_valuation_ratio(50000, 100000), 50.0, msg="Ratio should be 50.0%")
        self.assertAlmostEqual(get_loan_to_valuation_ratio(20000, 50000), 40.0, msg="Ratio should be 40.0%")

    def test_get_debt_to_income_ratio(self):
        self.assertAlmostEqual(get_debt_to_income_ratio(50000, 100000), 50.0, msg="Ratio should be 50.0%")
        self.assertAlmostEqual(get_debt_to_income_ratio(20000, 50000), 40.0, msg="Ratio should be 40.0%")

    def test_get_debt_sales_ratio_score(self):
        self.assertEqual(get_debt_sales_ratio_score(75), 0, "Ratio > 70% should return 0")
        self.assertEqual(get_debt_sales_ratio_score(65), 4, "Ratio between 60-70% should return 4")
        self.assertEqual(get_debt_sales_ratio_score(50), 3, "Ratio between 50-59% should return 3")
        self.assertEqual(get_debt_sales_ratio_score(30), 1, "Ratio < 40% should return 1")

    def test_get_to_income_ratio_score(self):
        self.assertEqual(get_to_income_ratio_score(60), 0, "Ratio > 55% should return 0")
        self.assertEqual(get_to_income_ratio_score(50), 3, "Ratio between 35-55% should return 3")
        self.assertEqual(get_to_income_ratio_score(20), 1, "Ratio < 35% should return 1")

    def test_get_loan_to_valuation_ratio_score(self):
        self.assertEqual(get_loan_to_valuation_ratio_score(85), 0, "Ratio > 80% should return 0")
        self.assertEqual(get_loan_to_valuation_ratio_score(75), 2, "Ratio between 60-79% should return 2")
        self.assertEqual(get_loan_to_valuation_ratio_score(50), 1, "Ratio < 60% should return 1")

    def test_calculate_score_and_update_status(self):
        borrower_credit_analysis = BorrowerCreditAnalysis()

        borrower_credit_analysis.get_borrower_information_details_score = lambda: 10
        borrower_credit_analysis.get_financial_details_score = lambda: 5
        borrower_credit_analysis.get_collateral_details_score = lambda: 3
        borrower_credit_analysis.get_facility_details_score = lambda: 3
        borrower_credit_analysis.min_total_credit_score = 20

        borrower_credit_analysis.calculate_score_and_update_status()
        self.assertEqual(
            borrower_credit_analysis.borrower_analysis_status, BorrowStatus.REJECTED,
            "Score >= min_total_credit_score should set status to REJECTED"
        )

        borrower_credit_analysis.get_borrower_information_details_score = lambda: 9
        borrower_credit_analysis.get_financial_details_score = lambda: 5
        borrower_credit_analysis.get_collateral_details_score = lambda: 3
        borrower_credit_analysis.get_facility_details_score = lambda: 2

        borrower_credit_analysis.calculate_score_and_update_status()
        self.assertEqual(
            borrower_credit_analysis.borrower_analysis_status, BorrowStatus.ACCEPTED,
            "Score < min_total_credit_score should set status to ACCEPTED"
        )

    def test_display_rejection_reasons(self):
        borrower_credit_analysis = BorrowerCreditAnalysis()
        borrower_credit_analysis.rejection_reasons.append("Debt-to-sales ratio exceeds 70%.")
        self.assertIn("Debt-to-sales ratio exceeds 70%.",
                      borrower_credit_analysis.get_rejection_results()['rejection_reasons'])

    @patch('builtins.input', side_effect=["50000", "100000", "200000"])
    def test_financial_details_inputs(self, mock_input):
        details = financial_details()
        self.assertEqual(details[0], 50000, "Total debt input mismatch")
        self.assertEqual(details[1], 100000, "Gross income input mismatch")
        self.assertEqual(details[2], 200000, "Total sales input mismatch")

    @patch('builtins.input', side_effect=["1", "2", "3", "4"])
    def test_property_inputs(self, mock_input):
        location_of_property = input_location_of_property()
        self.assertEqual(location_of_property, property_location_dic["1"], "Location property input mismatch")

        type_of_property = input_type_of_property()
        self.assertEqual(type_of_property, property_type_dic["2"], "Property type input mismatch")

    @patch('builtins.input', side_effect=["1", "50000", "75000"])
    def test_facility_inputs(self, mock_input):
        type_of_facility, applied_loan_amount = facility_details()
        self.assertEqual(type_of_facility, type_of_facility_applying_dic["1"], "Facility type mismatch")
        self.assertEqual(applied_loan_amount, 50000, "Loan amount mismatch")


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
    #  Script: MH6803_Required_Group_Project_code_Group1.py
    #  Run: python MH6803_Required_Group_Project_code_Group1.py
    #  Description: A credit analysis program
    #  Authors: 
    #    - Dirceu de Medeiros Teixeira
    #    - Chng Zuo En Calvin
    #    - Kelvin Thein
    #    - Melani Sugiharti The
    #  Date Created: 2024-11-05
    #  Last Modified: 2024-11-16
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


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


class FinancialDetails:
    def __init__(self, current_total_debt, gross_income, total_sales_per_year, debt_to_sales_ration,
                 debt_to_income_ratio):
        self.current_total_debt = current_total_debt
        self.gross_income = gross_income
        self.total_sales_per_year = total_sales_per_year
        self.debt_to_sales_ration = debt_to_sales_ration
        self.debt_to_income_ratio = debt_to_income_ratio


class CollateralDetails:
    def __init__(self, current_market_value, type_of_property: TypeProperty, current_property_status,
                 location_of_the_property: LocationProperty):
        self.current_market_value = current_market_value
        self.type_of_property = type_of_property
        self.current_property_status = current_property_status
        self.location_of_the_property = location_of_the_property


class FacilityDetails:
    def __init__(self, type_of_facility_applying: TypeFacilityApplying, applied_loan_amount,
                 loan_to_valuation):
        self.type_of_facility_applying = type_of_facility_applying
        self.applied_loan_amount = applied_loan_amount
        self.loan_to_valuation = loan_to_valuation


class Borrower:
    def __init__(self, full_name, entity_type, bank_status, number_of_guarantors, age_of_guarantors, borrowing_history):
        self.full_name = full_name
        self.entity_type = entity_type
        self.bank_status = bank_status
        self.number_of_guarantors = number_of_guarantors
        self.age_of_guarantors = age_of_guarantors
        self.borrowing_history = borrowing_history


class BorrowerCreditAnalysis:
    def __init__(self, borrower_information_details: Borrower = None,
                 borrower_financial_details: FinancialDetails = None,
                 borrower_collateral_detail: CollateralDetails = None,
                 borrower_facility_details: FacilityDetails = None,
                 borrower_analysis_status=BorrowStatus.IN_PROGRESS,
                 borrower_analysis_score=0, min_borrow_info_score=15, min_financial_details_score=7,
                 min_collateral_score=5,
                 min_facility_score=4,
                 min_total_credit_score=20,
                 total_credit_score=0):
        self.borrower_information_details = borrower_information_details
        self.borrower_financial_details = borrower_financial_details
        self.borrower_collateral_detail = borrower_collateral_detail
        self.borrower_facility_details = borrower_facility_details
        self.borrower_analysis_status = borrower_analysis_status
        self.borrower_analysis_score = borrower_analysis_score
        self.min_borrow_info_score = min_borrow_info_score
        self.min_financial_details_score = min_financial_details_score
        self.min_collateral_score = min_collateral_score
        self.min_facility_score = min_facility_score
        self.min_total_credit_score = min_total_credit_score
        self.total_credit_score = total_credit_score
        self.rejection_reasons = []

    def get_borrower_information_details_score(self):
        if self.borrower_information_details is not None:
            if invalid_guarantors_age(
                    self.borrower_information_details.age_of_guarantors) or self.borrower_information_details.number_of_guarantors < 1 or invalid_borrow_history_grade(
                self.borrower_information_details.borrowing_history):
                self.borrower_analysis_status = BorrowStatus.REJECTED
            borrower_score = (
                    get_entity_type_score(self.borrower_information_details.entity_type) +
                    get_bank_status_score(self.borrower_information_details.bank_status) +
                    get_guarantor_score(self.borrower_information_details.number_of_guarantors) +
                    get_grade_history_score(self.borrower_information_details.borrowing_history.upper())
            )
            if invalid_borrow_history_grade(self.borrower_information_details.borrowing_history):
                self.rejection_reasons.append("Only borrowing history A,B or C are accepted.")
            if invalid_guarantors_age(self.borrower_information_details.age_of_guarantors):
                self.rejection_reasons.append("Guarantor age is invalid (either below 21 or above 65).")
            if self.borrower_information_details.number_of_guarantors < 1:
                self.rejection_reasons.append("No guarantors provided.")
            if borrower_score >= self.min_borrow_info_score:
                self.borrower_analysis_status = BorrowStatus.REJECTED

            return borrower_score
        return 0

    def get_financial_details_score(self):
        if self.borrower_financial_details is not None:
            debt_to_sales_ratio = get_debt_to_sales_ratio(self.borrower_financial_details.current_total_debt,
                                                          self.borrower_financial_details.total_sales_per_year)
            debt_to_income_ratio = get_debt_to_income_ratio(self.borrower_financial_details.current_total_debt,
                                                            self.borrower_financial_details.gross_income)

            current_debt_sales_ratio_score = get_debt_sales_ratio_score(debt_to_sales_ratio)
            current_debt_to_income_score = get_to_income_ratio_score(debt_to_income_ratio)
            if debt_to_sales_ratio > 70:
                self.rejection_reasons.append("Debt-to-sales ratio exceeds 70%.")
            if debt_to_income_ratio > 55:
                self.rejection_reasons.append("Debt-to-income ratio exceeds 55%.")
            if current_debt_sales_ratio_score == 0 or current_debt_to_income_score == 0:
                self.borrower_analysis_status = BorrowStatus.REJECTED
            financial_details_score = (current_debt_sales_ratio_score + current_debt_to_income_score)
            if financial_details_score >= self.min_financial_details_score:
                self.borrower_analysis_status = BorrowStatus.REJECTED
            return financial_details_score
        return 0

    def get_collateral_details_score(self):
        if self.borrower_collateral_detail is not None:
            if self.borrower_collateral_detail.current_property_status == CurrentPropertyStatus.UNDER_CONSTRUCTION:
                self.rejection_reasons.append("Property is under construction.")
                self.borrower_analysis_status = BorrowStatus.REJECTED
            total_collateral_details_score = (int(self.borrower_collateral_detail.type_of_property.value) + int(
                self.borrower_collateral_detail.location_of_the_property.value))
            if total_collateral_details_score >= self.min_collateral_score:
                self.borrower_analysis_status = BorrowStatus.REJECTED
            return total_collateral_details_score
        return 0

    def get_facility_details_score(self):
        if self.borrower_facility_details is not None:
            loan_to_valuation_score = get_loan_to_valuation_ratio_score(
                get_loan_to_valuation_ratio(self.borrower_facility_details.applied_loan_amount,
                                            self.borrower_collateral_detail.current_market_value))

            if loan_to_valuation_score == 0:
                self.rejection_reasons.append("Loan-to-valuation ratio exceeds 80%.")
                self.borrower_analysis_status = BorrowStatus.REJECTED
            total_facility_details_score = (
                    int(self.borrower_facility_details.type_of_facility_applying.value) + loan_to_valuation_score)
            if total_facility_details_score >= self.min_facility_score:
                self.borrower_analysis_status = BorrowStatus.REJECTED
            return total_facility_details_score
        return 0

    def calculate_score_and_update_status(self):
        # borrow details
        borrower_details_score = self.get_borrower_information_details_score()

        # financial details
        total_financial_details_score = self.get_financial_details_score()

        # collateral details
        total_collateral_details_score = self.get_collateral_details_score()

        # facility details
        total_facility_details_score = self.get_facility_details_score()

        self.total_credit_score = borrower_details_score + total_financial_details_score + total_collateral_details_score + total_facility_details_score
        if self.total_credit_score >= self.min_total_credit_score:
            self.borrower_analysis_status = BorrowStatus.REJECTED
        else:
            self.borrower_analysis_status = BorrowStatus.ACCEPTED

        return self.total_credit_score

    def get_rejection_results(self):
        return {"rejection_reasons": self.rejection_reasons}

    @staticmethod
    def display_section(section_title, details):
        print("=" * 50)
        print(f" {section_title} ".center(50, "="))
        for label, value in details.items():
            print(f"{label:<30}: {value}")
        print("-" * 50)

    def borrower_details_summary(self):
        details = {
            "Full Name": self.borrower_information_details.full_name,
            "Entity Type": entity_type_dic_name[self.borrower_information_details.entity_type],
            "Bank Status": client_bank_status_dic_name[self.borrower_information_details.bank_status],
            "Number of Guarantors": self.borrower_information_details.number_of_guarantors,
            "Age of Guarantors": self.borrower_information_details.age_of_guarantors,
            "Borrowing History": self.borrower_information_details.borrowing_history,
            "Borrower Score": self.get_borrower_information_details_score(),
        }
        self.display_section("Borrower Financial Analysis Summary", details)

    def financial_details_summary(self):
        details = {
            "Current Total Debt": locale.currency(self.borrower_financial_details.current_total_debt, grouping=True),
            "Gross Income": locale.currency(self.borrower_financial_details.gross_income, grouping=True),
            "Total Sales per Year": locale.currency(self.borrower_financial_details.total_sales_per_year,
                                                    grouping=True),
            "Debt to Income Ratio": f"{self.borrower_financial_details.debt_to_income_ratio:.2f}%",
            "Financial Score": self.get_financial_details_score(),
        }
        self.display_section("Financial Details", details)

    def collateral_details_summary(self):
        details = {
            "Current Market Value (CVM)": locale.currency(self.borrower_collateral_detail.current_market_value,
                                                          grouping=True),
            "Type of Property": property_type_dic_name[self.borrower_collateral_detail.type_of_property],
            "Location of Property": property_location_dic_name[
                self.borrower_collateral_detail.location_of_the_property],
            "Collateral Score": self.get_collateral_details_score(),
        }
        self.display_section("Collateral Details", details)

    def facility_details_summary(self):
        details = {
            "Type of Facility Applying": type_of_facility_applying_dic_name[
                self.borrower_facility_details.type_of_facility_applying],
            "Applied Loan Amount": locale.currency(self.borrower_facility_details.applied_loan_amount, grouping=True),
            "Loan to Valuation": f"{self.borrower_facility_details.loan_to_valuation:.2f}%",
            "Facility Score": self.get_facility_details_score(),
        }
        self.display_section("Facility Details", details)

    def loan_status(self):
        details = {
            "Loan Application Status": self.borrower_analysis_status.name,
        }
        result = {
            "Total Credit Analysis Score": self.total_credit_score
        }
        self.display_section("Status", details)
        self.display_section("Total Score", result)

    def display_credit_analysis_result(self):
        self.borrower_details_summary()
        self.financial_details_summary()
        self.collateral_details_summary()
        self.facility_details_summary()
        self.loan_status()


entity_type_dic_name = {EntityType.SOLE_PROPRIETORSHIP: "Solo Proprietorship",
                        EntityType.LIMITED_PARTNERSHIP: "Limited Partnership",
                        EntityType.COMPANY_LIMITED: "Company Limited"}

property_type_dic_name = {TypeProperty.RESIDENTIAL_LANDED: "Residential Landed",
                          TypeProperty.RESIDENTIAL_APARTMENT: "Residential Apartment",
                          TypeProperty.COMMERCIAL: "Commercial",
                          TypeProperty.OTHER: "other"}

property_location_dic_name = {LocationProperty.CENTRAL_AREA: "Central Area",
                              LocationProperty.URBAN: "Urban",
                              LocationProperty.SUBURBAN: "Suburban"}

current_property_status_dic_name = {CurrentPropertyStatus.UNDER_CONSTRUCTION: "Under construction",
                                    CurrentPropertyStatus.COMPLETED: "Completed"}

type_of_facility_applying_dic_name = {
    TypeFacilityApplying.REVOLVING_CREDIT: "Revolving credit",
    TypeFacilityApplying.TERM_LOAN: "Term loan"}

client_bank_status_dic_name = {
    ClientBankStatus.NEW_BANK: "New bank",
    ClientBankStatus.EXISTING_TO_A_BANK: "Existing to a bank"}

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
    return 0


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


# --------------------------------------- Input with exit option -------------------------------------------------------

class ReturnToMenu(Exception):
    """Exception to signal returning to the main menu."""
    pass


def input_with_exit_option(prompt, validation_func=None, error_message="Invalid input. Please try again."):
    while True:
        print("Type 'q' to return to the main menu.")  # Display option to quit
        user_input = input(prompt).strip()
        if user_input.lower() == "q":  # Quit option
            raise ReturnToMenu()
        if validation_func is None or validation_func(user_input):  # Validate input
            return user_input
        print(error_message)


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
    return input_with_exit_option(INPUT_FULL_NAME_MESSAGE, validate_full_name, INVALID_NAME_MESSAGE)


def input_borrower_borrowing_history() -> str:
    return input_with_exit_option(INPUT_BORROWER_HISTORY, validate_borrower_history, INVALID_BORROWER_HISTORY_MESSAGE)


def input_client_bank_status():
    result = input_with_exit_option(INPUT_CLIENT_BANK_STATUS, validate_client_bank_status_option,
                                    ERROR_MESSAGE_CLIENT_BANK_STATUS)
    return client_bank_status_dic[result]


def input_entity_type():
    result = input_with_exit_option(INPUT_ENTITY_TYPE, validate_entity_type, ERROR_MESSAGE_ENTITY_TYPE)
    return entity_type_dic[result]


def input_number_of_guarantors() -> int:
    return int(
        input_with_exit_option(INPUT_NUMBER_OF_GUARANTORS, validate_number_input, INVALID_NUMBER_GUARANTOR_MESSAGE))


def input_age_of_guarantors() -> int:
    return int(input_with_exit_option(INPUT_AGE_OF_GUARANTORS, validate_number_input, INVALID_NUMBER_GUARANTOR_MESSAGE))


def input_current_total_debt():
    return int(input_with_exit_option(INPUT_TOTAL_DEBT_MESSAGE, validate_number_input, INVALID_TOTAL_DEBT_MESSAGE))


def input_gross_income():
    return int(input_with_exit_option(INPUT_GROSS_INCOME_MESSAGE, validate_number_input, INVALID_TOTAL_INCOME_MESSAGE))


def input_applied_loan_amount():
    return int(
        input_with_exit_option(INPUT_APPLIED_LOAN_AMOUNT, validate_number_input, INVALID_APPLIED_LOAN_AMOUNT_MESSAGE))


def input_total_sales_per_year():
    return int(
        input_with_exit_option(INPUT_TOTAL_SALES_PER_YEAR, validate_number_input, INVALID_TOTAL_SALES_PER_YEAR_MESSAGE))


def input_current_market_value():
    return int(input_with_exit_option(INPUT_CURRENT_MARKET_VALUE, validate_number_input, INVALID_CURRENT_MARKET_VALUE))


def input_type_of_property():
    return property_type_dic[
        input_with_exit_option(INPUT_PROPERTY_TYPE, validate_property_type, INVALID_TYPE_PROPERTY_MESSAGE)]


def input_current_property_status():
    return current_property_status_dic[
        input_with_exit_option(INPUT_CURRENT_PROPERTY_STATUS, validate_property_status_input,
                               INVALID_TOTAL_SALES_PER_YEAR_MESSAGE)]


def input_location_of_property():
    return property_location_dic[input_with_exit_option(INPUT_PROPERTY_LOCATION_TYPE, validate_property_location,
                                                        INVALID_PROPERTY_LOCATION_TYPE_MESSAGE)]


def input_type_of_facility_applying():
    return type_of_facility_applying_dic[
        input_with_exit_option(INPUT_TYPE_OF_FACILITY_APPLYING, validate_type_of_facility_applying_input,
                               INVALID_TYPE_OF_FACILITY_APPLYING_MESSAGE)]


def get_debt_sales_ratio_score(debt_sales_ratio) -> int:
    if debt_sales_ratio > 70:
        return 0
    elif 60 <= debt_sales_ratio <= 70:
        return 4
    elif 50 <= debt_sales_ratio <= 59:
        return 3
    elif 40 <= debt_sales_ratio <= 49:
        return 3
    else:
        return 1


def get_to_income_ratio_score(debt_to_income_ratio) -> int:
    if debt_to_income_ratio > 55:
        return 0
    elif 35 <= debt_to_income_ratio <= 55:
        return 3
    elif debt_to_income_ratio < 35:
        return 1


def get_loan_to_valuation_ratio_score(loan_to_valuation_ratio) -> int:
    if loan_to_valuation_ratio > 80:
        return 0
    elif 60 <= loan_to_valuation_ratio <= 79:
        return 2
    elif loan_to_valuation_ratio < 60:
        return 1
    else:
        return 1


def get_debt_to_sales_ratio(current_total_debt, total_sales_per_year) -> float:
    if total_sales_per_year == 0:
        return 0.0
    return float(current_total_debt / total_sales_per_year) * 100


def get_loan_to_valuation_ratio(applied_loan_amount, current_market_value) -> float:
    if current_market_value == 0:
        return 0.0
    return float(applied_loan_amount / current_market_value) * 100


def get_debt_to_income_ratio(current_total_debt, gross_income) -> float:
    if gross_income == 0:
        return 0.0
    return float(current_total_debt / gross_income) * 100


# ----------------------------------------------------------------------------------------------------------------------

def analyze_borrow_information():
    try:
        print("\n--- Analyze Borrower Information ---")
        # Step 1: Borrower Details
        borrower, borrower_credit_analysis = process_borrower_details()

        if borrower_credit_analysis.borrower_analysis_status == BorrowStatus.REJECTED:
            display_rejection_reasons(borrower_credit_analysis)
            return

        # Step 2: Financial Details
        financial_borrower_details, borrower_credit_analysis = process_financial_details(borrower_credit_analysis)

        if borrower_credit_analysis.borrower_analysis_status == BorrowStatus.REJECTED:
            display_rejection_reasons(borrower_credit_analysis, include_financial=True)
            return

        # Step 3: Collateral Details
        collateral_detail, borrower_credit_analysis = process_collateral_details(borrower_credit_analysis)

        if borrower_credit_analysis.borrower_analysis_status == BorrowStatus.REJECTED:
            display_rejection_reasons(borrower_credit_analysis, include_collateral=True)
            return

        # Step 4: Facility Details
        borrower_credit_analysis = process_facility_details(collateral_detail, borrower_credit_analysis)

        # Step 5: Final Analysis and Result
        borrower_credit_analysis.display_credit_analysis_result()

    except ReturnToMenu:
        print("\nReturning to the main menu...\n")


def process_borrower_details():
    borrower_full_name, entity_type, client_bank_status, number_of_guarantors, age_of_guarantors, borrower_history = borrow_details()
    borrower = Borrower(
        borrower_full_name,
        entity_type,
        client_bank_status,
        number_of_guarantors,
        age_of_guarantors,
        borrower_history
    )
    borrower_credit_analysis = BorrowerCreditAnalysis(borrower)
    borrower_credit_analysis.get_borrower_information_details_score()
    return borrower, borrower_credit_analysis


def process_financial_details(borrower_credit_analysis):
    current_total_debt, gross_income, total_sales_per_year, debt_to_sales_ratio, debt_to_income_ratio = financial_details()
    financial_borrower_details = FinancialDetails(
        current_total_debt, gross_income, total_sales_per_year, debt_to_sales_ratio, debt_to_income_ratio
    )
    borrower_credit_analysis.borrower_financial_details = financial_borrower_details
    borrower_credit_analysis.get_financial_details_score()
    return financial_borrower_details, borrower_credit_analysis


def process_collateral_details(borrower_credit_analysis):
    current_market_value, type_of_property, current_property_status, location_of_property = collateral_details()
    collateral_detail = CollateralDetails(
        current_market_value, type_of_property, current_property_status, location_of_property
    )
    borrower_credit_analysis.borrower_collateral_detail = collateral_detail
    borrower_credit_analysis.get_collateral_details_score()
    return collateral_detail, borrower_credit_analysis


def process_facility_details(collateral_detail, borrower_credit_analysis):
    type_of_facility_applying, applied_loan_amount = facility_details()
    loan_to_valuation = get_loan_to_valuation_ratio(applied_loan_amount, collateral_detail.current_market_value)
    facility_detail = FacilityDetails(type_of_facility_applying, applied_loan_amount, loan_to_valuation)
    borrower_credit_analysis.borrower_facility_details = facility_detail
    borrower_credit_analysis.calculate_score_and_update_status()
    return borrower_credit_analysis


def display_rejection_reasons(borrower_credit_analysis, include_financial=False, include_collateral=False):
    borrower_credit_analysis.borrower_details_summary()
    if include_financial:
        borrower_credit_analysis.financial_details_summary()
    if include_collateral:
        borrower_credit_analysis.collateral_details_summary()

    if borrower_credit_analysis.get_rejection_results()['rejection_reasons']:
        print("Rejection Reasons:")
        for reason in set(borrower_credit_analysis.get_rejection_results()['rejection_reasons']):
            print(f"- {reason}")


def borrow_details():
    borrower_full_name = input_borrower_full_name()
    entity_type = input_entity_type()
    client_bank_status = input_client_bank_status()
    number_of_guarantors = input_number_of_guarantors()
    age_of_guarantors = input_age_of_guarantors()
    borrower_history = input_borrower_borrowing_history()
    return borrower_full_name, entity_type, client_bank_status, number_of_guarantors, age_of_guarantors, borrower_history


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


def display_help_menu():
    print("\n" + "=" * 50)
    print(" " * 15 + "HELP MENU")
    print("=" * 50)
    print("\nThis program is a comprehensive credit analysis tool designed to:")
    print("✔ Evaluate borrower creditworthiness.")
    print("✔ Analyze financial, collateral, and loan details.")
    print("\nKey Features:")
    print("- Borrower Details: Includes name, borrowing history, guarantors, and age verification.")
    print("- Financial Analysis: Calculates debt-to-income and debt-to-sales ratios.")
    print("- Collateral Evaluation: Assesses property type, value, and location.")
    print("- Loan Facility: Analyzes loan application types and loan-to-valuation ratios.")
    print("\nMenu Options:")
    print("1. Run Tests: Validates the program's functionality using pre-written unit tests.")
    print("2. Analyze Borrower Information: Guides you through entering:")
    print("   - Borrower Details")
    print("   - Financial Details")
    print("   - Collateral Details")
    print("   - Facility Details")
    print("3. Help: Displays this help menu with detailed guidance.")
    print("4. Exit: Closes the program.")
    print("\nTips:")
    print("- During data entry, type 'q' at any prompt to return to the main menu.")
    print("- Follow the on-screen instructions for accurate data entry.")
    print("\n" + "=" * 50)


def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Run Tests")
        print("2. Analyze Borrower Information")
        print("3. Help")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            run_tests()
        elif choice == "2":
            analyze_borrow_information()
        elif choice == "3":
            display_help_menu()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    print_header()
    main_menu()
