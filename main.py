def main():
    print("MH6808 Graded Group Project Team1")

if __name__ == "__main__":
    main()


#Facility Details Evaluation_Kelvin
def evaluate_loan_application_by_ltv(facility_type, loan_to_valuation):
    # Define scores based on facility type
    if facility_type == 'Revolving Credit':
        facility_score = 2
    elif facility_type == 'Term Loan':
        facility_score = 1
    else:
        return "Invalid facility type."

    # Define scores based on loan to valuation ratio
    if loan_to_valuation > 80:
        return "Reject"  # Immediate rejection if LTV is greater than 80%
    elif 60 <= loan_to_valuation <= 79:
        ltv_score = 2  # Moderate risk
    else:  # Below 60%
        ltv_score = 1  # Lower risk

    # Calculate total score
    total_score = facility_score + ltv_score

    # Determine acceptance or rejection based on total score
    if total_score < 4:
        return "Accept"
    else:
        return "Reject"

def evaluate_loan_application(facility_type, applied_loan_amount, current_market_value):
    # Check to avoid division by zero
    if current_market_value <= 0:
        return "Current market value must be greater than zero."

    # Calculate loan to valuation ratio (LTV)
    loan_to_valuation = (applied_loan_amount / current_market_value) * 100

    # Call the evaluation function based on LTV
    return evaluate_loan_application_by_ltv(facility_type, loan_to_valuation)

# Example usage
facility_type = input("Enter the type of facility (Revolving Credit/Term Loan): ")
applied_loan_amount = float(input("Enter the applied loan amount: "))
current_market_value = float(input("Enter the current market value: "))

result = evaluate_loan_application(facility_type, applied_loan_amount, current_market_value)
print(f"Loan Application Result: {result}")

