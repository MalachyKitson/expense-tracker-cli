import json
from datetime import datetime
import csv
from tabulate import tabulate

#Handling data
DATA_FILE = "expenses.json"

def loadExpenses():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def saveExpenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

def generateId():
    expenses = loadExpenses()
    return max([expense['id'] for expense in expenses], default=0) + 1

#Commands
def addExpense(description, amount, category=None):
    if not description or not description.strip():
        description = "No description"

    expenses = loadExpenses()

    if amount < 0:
        print(f"Negative amount provided: {amount} - Use only for refunds")

    newExpense = {
        "id": generateId(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount,
        "category": category or "Uncategorised"
    }

    expenses.append(newExpense)
    saveExpenses(expenses)
    print(f"Expenses added successfully (ID: {newExpense['id']})")

def listExpenses():
    expenses = loadExpenses()

    if not expenses:
        print("No expenses found")
        return
    
    table = []
    for expense in expenses:
        table.append([expense['id'], expense['date'], expense['description'], expense['id'], f"${expense['amount'],}", expense['category']])
    headers = ["ID", "Date", "Description", "Amount", "Category"]
    print(tabulate(table, headers=headers, tablefmt="grid"))

def expensesSummary(month=None, budget=None):
    expenses = loadExpenses()
    total = 0
    filteredExpenses = expenses

    if month:
        filteredExpenses = [
            expense for expense in expenses if datetime.strptime(expense['date'], "%d-%m-%y").month == month
        ]

    filteredTotal = sum(expense['amount'] for expense in filteredExpenses)
    total = sum(expense['amount'] for expense in expenses)
    print(f"Total expenses: ${total}")
    if month:
        print(f"Total expenses for month {month}: ${filteredTotal}")
    if budget and filteredTotal > budget:
        print(f"WARNING: You have exceeded you budget of ${budget} by ${filteredTotal - budget}")

def deleteExpense(ExpenseID):
    expenses = loadExpenses()
    updatedExpenses = [expense for expense in expenses if expense['id'] != ExpenseID]
    if len(updatedExpenses) == len(expenses):
        print(f"No expense found with ID: {ExpenseID}")
        return
    saveExpenses(updatedExpenses)
    print(f"Expense deleted successfully (ID: {ExpenseID})")

def updateExpenses(expenseID, description=None, amount=None, category=None):
    if not description or not description.strip():
        description = "No description"

    expenses = loadExpenses()
    for expense in expenses:
        if expense['id'] == expenseID:
            if description:
                expense['description'] = description
            if amount:
                expense['amount'] = amount
            if category:
                expense['category'] = category
            saveExpenses(expenses)
            print(f"Expense updated successfully (ID: {expenseID})")
            return
    print(f"No expense found with ID: {expenseID}")

def exportToCsv():
    expenses = loadExpenses()
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Date", "Description", "Amount", "Category"])
        for expense in expenses:
            writer.writerow([expense['id'], expense['date'], expense['description'], expense['amount'], expense['category']])
    print("Expenses exported to expenses.csv")