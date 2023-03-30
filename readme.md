# Financial Auditor

## Introduction

Financial Auditor is a simple command-line Python application that helps users manage their personal finances. With this tool, users can create and modify financial profiles, record and update debts, and generate debt payoff plans. The application also provides recommendations for budget allocation based on the popular 50/30/20 rule.

## Features

- Create and modify user profiles with basic financial data (name, age, salary, savings)
- Add, view, modify, and delete debts for each user
- Generate debt payoff plans based on user's salary, savings, and allocated payment for debts
- Calculate recommended budget allocation based on the 50/30/20 rule

## Requirements

- Python 3.x
- `tabulate` library (install with `pip install tabulate`)

## Usage

1. Clone or download the repository.
2. Open a terminal/command prompt and navigate to the directory containing the `financial_auditor.py` file.
3. Install the required library by running `pip install tabulate` if you haven't already.
4. Run the application with the command `python financial_auditor.py` or `python3 financial_auditor.py`, depending on your system's configuration.
5. Follow the prompts to create new users, modify existing users, manage debts, generate debt payoff plans, and calculate recommended budget allocations.

## Application Walkthrough

When you run the application, you'll be presented with three options:

1. Select an existing user
2. Create a new user
3. Exit

Choose an option by entering the corresponding number.

If you select an existing user or create a new one, you'll be presented with another menu:

1. Create a new debt
2. View existing debts
3. Modify an existing debt
4. Delete all debts
5. Debt payoff plan
6. Modify user data
7. 50/30/20 rule
8. Return to the main menu

Choose an action by entering the corresponding number and follow the prompts to perform the desired action.

To exit the application, return to the main menu and choose option 3 (Exit).

## Contributing

Feel free to create a fork of this repository, make improvements or add new features, and submit a pull request. We welcome your contributions and will review and consider any proposed changes.
