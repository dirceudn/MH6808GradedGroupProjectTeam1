# Financial details by Melani

def evaluate_loan_application_by_debt_sales_ratio():
    # Prompt user inputs for total debt and sales, converted to integers
    current_total_debt = int(input("Enter total debt amount: "))
    gross_sales = int(input("Enter total sales amount: "))
    
    # Calculate debt-to-sales ratio
    debt_to_sales_ratio = (current_total_debt / gross_sales) * 100
    print(f"Debt to Sales Ratio: {debt_to_sales_ratio:.2f}%")
    
    # Define debt-to-sales ratio scoring
    if debt_to_sales_ratio > 70:
        Loan_Application_Result_score = "Reject"  # Immediate rejection if DSR > 70%
    elif 60 <= debt_to_sales_ratio <= 69:
        Loan_Application_Result_score = 4
    elif 50 <= debt_to_sales_ratio <= 59:
        Loan_Application_Result_score = 3
    elif 40 <= debt_to_sales_ratio <= 49:
        Loan_Application_Result_score = 2
    else:  # debt_to_sales_ratio < 40
        Loan_Application_Result_score = 1
    
    # Output the result
    print(f"Loan Application Result Score by Debt-to-Sales Ratio: {Loan_Application_Result_score}")


def evaluate_loan_application_by_debt_income_ratio():
    # Prompt user inputs for total debt and income, converted to integers
    current_total_debt = int(input("Enter total debt amount: "))
    gross_income = int(input("Enter income amount: "))
    
    # Calculate debt-to-income ratio
    debt_to_income_ratio = (current_total_debt / gross_income) * 100
    print(f"Debt to Income Ratio: {debt_to_income_ratio:.2f}%")
    
    # Define debt-to-income ratio scoring
    if debt_to_income_ratio > 55:
        Loan_Application_Result_score = "Reject"  # Immediate rejection if DIR > 55%
    elif 35 <= debt_to_income_ratio < 55:
        Loan_Application_Result_score = 3
    else:  # debt_to_income_ratio < 35
        Loan_Application_Result_score = 1
    
    # Output the result
    print(f"Loan Application Result Score by Debt-to-Income Ratio: {Loan_Application_Result_score}")


# Example usage
evaluate_loan_application_by_debt_sales_ratio()
evaluate_loan_application_by_debt_income_ratio()
