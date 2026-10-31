import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"


def load_expenses():
    """Load expenses from the JSON file, or return an empty list."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("\n[!] Warning: Could not read the data file. Starting with an empty tracker.")
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)
    except OSError:
        print("\n[!] Error: Could not save data to file.")


def add_expense(expenses):
    """Ask for expense details and save a new expense."""
    print("\n--- Add New Expense ---")
    date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("[!] Invalid date format. Using today's date instead.")
            date_str = datetime.today().strftime("%Y-%m-%d")

    print("Categories: Food, Transport, Utilities, Entertainment, Shopping, Other")
    category = input("Enter category: ").strip().capitalize() or "Other"

    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("[!] Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("[!] Invalid input. Please enter a valid number.")

    description = input("Enter brief description: ").strip() or "N/A"
    expense = {
        "date": date_str,
        "category": category,
        "amount": round(amount, 2),
        "description": description,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"\nSuccessfully added: {amount:.2f} for {category}!")


def view_expenses(expenses):
    """Display all saved expenses."""
    print("\n--- Tracked Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'ID':<5} | {'Date':<12} | {'Category':<15} | {'Amount':<10} | Description")
    print("-" * 75)
    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:<5} | {expense['date']:<12} | {expense['category']:<15} | "
            f"{expense['amount']:<10.2f} | {expense['description']}"
        )


def delete_expense(expenses):
    """Delete an expense using its displayed ID."""
    view_expenses(expenses)
    if not expenses:
        return

    print("\n--- Delete an Expense ---")
    while True:
        choice = input("Enter the ID to delete (or 'c' to cancel): ").strip()
        if choice.lower() == "c":
            return
        try:
            index = int(choice) - 1
            if 0 <= index < len(expenses):
                removed = expenses.pop(index)
                save_expenses(expenses)
                print(f"\nRemoved expense: {removed['amount']:.2f} spent on {removed['category']}.")
                return
            print(f"[!] Choose an ID between 1 and {len(expenses)}.")
        except ValueError:
            print("[!] Please enter a valid number or 'c'.")


def show_summary(expenses):
    """Show total spending and spending by category."""
    print("\n--- Financial Summary ---")
    if not expenses:
        print("No summary available. Add expenses first.")
        return

    total = sum(expense["amount"] for expense in expenses)
    category_totals = {}
    for expense in expenses:
        category = expense["category"]
        category_totals[category] = category_totals.get(category, 0) + expense["amount"]

    print(f"Total Spent: {total:.2f}")
    print("\nBreakdown by Category:")
    for category, category_total in category_totals.items():
        percentage = (category_total / total) * 100 if total else 0
        print(f" - {category:<15}: {category_total:.2f} ({percentage:.1f}%)")


def main():
    """Run the expense tracker menu."""
    expenses = load_expenses()
    while True:
        print("\n=============================")
        print("    PYTHON EXPENSE TRACKER")
        print("=============================")
        print("1. Add an Expense")
        print("2. View All Expenses")
        print("3. Delete an Expense")
        print("4. View Spending Summary")
        print("5. Exit Application")

        choice = input("\nSelect an option (1-5): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            show_summary(expenses)
        elif choice == "5":
            print("\nGoodbye! Stay on budget.")
            break
        else:
            print("[!] Invalid option. Please choose 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
