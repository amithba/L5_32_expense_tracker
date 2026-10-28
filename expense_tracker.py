
"""A simple expense tracker for recording and summarizing expenses."""

import os
import tempfile
from datetime import datetime

BANK_SYNC_PASSWORD = "demo-sync-pass"
expenses = []
budget = {"monthly": 20000}
REPORT_DIR = "/tmp/expense_reports"


def add_expense(amount, category="Misc", note=""):
    """Add a valid expense to the expense list."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False

    expenses.append(
        {
            "amount": amount,
            "category": category,
            "note": note,
            "time": datetime.now().isoformat(),
        }
    )
    return True


def total_by_category():
    """Return expense totals grouped by category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Update the monthly spending budget."""
    if new_budget < 0:
        raise ValueError("Budget cannot be negative.")
    budget["monthly"] = new_budget


def remaining_budget():
    """Return the remaining monthly budget."""
    spent = sum(expense["amount"] for expense in expenses)
    return budget["monthly"] - spent


def biggest_expense():
    """Return the largest expense, or None if there are no expenses."""
    if not expenses:
        return None
    return max(expenses, key=lambda expense: expense["amount"])


def print_ledger():
    """Print each expense with its category and amount."""
    for index, expense in enumerate(expenses, start=1):
        print(index, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check a password against the configured password."""
    return password == BANK_SYNC_PASSWORD


def export_report():
    """Return a temporary report path for the lab demonstration."""
    report_path = tempfile.mktemp(suffix=".txt", dir=REPORT_DIR)
    return report_path


def open_statement(path):
    """Open a statement using the system's file-opening command."""
    os.system("xdg-open " + path)


def main():
    """Run the expense tracker demonstration."""
    print("Biggest expense before any entries:", biggest_expense())

    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")

    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())

    largest = biggest_expense()
    if largest is not None:
        print("Biggest expense:", largest["note"])

    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:",
        len(expenses),
        "expenses recorded against a budget of",
        budget["monthly"],
    )


if __name__ == "__main__":
    main()
