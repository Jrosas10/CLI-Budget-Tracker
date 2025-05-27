import json
from datetime import datetime
import os

FILE_NAME = "transactions.json"

# Load existing transactions
def load_transactions():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# Save transactions to file
def save_transactions(transactions):
    with open(FILE_NAME, "w") as file:
        json.dump(transactions, file, indent=4)

from datetime import datetime

# Monthly Summary
def view_monthly_summary(transactions):
    month_input = input("Enter month to view (YYYY-MM): ").strip()

    # Validate input format
    try:
        datetime.strptime(month_input, "%Y-%m")
    except ValueError:
        print("Invalid format. Please enter month as YYYY-MM (e.g., 2024-12).")
        return

    monthly_income = 0
    monthly_expense = 0
    count = 0

    for t in transactions:
        if t["date"].startswith(month_input):
            if t["type"] == "Income":
                monthly_income += t["amount"]
            elif t["type"] == "Expense":
                monthly_expense += abs(t["amount"])
            count += 1

    if count == 0:
        print(f"\nNo transactions found for {month_input}.\n")
        return

    net = monthly_income - monthly_expense
    month_label = datetime.strptime(month_input, "%Y-%m").strftime("%B %Y")

    print("\n------ Monthly Summary ------")
    print(f"Month:           {month_label}")
    print(f"Total Income:    ${monthly_income:.2f}")
    print(f"Total Expenses: -${monthly_expense:.2f}")
    print(f"Net Change:      ${net:.2f}")
    print("-----------------------------\n")
16


# Add income
def add_income(transactions):
    try:
        amount = float(input("Enter income amount: $"))
        entry = {
            "type": "Income",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        transactions.append(entry)
        save_transactions(transactions)
        print(f"Added income: ${amount:.2f}")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Add expense
def add_expense(transactions):
    try:
        amount = float(input("Enter expense amount: $"))
        entry = {
            "type": "Expense",
            "amount": -amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        transactions.append(entry)
        save_transactions(transactions)
        print(f"Added expense: ${amount:.2f}")
    except ValueError:
        print("Invalid input. Please enter a number.")

# View current balance
def view_balance(transactions):
    balance = sum(t["amount"] for t in transactions)
    print(f"\nCurrent balance: ${balance:.2f}\n")

# View transaction history
def view_history(transactions):
    print("\nTransaction History:")
    if not transactions:
        print("No transactions yet.")
        return
    for t in transactions:
        print(f"{t['date']} - {t['type']}: ${t['amount']:.2f}")
    print()

# CSV export
import csv

def export_to_csv(transactions):
    if not transactions:
        print("No transactions to export.")
        return

    filename = input("Enter filename to export (without extension): ").strip()
    if not filename:
        filename = "export"
    filepath = f"{filename}.csv"

    try:
        with open(filepath, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "type", "amount"])
            writer.writeheader()
            for t in transactions:
                writer.writerow(t)
        print(f"Transactions exported successfully to {filepath}\n")
    except Exception as e:
        print(f"Export failed: {e}")

# Main menu
def menu():
    transactions = load_transactions()

    while True:
        print("------ Budget Tracker ------")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. View History")
        print("5. View Monthly Summary")
        print("6. Export Transaction to CSV")
        print("7. Exit")
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == '1':
            add_income(transactions)
        elif choice == '2':
            add_expense(transactions)
        elif choice == '3':
            view_balance(transactions)
        elif choice == '4':
            view_history(transactions)
        elif choice =='5':
            view_monthly_summary(transactions)
        elif choice =='6':
            export_to_csv(transactions)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()
