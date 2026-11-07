from datetime import datetime
from .expense_service import fetch_expenses, get_month_summary
from .expense_utils import format_money


def show_balance(user_id):
    s = get_month_summary(user_id)

    print(f"\n{'=' * 10} MONEY IN HAND ({datetime.now():%B %Y}) {'=' * 10}")
    print("Carried over from earlier months: ", format_money(s["opening"]))
    print("Money received this month: ", format_money(s["received"]))
    print("Total spent this month: ", format_money(s["spent"]))
    print("Sent to others, net of settled: ", format_money(s["transfers"]))
    print("Money in hand: ", format_money(s["closing"]))


def show_expense_history(user_id, limit=None):
    expenses = fetch_expenses(user_id, limit)

    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\n{'=' * 10} EXPENSE HISTORY (latest {limit}) {'=' * 10}")

    for number, expense in enumerate(expenses, start=1):
        path = [expense["category"]]

        if expense["subcategory"] != expense["category"]:
            path.append(expense["subcategory"])

        if expense["recipient"]:
            if expense["subcategory"] == "Receive Money":
                direction = "from"
            elif expense["funded_by"]:
                direction = "spent by"
            else:
                direction = "to"
            path.append(f"{direction} {expense['recipient']}")

        print(
            f"{number}. {' >> '.join(path)} >> {expense['description']}: "
            f"{format_money(expense['amount'])}"
        )

        receipt = " | 📎 receipt attached" if expense["has_receipt"] else ""
        
        print(
            f"Spent on: {expense['spent_on']:%Y-%m-%d} | "
            f"Recorded: {expense['recorded_at'].astimezone():%Y-%m-%d %H:%M:%S}{receipt}"
        )