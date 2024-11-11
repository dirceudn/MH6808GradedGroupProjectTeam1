def get_collateral_details():   
    def get_property_type():
        prompt = '''
        Please select a property type:
        (1) Residential Landed
        (2) Residential Apartment
        (3) Commercial
        (4) Others

        Enter the number corresponding to your choice (1-4):
        '''
        property_types = {
            1: "Residential Landed",
            2: "Residential Apartment",
            3: "Commercial",
            4: "Others"
        }
        # Check for invalid inputs
        while True:
                try:
                    choice = int(input(prompt))
                    if choice in [1, 2, 3, 4]:
                        return choice
                    else:
                        print("Invalid input. Please enter a number between 1 and 4.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        return choice 

    def get_property_location():
        prompt = '''
        Please select a property type:
        (1) Central Area
        (2) Urban
        (3) Suburban

        Enter the number corresponding to your choice (1-3):
        '''
        location_map = {
            1: "Central Area",
            2: "Urban",
            3: "Suburban"
        }

        while True:
            try:
                choice = int(input(prompt))
                if choice in location_map:
                    print(f"You have selected {location_map[choice]}")
                    return choice
                else:
                    print("Invalid input. Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_property_status():
        prompt = '''
        Please select current property status:
        (1) Under construction
        (2) Completed

        Enter the number corresponding to your choice (1 or 2):
        '''
        #Check for invalid inputs
        while True:
            try:
                choice = int(input(prompt))
                if choice == 1:
                    status = False
                    print("Construction Status: Under Construction")
                    return status
                elif choice == 2:
                    status = True
                    print("Construction Status: Completed")
                    return status
                else:
                    print("Invalid input. Please enter 1 for Under Construction or 2 for Completed.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    #Sum up score based on user inputs
    score = get_property_type()
    score += get_property_location()

    #Check score to determine BorrowStatus
    if score >= 7:
        BorrowStatus = False
    else:
        BorrowStatus = get_property_status()

    print(score)
    print(BorrowStatus)
    return score, BorrowStatus