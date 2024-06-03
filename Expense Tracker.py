
# This one was tough, let me know if I went wrong anywhere.
# I learnt about ASCII art and adding color to python terminal output, but opted to not use it for now.
# This task helped me understand functions a lot more.
# I see lots of improvements I can continue making and will do so for my coding portfolio
# Took a week off work to do this, 
# If errors are found let me know soonest, otherwise kindly advise on the next step.


#=====Importing Libraries=====

import sqlite3
import time
from datetime import datetime


#=====Create Functions=====

# Display the full table
def table():
    table_spacing = " {:<3} | {:<10} | {:<15} | {:<20} | {:<10} | {:<10}"
    print(table_spacing.format("ID", "Date", "Category", "Description", "Amount", "Remaining"))
    print("-" * 95)
    cursor.execute('''
        SELECT ID, Date, Category, Description, Amount, Remaining
        FROM Expenses''')
    rows = cursor.fetchall()
    for row in rows:
        print(table_spacing.format(
            row[0], row[1], row[2], row[3], row[4], row[5]))


# Expense Functions:
# Display the expense records in the table
def table_expenses():
    table_spacing = " {:<3} | {:<10} | {:<15} | {:<20} | {:<10} | {:<10}"
    print(table_spacing.format("ID", "Date", "Category", "Description", "Amount", "Remaining"))
    print("-" * 95)
    cursor.execute('''
        SELECT ID, Date, Category, Description, Amount, Remaining
        FROM Expenses
        WHERE Amount < 0''')
    rows = cursor.fetchall()
    for row in rows:
        print(table_spacing.format(
            row[0], row[1], row[2], row[3], row[4], row[5]))

# Checks if specified expense category is a valid expense, then displays those records
def table_expenses_category():
    while True:
        Category = input("Enter the expense category to display: ").capitalize()
        cursor.execute('''
            SELECT ID, Date, Category, Description, Amount, Remaining
            FROM Expenses
            WHERE Category = ? AND Amount < 0''', (Category,))
        rows = cursor.fetchall()
        if rows:
            table_spacing = " {:<3} | {:<10} | {:<15} | {:<20} | {:<10} | {:<10}"
            print(table_spacing.format("ID", "Date", "Category", "Description", "Amount", "Remaining"))
            print("-" * 95)
            for row in rows:
                print(table_spacing.format(
                    row[0], row[1], row[2], row[3], row[4], row[5]))
            break
        elif Category == 'Back':
            break
        else:
            print("Invalid category or no expenses found for this category. Please try again or type 'Back'.\n")

# Checks if ID provided matches an expense record
def valid_expense_record():
    while True:
        ID = valid_int_input("Provide the record ID: ")
        cursor.execute('''
            SELECT COUNT(*)
            FROM Expenses
            WHERE ID = ? AND Amount < 0''', (ID,))
        if cursor.fetchone()[0] > 0:
            return ID
        elif ID == 'Back':
            break
        else:
            print("Invalid record ID or no expenses found for this ID. Please try again or type 'Back'.\n")


# Income Functions:
# Display the income records in the table
def table_income():
    table_spacing = " {:<3} | {:<10} | {:<15} | {:<20} | {:<10} | {:<10}"
    print(table_spacing.format("ID", "Date", "Category", "Description", "Amount", "Remaining"))
    print("-" * 95)
    cursor.execute('''
        SELECT ID, Date, Category, Description, Amount, Remaining
        FROM Expenses
        WHERE Amount > 0''')
    rows = cursor.fetchall()
    for row in rows:
        print(table_spacing.format(
            row[0], row[1], row[2], row[3], row[4], row[5]))

# Checks if specified income category is a valid income, then displays those records
def table_income_category():
    while True:
        Category = input("Enter the income category to display: ").capitalize()
        cursor.execute('''
            SELECT ID, Date, Category, Description, Amount, Remaining
            FROM Expenses
            WHERE Category = ? AND Amount > 0''', (Category,))
        rows = cursor.fetchall()
        if rows:
            table_spacing = " {:<3} | {:<10} | {:<15} | {:<20} | {:<10} | {:<10}"
            # Prints the expenses table, and handles the budget None
            print(table_spacing.format("ID", "Date", "Category", "Description", "Amount", "Remaining"))
            print("-" * 95)
            for row in rows:
                print(table_spacing.format(
                    row[0], row[1], row[2], row[3], row[4], row[5]))
            break
        elif Category == 'Back':
            break
        else:
            print("Invalid category or no income found for this category. Please try again or type 'Back'.\n")

# Checks if ID provided matches an income record
def valid_income_record():
    while True:
        ID = valid_int_input("Provide the record ID: ")
        cursor.execute('''
            SELECT COUNT(*)
            FROM Expenses
            WHERE ID = ? AND Amount > 0''', (ID,))
        if cursor.fetchone()[0] > 0:
            return ID
        elif ID == 'Back':
            break
        else:
            print("Invalid record ID or no income found for this ID. Please try again or type 'Back'.\n")


# Budget Functions:
# Display full budget and amount spent per category table
def table_budget():
    cursor.execute('''
        SELECT DISTINCT Category, Budget
        FROM Expenses
        WHERE Budget IS NOT NULL''')
    rows = cursor.fetchall()
    if rows:
        table_spacing = " {:<15} | {:<10} | {:<15}"
        # Prints the category, budget, and total amount spent
        print(table_spacing.format("Category", "Budget", "Total Spent"))
        print("-" * 45)
        for row in rows:
            category = row[0]
            budget = row[1]
            # Calculate the total amount spent for the category
            cursor.execute('''
                SELECT SUM(Amount)
                FROM Expenses
                WHERE Category = ? AND Amount < 0''', (category,))
            total_spent = cursor.fetchone()[0] or 0
            total_spent *= -1 # Changes to positive value
            print(table_spacing.format(
                category, budget if budget is not None else 'NULL', f"{total_spent:.2f}"))
    else:
        print("No categories with a budget found.")

# Checks if specified category has a budget, then displays Budget and total spent for category
def table_budget_category():
    while True:
        Category = input("Enter the category to display the budget for: ").capitalize()
        cursor.execute('''
            SELECT COUNT(*)
            FROM Expenses
            WHERE Category = ? AND Budget IS NOT NULL''', (Category,))
        if cursor.fetchone()[0] > 0:
            # Fetch the budget for the category, DISTINCT will avoid duplicates
            cursor.execute('''
                SELECT DISTINCT Category, Budget
                FROM Expenses
                WHERE Category = ? AND Budget IS NOT NULL''', (Category,))
            rows = cursor.fetchall()
            # Calculate the total amount spent for the category
            cursor.execute('''
                SELECT SUM(Amount)
                FROM Expenses
                WHERE Category = ? AND Amount < 0''', (Category,))
            total_spent = cursor.fetchone()[0] or 0
            total_spent *= -1 # Changes to positive value
            table_spacing = " {:<15} | {:<10} | {:<15}"
            # Prints the category, budget, and total amount spent
            print(table_spacing.format("Category", "Budget", "Total Spent"))
            print("-" * 45)
            for row in rows:
                print(table_spacing.format(
                    row[0], row[1] if row[1] is not None else 'NULL', f"{total_spent:.2f}"))
            break
        elif Category == 'Back':
            break
        else:
            print("Invalid category or no budget found for this category. Please try again or type 'Back'.\n")

# Checks if category provided is valid and has a budget
def valid_budget_category():
    while True:
        Category = input("Enter the category to check the budget for: ").capitalize()
        cursor.execute('''
            SELECT DISTINCT Budget
            FROM Expenses
            WHERE Category = ? AND Budget IS NOT NULL''', (Category,))
        if cursor.fetchone():
            return Category
        elif Category == 'Back':
            break
        else:
            print("Invalid category or no budget found for this category. Please try again or type 'Back'.\n")


# Financial Goals Functions:
# Function to get the remaining amount of the last expense record
def get_last_expense_remaining():
    cursor.execute('''
        SELECT Remaining
        FROM Expenses
        LIMIT 1
    ''')
    return cursor.fetchone()[0]

# Function to display financial goals with progress
def table_financial_goals():
    # Prints the table header
    print(" {:<15} | {:<10} | {:<15}".format("Goal", "Cost", "Amount Available"))
    print("-" * 45)
    cursor.execute('''
        SELECT GoalDescription, GoalCost
        FROM FinancialGoals
    ''')
    rows = cursor.fetchall()
    for row in rows:
        goal_description = row[0]
        goal_cost = row[1]
        Amount_Available = goal_cost - get_last_expense_remaining()
        print(" {:<15} | {:<10} | {:<15}".format(goal_description, goal_cost, Amount_Available))


# Automatic Remaining Updaters:
# Decrease remaining (Expense)
def reduce_remaining(cursor, amount):
    cursor.execute('''
        SELECT Remaining 
        FROM Expenses 
        ORDER BY ID 
        DESC LIMIT 1''')
    row = cursor.fetchone()
    previous_remaining = row[0] if row else 0
    new_remaining = previous_remaining - amount
    return new_remaining

# Increase remaining (Income)
def increase_remaining(cursor, amount):
    cursor.execute('''
        SELECT Remaining 
        FROM Expenses 
        ORDER BY ID 
        DESC LIMIT 1''')
    row = cursor.fetchone()
    previous_remaining = row[0] if row else 0
    new_remaining = previous_remaining + amount
    return new_remaining


# Input Type error checks:
# Checks if date input is in correct format
def valid_date_input(prompt):
    while True:
        date_input = input(prompt)
        try:
            datetime.strptime(date_input, '%Y-%m-%d')
            return date_input
        except ValueError:
            print("Please enter a valid date in the format YYYY-MM-DD, example: 2024-01-21.")

# Checks if float (Amount) input is in correct format
def valid_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

# Checks if integer input is in correct format
def valid_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


#=====Foundation=====

try:
    # Creates/connects to a database file called 'Expense Tracker.db' and creates a cursor object
    db = sqlite3.connect('Expense Tracker.db')
    cursor = db.cursor()

    # Creates an empty table called 'Expenses'
    # Catagories: ID, Date, Category, Description, Budget, Amount, Remaining
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Expenses (
        ID INTEGER PRIMARY KEY,
        Date DATE NOT NULL,
        Category TEXT NOT NULL,
        Description TEXT NOT NULL,
        Budget NUMERIC,
        Amount NUMERIC NOT NULL,
        Remaining NUMERIC)
    ''')
    db.commit()

    # Inserts starting records into the table
    # Date is YYYY-MM-DD
    # Check if any records exist in the Expenses table
    # Insert starting records only if the table is empty
    starting_records = [
        (1, '2024-05-01', 'Income', 'Monthly Salary', None, 10000.00, 10000.00),
        (2, '2024-05-01', 'Housing', 'Rent and utilities', None, -4500.00, 5500.00),
        (3, '2024-05-01', 'Housing', 'Internet', None, -350.00, 5150.00),
        (4, '2024-05-01', 'Transportation', 'Public bus', None, -400.00, 4750.00),
        (5, '2024-05-01', 'Food', 'Monthly Groceries', None, -2000.00, 2750.00)
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Expenses(ID, Date, Category, Description, Budget, Amount, Remaining) 
        VALUES (?, ?, ?, ?, ?, ?, ?)''', starting_records)
    db.commit()

    # Secondary table just for Financial Goals
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FinancialGoals (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        GoalDescription TEXT NOT NULL,
        GoalCost NUMERIC NOT NULL)
    ''')
    db.commit()


#=====Menu Section=====

    # Main menu loop, requesting user input
    print("    Welcome to the Expense Tracker App!")
    while True:
        menu = input('''
    MAIN MENU
-----------------------------------------------
    Select one of the following options:

    1   - Expenses
    2   - Income
    3   - Budget
    4   - Financial Goals
    5   - Quit

    Type 'Show' to display the full Expense+Income table.
    Selection: ''').lower()

        # Shows full Income + Expense Table
        if menu in ['s', 'show']:
            print("\n\n")
            table()
            print("")


        # Shows Expense submenu
        elif menu in ['1', 'e', 'expenses']:
            while True:
                submenu = input('''\n\n\n\n
    EXPENSES SUBMENU
-----------------------------------------------
    Select one of the following options:

    1   - Add expense
    2   - View expenses
    3   - View expenses by category
    4   - Update expense
    5   - Delete expense
    6   - Back

    Selection: ''').lower()

                # Allows adding new expense records
                if submenu in ['1', 'a', 'add', 'add expense']:
                    print("\n\n")
                    table()
                    print("\n\nThis is to add a new expense: \n")

                    Date = valid_date_input("Date (YYYY-MM-DD, example: 2024-01-20): ")
                    Category = input("Expense Category: ").capitalize()
                    Description = input("Short Description: ").capitalize()
                    Amount = valid_float_input("Total Amount: ")
                    Remaining = reduce_remaining(cursor, Amount)
                    Amount *= -1 # Turn into a negative value

                    cursor.execute('''
                        INSERT INTO Expenses(Date, Category, Description, Amount, Remaining)
                        VALUES(?, ?, ?, ?, ?)''', (Date, Category, Description, Amount, Remaining))
                    db.commit()
                    print("Successfully added a new expense in the %s Category: R%.2f for %s on %s" % (Category, Amount, Description, Date))
                    print("\n")

                # Display expenses table
                elif submenu in ['2', 'v', 'view expenses']:
                    print("\n\n")
                    table_expenses()
                    print("\n")
                    break

                # Display expenses table by category
                elif submenu in ['3', 'category']:
                    print("\n\n")
                    table_expenses_category()
                    print("\n")
                    break

                # Allows user to update an expense record based on Expense 'ID' input
                elif submenu in ['4', 'up', 'update', 'update expense']:
                    print("\nThese questions are pertaining to an existing expense.\n")
                    update = input("Do you want to update the Date, Category, Description or Amount: ").capitalize()
                    if update == "Date":
                        ID = valid_expense_record()
                        Date = valid_date_input("Date (YYYY-MM-DD, example: 2024-01-20): ")
                        cursor.execute('''
                            UPDATE Expenses
                            SET Date = ?
                            WHERE ID = ?''', (Date, ID))
                        db.commit()
                        print("Successfully updated the record ID: %d date to %s." % (ID, Date))

                    # Update expense Category
                    elif update == "Category":
                        ID = valid_expense_record()
                        Category = input("Please confirm the new category: ").capitalize()
                        cursor.execute('''
                            UPDATE Expenses
                            SET Category = ?
                            WHERE ID = ?''', (Category, ID))
                        db.commit()
                        print("Successfully updated the record ID: %d category to %s." % (ID, Category))

                    # Update expense Description
                    elif update == "Description":
                        ID = valid_expense_record()
                        Description = input("Please confirm the new description: ")
                        cursor.execute('''
                            UPDATE Expenses
                            SET Description = ?
                            WHERE ID = ?''', (Description, ID))
                        db.commit()
                        print("Successfully updated the record ID: %d description to %s." % (ID, Description))

                    # Update expense Amount
                    elif update == "Amount":
                        ID = valid_expense_record()
                        Amount = valid_float_input("Please confirm the new amount: ")
                        Amount *= -1 # Turn into a negative value
                        cursor.execute('''
                            UPDATE Expenses
                            SET Amount = ?
                            WHERE ID = ?''', (Amount, ID))
                        db.commit()
                        print("Successfully updated the record ID: %d amount to R%.2f." % (ID, Amount))
                    else:
                        print("That's an invalid input. Please try: Date, Category, Description or Amount.")

                # Allows user to delete a record from the database based on book 'ID'
                elif submenu in ['5', 'del', 'delete', 'delete expense']:
                    print("\nThis will delete the expense record.\n")
                    ID = valid_int_input("Please provide the expense record ID: ")
                    cursor.execute('''
                        DELETE FROM Expenses
                        WHERE ID = ?''', (ID,))
                    db.commit()
                    print("Successfully deleted the ID: %d expense record." % ID)

                # Back to main menu
                elif submenu in ['6', 'b', 'back']:
                    print("\n\n\n\n")
                    break


        # Displays the Income submenu
        elif menu in ['2', 'i', 'income']:
            while True:
                submenu = input('''\n\n\n\n
    INCOME SUBMENU
-----------------------------------------------
    Select one of the following options:

    1   - Add income
    2   - View income
    3   - View income by category
    4   - Update income
    5   - Delete income
    6   - Back

    Selection: ''').lower()

                # Allows adding new income records
                if submenu in ['1', 'a', 'add', 'add income']:
                    print("\n\n")
                    table()
                    print("\n\nThis is to add a new income record: \n")

                    Date = valid_date_input("Date (YYYY-MM-DD, example: 2024-01-20): ")
                    Category = input("Income Category: ").capitalize()
                    Description = input("Short Description: ").capitalize()
                    Amount = valid_float_input("Total Amount: ")
                    Remaining = increase_remaining(cursor, Amount)

                    cursor.execute('''
                        INSERT OR IGNORE INTO Expenses(Date, Category, Description, Amount, Remaining)
                        VALUES(?, ?, ?, ?, ?)''', (Date, Category, Description, Amount, Remaining))
                    db.commit()
                    print("Successfully added new earnings in the %s Category: R%.2f for %s on %s" % (Category, Amount, Description, Date))
                    print("\n")
                    break

                # Display income table
                elif submenu in ['2', 'v', 'view income']:
                    print("\n\n")
                    table_income()
                    print("\n")
                    break

                # Display income table by category
                elif submenu in ['3', 'category']:
                    print("\n\n")
                    table_income_category()
                    print("\n")
                    break

                # Allows user to update an income record based on Expense 'ID' input
                elif submenu in ['4', 'up', 'update', 'update income']:
                    print("\nThese questions are pertaining to an existing income.\n")
                    update = input("Do you want to update the Date, Category, Description or Amount? ").capitalize()

                    # Update an income record Date
                    if update == "Date":
                        ID = valid_income_record()
                        Date = valid_date_input("Date (YYYY-MM-DD, example: 2024-01-20): ")
                        cursor.execute('''
                            UPDATE Expenses
                            SET Date = ?
                            WHERE ID = ?''', (Date, ID))
                        db.commit()
                        print("Successfully updated the record ID: %d date to %s." % (ID, Date))

                    # Update an income record Category
                    elif update == "Category":
                        ID = valid_income_record()
                        Category = input("Please confirm the new category: ").capitalize()
                        cursor.execute('''
                            UPDATE Expenses
                            SET Category = ?
                            WHERE ID = ?''', (Category, ID))
                        db.commit()
                        print("Successfully updated the record ID: %d category to %s." % (ID, Category))

                    # Update an income record Description
                    elif update == "Description":
                        ID = valid_income_record()
                        Description = input("Please confirm the new description: ")
                        cursor.execute('''
                            UPDATE Expenses
                            SET Description = ?
                            WHERE ID = ?''', (Description, ID))
                        db.commit()
                        print("Successfully updated the record ID: %d description to %s." % (ID, Description))

                    # Update an income record Amount
                    elif update == "Amount":
                        ID = valid_income_record()
                        Amount = valid_float_input("Please confirm the new amount: ")
                        cursor.execute('''
                            UPDATE Expenses
                            SET Amount = ?
                            WHERE ID = ?''', (Amount, ID))
                        db.commit()
                        print("Successfully updated the record ID: %d amount to R%.2f." % (ID, Amount))
                    else:
                        print("That's an invalid input. Please try: Date, Category, Description or Amount.")

                # Allows user to delete a record from the database based on book 'ID'
                elif submenu in ['5', 'del', 'delete', 'delete income']:
                    print("\nThis will delete the income record.\n")
                    ID = valid_int_input("Please provide the income record ID: ")
                    cursor.execute('''
                        DELETE FROM Expenses
                        WHERE ID = ?''', (ID,))
                    db.commit()
                    print("Successfully deleted the ID: %d income record." % ID)

                # Back to main menu
                elif submenu in ['6', 'b', 'back']:
                    print("\n\n\n\n")
                    break


        # Displays the Budget submenu
        elif menu in ['3', 'b', 'budget']:
            while True:
                submenu = input('''\n\n\n\n
    BUDGET SUBMENU
-----------------------------------------------
    Select one of the following options:

    1   - Set budget for category
    2   - View budget
    3   - View budget for category
    4   - Update budget for category
    5   - Clear budget for category
    6   - Back

    Selection: ''').lower()

                # Allows adding new budget for a category
                if submenu in ['1', 's', 'set', 'set budget']:
                    print("\n\n")
                    # Checks if specified category exists, then allows user to set a budget for it
                    while True:
                        Category = input("Enter the category to set the budget for: ").capitalize()
                        cursor.execute('''
                            SELECT COUNT(*)
                            FROM Expenses
                            WHERE Category = ?''', (Category,))
                        if cursor.fetchone()[0] > 0:
                            Budget = valid_float_input(f"Enter the budget for the {Category} category: ")
                            cursor.execute('''
                                UPDATE Expenses
                                SET Budget = ?
                                WHERE Category = ?''', (Budget, Category))
                            db.commit()
                            print("Successfully updated the Budget for the %s Category to R%.2f" % (Category,  Budget))
                            print("\n")
                            break
                        elif Category == 'Back':
                            break
                        else:
                            print("Invalid category. Please try again or type 'Back'.\n")
                    print("\n")
                    break

                # Display budget table
                elif submenu in ['2', 'v', 'view budget']:
                    print("\n\n")
                    table_budget()
                    print("\n")
                    break

                # Display budget table by category
                elif submenu in ['3', 'view category']:
                    print("\n\n")
                    table_budget_category()
                    print("\n")
                    break
                    # needs to ask user which category to check

                elif submenu in ['4', 'up', 'update', 'update budget']:
                    Category = valid_budget_category()
                    Budget = valid_float_input(f"Enter the new budget for the {Category} category: ")
                    cursor.execute('''
                        UPDATE Expenses
                        SET Budget = ?
                        WHERE Category = ? AND Budget IS NOT NULL''', (Budget, Category))
                    db.commit()
                    print("Successfully updated the Budget for the %s Category to R%.2f." % (Category, Budget))

                # Allows user to clear the budget for a specific category
                elif submenu in ['5', 'clear', 'clear budget']:
                    print("\nThis will clear the budget for the specified category.\n")
                    Category = input("Please provide the category to clear the budget for: ").capitalize()
                    cursor.execute('''
                        UPDATE Expenses
                        SET Budget = NULL
                        WHERE Category = ?''', (Category,))
                    db.commit()
                    print("Successfully cleared the budget for the %s category." % Category)

                # Back to main menu
                elif submenu in ['6', 'b', 'back']:
                    print("\n\n\n\n")
                    break


        # Displays the Financial Goals submenu
        elif menu in ['4', 'f', 'goals', 'financial goals']:
            while True:
                submenu = input('''\n\n\n\n
    FINANCIAL GOALS SUBMENU
-----------------------------------------------
    Select one of the following options:

    1   - Set financial goals
    2   - Update financial goals
    3   - View progress towards financial goals
    4   - Back

    Selection: ''').lower()

                # Allows adding a new financial goal
                if submenu in ['1', 's', 'set', 'set goals']:
                    print("\n")
                    goal_description = input("Describe the goal: ").capitalize()
                    goal_cost = valid_float_input("How much money is needed: ")
                    cursor.execute('''
                        INSERT INTO FinancialGoals (GoalDescription, GoalCost)
                        VALUES (?, ?)''', (goal_description, goal_cost))
                    db.commit()
                    print("Successfully added a new financial goal for %s with a cost of R%.2f." % (goal_description, goal_cost))
                    print("\n")
                    break

                # Update a financial goal
                elif submenu in ['2', 'up', 'update', 'update goals']:
                    print("\n\n")
                    while True:
                        valid_goal_description = input("Enter the description of the goal to update: ").capitalize()
                        cursor.execute('''
                            SELECT COUNT(*)
                            FROM FinancialGoals
                            WHERE GoalDescription = ?''', (valid_goal_description,))
                        if cursor.fetchone()[0] > 0:
                            goal_description = input("Enter the new description for the goal: ").capitalize()
                            goal_cost = valid_float_input("Enter the new cost for the goal: ")
                            cursor.execute('''
                                UPDATE FinancialGoals
                                SET GoalDescription = ?, GoalCost = ?
                                WHERE GoalDescription''', (goal_description, goal_cost, valid_goal_description))
                            db.commit()
                            print("")
                        elif valid_goal_description == "Back":
                            break
                        else:
                            print("No financial goal found with the provided description. Please try again or type 'Back'.\n")

                # Shows progress towards financial goals
                elif submenu in ['3', 'v', 'view', 'view goals', 'view progress']:
                    print("\n\n")
                    table_financial_goals()
                    print("\n")
                    break
                    # needs to ask user which category to check

                # Back to main menu
                elif submenu in ['4', 'b', 'back']:
                    print("\n\n\n\n")
                    break

        # Exits program after short delay, closes db and cursor
        elif menu in ['5', 'q', 'quit', 'exit']:
            print('\n\nHave a good day.\nGoodbye! :)\n')
            time.sleep(0.7)
            exit()

        # Checks for invalid inputs
        else:
            print("\nYou have provided an invalid input. Please try again\n\n")

except Exception as e:
    print("An error occurred: ", e)
finally:
    # Ensure the cursor and database connection are always closed
    cursor.close()
    db.close()

