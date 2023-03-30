import csv
import os
import datetime
from tabulate import tabulate


# Read data from a CSV file and return a list of dictionaries

def read_csv(filename):
    if not os.path.isfile(filename):
        return []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# Write a dictionary of data to a CSV file


def write_to_csv(data, filename):
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Prompt the user to select an existing user and return the selected user's data


def select_existing_user(users):
    print("Select an existing user by entering the corresponding number:")
    for idx, user in enumerate(users):
        print(f"{idx + 1}. {user['name']}")

    user_index = int(input()) - 1
    return users[user_index]


# Create a new user with input from the user and save the user data to a CSV file

def create_new_user():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    salary = float(input("Enter your current salary: "))
    savings = float(input("Enter your current savings: "))

    user_data = {'name': name, 'age': age,
                 'salary': salary, 'savings': savings}
    write_to_csv(user_data, 'financial_data.csv')
    print("User created successfully.")

    debt_filename = f"{name}_debts.csv"
    if not os.path.isfile(debt_filename):
        with open(debt_filename, 'w', newline='') as csvfile:
            fieldnames = ['month', 'year', 'debtName',
                          'debtTotal', 'debtMonthlyPayment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    return user_data

# Create a new debt for the user and save it to a CSV file


def create_debt(user_name):
    debt_name = input("Enter the name of the debt: ")
    debt_total = float(input("Enter the total amount of the debt: "))
    debt_monthly_payment = float(
        input("Enter the monthly payment for the debt: "))
    month = int(input("Enter the starting month of the debt: "))
    year = int(input("Enter the starting year of the debt: "))

    debt_data = {
        'month': month,
        'year': year,
        'debtName': debt_name,
        'debtTotal': debt_total,
        'debtMonthlyPayment': debt_monthly_payment,
    }

    write_to_csv(debt_data, f"{user_name}_debts.csv")
    print("Debt added successfully.")

# Display a user's existing debts


def view_debts(user_name):
    debts = read_csv(f"{user_name}_debts.csv")

    if not debts:
        print("No debts found.")
        return

    print("Debts:")
    for debt in debts:
        print(f"{debt['debtName']} - Total: ${debt['debtTotal']} - Monthly Payment: ${debt['debtMonthlyPayment']} - Start: {debt['month']}/{debt['year']}")

# Modify an existing debt for a user and save the updated information to a CSV file


def modify_debt(user_name):
    # Read the user's debts from the corresponding CSV file
    debts = read_csv(f"{user_name}_debts.csv")

    # If there are no debts, print a message and return
    if not debts:
        print("No debts found.")
        return

    # Display the user's debts
    view_debts(user_name)

    # Prompt the user to select a debt to modify
    print("Select the debt you want to modify by entering the corresponding number:")
    for idx, debt in enumerate(debts):
        print(f"{idx + 1}. {debt['debtName']}")

    # Read the user's selection and get the corresponding debt from the list
    debt_index = int(input()) - 1
    selected_debt = debts[debt_index]

    # Prompt the user to enter updated information for the selected debt
    print("Enter the updated information for the selected debt:")
    new_debt_name = input(
        "Enter the new name of the debt (or leave blank to keep the current name): ")
    new_debt_total = input(
        "Enter the new total amount of the debt (or leave blank to keep the current amount): ")
    new_debt_monthly_payment = input(
        "Enter the new monthly payment for the debt (or leave blank to keep the current payment): ")
    new_month = input(
        "Enter the new starting month of the debt (or leave blank to keep the current month): ")
    new_year = input(
        "Enter the new starting year of the debt (or leave blank to keep the current year): ")

    # Update the selected debt's information based on user input
    if new_debt_name:
        selected_debt['debtName'] = new_debt_name
    if new_debt_total:
        selected_debt['debtTotal'] = new_debt_total
    if new_debt_monthly_payment:
        selected_debt['debtMonthlyPayment'] = new_debt_monthly_payment
    if new_month:
        selected_debt['month'] = new_month
    if new_year:
        selected_debt['year'] = new_year

    # Write the updated debts back to the CSV file
    with open(f"{user_name}_debts.csv", 'w', newline='') as csvfile:
        fieldnames = ['month', 'year', 'debtName',
                      'debtTotal', 'debtMonthlyPayment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for debt in debts:
            writer.writerow(debt)

    # Print a success message
    print("Debt updated successfully.")


# Delete all debts for a user and remove the corresponding CSV file

def delete_all_debts(user_name):
    if os.path.isfile(f"{user_name}_debts.csv"):
        os.remove(f"{user_name}_debts.csv")
        print("All debts have been deleted.")
    else:
        print("No debts found.")

# Generate a debt payoff plan based on the user's salary, savings, and allocated payment for debts


def debt_payoff_plan(user_name, salary, savings):
    # Read the user's debts from the corresponding CSV file
    debt_filename = f"{user_name}_debts.csv"
    debts = read_csv(debt_filename)

    # If there are no debts, print a message and return
    if not debts:
        print("No debts found for this user.")
        return

    # Prompt the user for the necessary input data
    current_month = int(input("Enter the current month: "))
    current_year = int(input("Enter the current year: "))
    allocated_payment = float(
        input("Enter the amount you want to allocate to paying your debts: "))
    expenses = float(input("Enter the amount you need for other expenses: "))

    # Calculate the total debt and initialize remaining_debt
    total_debt = sum(float(debt['debtTotal']) for debt in debts)
    remaining_debt = total_debt
    # Initialize the list to store the debt payoff plan
    table_rows = []

    # Calculate the debt payoff plan until all debt is paid off
    while remaining_debt > 0:
        # Create a date object for the current month and year
        date = datetime.date(current_year, current_month, 1)
        # Calculate the available payment after accounting for expenses
        available_payment = salary - expenses
        # Determine the amount to be paid towards the debt this month
        debt_payment = min(
            remaining_debt, allocated_payment, available_payment)
        # Update the remaining debt and savings
        remaining_debt -= debt_payment
        savings += (salary - debt_payment - expenses)

        # Add the current month's data to the table rows
        table_rows.append([
            date,
            f"${debt_payment:.2f}",
            f"${remaining_debt:.2f}",
            f"${savings:.2f}"
        ])

        # Update the current month and year for the next iteration
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

    # Print the debt payoff plan in a table format
    headers = ["Date", "Debt Payment", "Remaining Debt", "Savings"]
    print(tabulate(table_rows, headers=headers, tablefmt='grid'))

    payoff_filename = f"{user_name}_payoff_plan.csv"
    with open(payoff_filename, 'w', newline='') as csvfile:
        fieldnames = ['date', 'debtPayment', 'remainingDebt', 'savings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in table_rows:
            writer.writerow({
            'date': entry[0],
            'debtPayment': entry[1],
            'remainingDebt': entry[2],
            'savings': entry[3]
            })


    # Print a success message
    print("Debt payoff plan generated successfully.")


# Update a user's data (name, age, salary, and savings) and save the updated information to a CSV file

def modify_user_data(selected_user, users):
    print("Enter the updated information for the selected user:")
    new_name = input(
        "Enter the new name (or leave blank to keep the current name): ")
    new_age = input(
        "Enter the new age (or leave blank to keep the current age): ")
    new_salary = input(
        "Enter the new salary (or leave blank to keep the current salary): ")
    new_savings = input(
        "Enter the new savings (or leave blank to keep the current savings): ")

    if new_name:
        selected_user['name'] = new_name
    if new_age:
        selected_user['age'] = new_age
    if new_salary:
        selected_user['salary'] = new_salary
    if new_savings:
        selected_user['savings'] = new_savings

    with open('financial_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'age', 'salary', 'savings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow(user)

    print("User data updated successfully.")


# Calculate the recommended budget allocation based on the 50/30/20 rule

def calculate_50_30_20(salary):
    needs = salary * 0.50
    wants = salary * 0.30
    savings_and_debts = salary * 0.20

    print("\nBased on the 50/30/20 rule, you should distribute your salary as follows:")
    print(f"1. Needs and obligations (50%): ${needs:.2f}")
    print(f"2. Wants and leisure (30%): ${wants:.2f}")
    print(f"3. Savings and debt repayment (20%): ${savings_and_debts:.2f}\n")

    print("The rule states that you should spend up to 50% of your after-tax income on needs and obligations that you must-have or must-do. The remaining half should be split up between 20% savings and debt repayment and 30% to everything else that you might want.")


# Main menu function for the Financial Auditor program

def main_menu():
    while True:
        print("Welcome to the Financial Auditor!")
        print("Please choose an option:")
        print("1. Select an existing user")
        print("2. Create a new user")
        print("3. Exit")

        choice = int(input())

        if choice == 1:
            users = read_csv('financial_data.csv')
            if not users:
                print("No users found. Please create a new user.")
                continue

            selected_user = select_existing_user(users)
            print(f"You have selected {selected_user['name']}")

            while True:
                print("Select an action:")
                print("1. Create a new debt")
                print("2. View existing debts")
                print("3. Modify an existing debt")
                print("4. Delete all debts")
                print("5. Debt payoff plan")
                print("7. 50/30/20 rule")
                print("8. Return to main menu")

                action = int(input())

                if action == 1:
                    create_debt(selected_user['name'])
                elif action == 2:
                    view_debts(selected_user['name'])
                elif action == 3:
                    modify_debt(selected_user['name'])
                elif action == 4:
                    delete_all_debts(selected_user['name'])
                elif action == 5:
                    debt_payoff_plan(selected_user['name'], float(
                        selected_user['salary']), float(selected_user['savings']))
                elif action == 6:
                    modify_user_data(selected_user, users)
                elif action == 7:
                    calculate_50_30_20(float(selected_user['salary']))
                elif action == 8:
                    break
                else:
                    print("Invalid action. Please try again.")

        elif choice == 2:
            create_new_user()
        elif choice == 3:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
