import psycopg2

from datetime import date, timedelta
from decimal import Decimal
from ..database import db_connection
from .expense_config import CURRENCY, INCOME_TYPES, MAX_DESCRIPTION_LENGTH
from .expense_categories import select_expense
from .expense_utils import(format_money, get_amount, get_choice, get_date, get_description, show_menu)
from .expense_factory import create_expense

def month_range(month=None):
    first = (month or date.today()).replace(day=1)
    next_first = (first + timedelta(days=32)).replace(day=1)
    return first, next_first

# Option 4: record money received
def count_income(user_id):
    with db_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM income WHERE user_id = %s", (user_id,),)
        return cur.fetchone()[0]

def add_income(user_id, kind, amount, received_on, note=None):
    with db_connection() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO income (user_id, kind, amount, received_on, note) VALUES (%s, %s, %s, %s, %s)", (user_id, kind, amount, received_on, note),)

def fetch_income(user_id):
    with db_connection() as conn, conn.cursor() as cur:
        cur.execute(""" SELECT kind, amount, received_on, note, recorded_at FROM income WHERE user_id = %s ORDER BY received_on DESC, income_id DESC """, (user_id,),)
        rows = cur.fetchall()

    keys = ("kind", "amount", "received_on", "note", "recorded_at")
    return [dict(zip(keys, row)) for row in rows]


# Option 2: add expenses
def _insert_expense(cur, user_id, expense, funded_by=None):
    receipt = expense.get("receipt_data")
    cur.execute(""" INSERT INTO expenses(user_id, category, subcategory, description, amount, food_cost, delivery_fee, spent_on, recorded_at, receipt_image, recipient, funded_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """,
        (
            user_id,
            expense["category"],
            expense["subcategory"],
            expense["description"],
            expense["amount"],
            expense.get("food_cost"),
            expense.get("delivery_fee"),
            expense["spent_on"],
            expense["timestamp"],
            psycopg2.Binary(receipt) if receipt else None,
            expense.get("recipient"),
            funded_by,
        ),
    )


def save_expense(user_id, expense):
    with db_connection() as conn, conn.cursor() as cur:
        _insert_expense(cur, user_id, expense)


def fetch_expenses(user_id, limit=None):
    with db_connection() as conn, conn.cursor() as cur:
        cur.execute(""" SELECT expense_id, category, subcategory, recipient, description, amount, spent_on, recorded_at, (receipt_image IS NOT NULL), funded_by FROM expenses WHERE user_id = %s ORDER BY spent_on DESC, recorded_at DESC, expense_id DESC LIMIT %s """, (user_id, limit),)
        rows = cur.fetchall()

    keys = ("expense_id", "category", "subcategory", "recipient", "description", "amount", "spent_on", "recorded_at", "has_receipt", "funded_by",)
    return [dict(zip(keys, row)) for row in rows]


def fetch_receipt(user_id, expense_id):
    with db_connection() as conn, conn.cursor() as cur:
        cur.execute(""" SELECT receipt_image FROM expenses WHERE expense_id = %s AND user_id = %s AND receipt_image IS NOT NULL """, (expense_id, user_id),)
        row = cur.fetchone()

    return bytes(row[0]) if row else None

CASH_OUT = (
    "CASE WHEN funded_by IS NOT NULL THEN 0 "
    "WHEN category = 'Money Transfer' AND subcategory = 'Receive Money' THEN -amount "
    "ELSE amount END"
)

SPENDING = "CASE WHEN category = 'Money Transfer' THEN 0 ELSE amount END"


def get_money_in_hand(user_id, as_of=None):
    as_of = as_of or date.today()

    with db_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT COALESCE(SUM(amount), 0) FROM income WHERE user_id = %s AND received_on <= %s", (user_id, as_of),)
        received = cur.fetchone()[0]

        cur.execute(
            f"SELECT COALESCE(SUM({CASH_OUT}), 0) FROM expenses "
            "WHERE user_id = %s AND spent_on <= %s",
            (user_id, as_of),
        )
        cash_out = cur.fetchone()[0]

    return received - cash_out


def get_month_summary(user_id, month=None):
    first, next_first = month_range(month)

    with db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                COALESCE(SUM(amount) FILTER (WHERE received_on <  %s), 0),
                COALESCE(SUM(amount) FILTER (WHERE received_on >= %s), 0)
            FROM income WHERE user_id = %s AND received_on < %s
            """,
            (first, first, user_id, next_first),)
        income_before, received = cur.fetchone()

        cur.execute(
            f"""
            SELECT
                COALESCE(SUM({CASH_OUT}) FILTER (WHERE spent_on <  %s), 0),
                COALESCE(SUM({CASH_OUT}) FILTER (WHERE spent_on >= %s), 0),
                COALESCE(SUM({SPENDING}) FILTER (WHERE spent_on >= %s), 0)
            FROM expenses WHERE user_id = %s AND spent_on < %s
            """,
            (first, first, first, user_id, next_first),)

        cash_before, cash_month, spent = cur.fetchone()

    opening = income_before - cash_before
    return {
        "opening": opening,
        "received": received,
        "spent": spent,
        "transfers": cash_month - spent,
        "closing": opening + received - cash_month,
    }


# record money received 
def record_income(user_id):
    show_menu("Money Received", INCOME_TYPES)
    choice = get_choice("Select type: ", {*INCOME_TYPES, "0"})

    if choice == "0":
        return

    kind = INCOME_TYPES[choice]

    amount = get_amount(f"Amount received ({CURRENCY}): ", allow_zero=False)
    received_on = get_date("Date received (enter YYYY-MM-DD or a day number): ")
    note = input("Note (optional, e.g. who sent it): ").strip()[:MAX_DESCRIPTION_LENGTH] or None

    add_income(user_id, kind, amount, received_on, note)
    print(f"{kind} of {format_money(amount)} recorded for {received_on:%Y-%m-%d}.✓")

    print(f"Money in hand as of {received_on:%Y-%m-%d}:", format_money(get_money_in_hand(user_id, received_on)))

#  money transfers 
def fetch_pending_transfers(user_id):
    with db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT expense_id, recipient, amount, spent_on
            FROM expenses
            WHERE user_id = %s
              AND category = 'Money Transfer' AND subcategory = 'Send Money'
              AND settled_by IS NULL
            ORDER BY spent_on, expense_id
            """, 
            (user_id,),
        )
        rows = cur.fetchall()

    keys = ("expense_id", "recipient", "amount", "spent_on")
    return [dict(zip(keys, row)) for row in rows]

def _group_by_recipient(pending):
    groups = {}

    for send in pending:
        name = (send["recipient"] or "Unknown").strip()
        group = groups.setdefault(name.lower(), {"name": name, "sends": []})
        group["sends"].append(send)

    return list(groups.values())
    

# the user picks any subset of sends. Returns the chosen sends
def get_send_selection(sends, name):
    options = {
        str(number): f"sent {s['spent_on']:%Y-%m-%d} | {format_money(s['amount'])}"
        for number, s in enumerate(sends, start=1)
    }
    show_menu(f"{name} - Pending Sends", options)
    print("Enter the number(s) to settle, e.g. 2  or  1,3  or  1-3  or  all")

    while True:
        raw = input("Select send(s): ").strip().lower().replace(" ", "")

        if raw == "0":
            return None

        if raw == "all":
            return list(sends)

        chosen = set()

        try:
            for part in raw.split(","):
                if "-" in part:
                    start, end = (int(x) for x in part.split("-", 1))
                    if start > end:
                        raise ValueError
                    chosen.update(range(start, end + 1))
                else:
                    chosen.add(int(part))
        except ValueError:
            print("Error: Use numbers like 2, 1,3, 1-3, or 'all'.")
            continue

        if not chosen or min(chosen) < 1 or max(chosen) > len(sends):
            print(f"Error: Choose numbers between 1 and {len(sends)}.")
            continue

        return [sends[number - 1] for number in sorted(chosen)]


def collect_transfer_spending(name, total_sent, earliest_send):
    """Ask what the recipient spent the money on. Returns a list of expenses."""
    items = []
    remaining = total_sent

    while remaining > 0:
        print(f"\nStill to account for: {format_money(remaining)}")
        print(f"Record what {name} spent money on. Select 0 to prompt Confirmation.")
        expense = select_expense(allow_transfers=False)

        if expense is None:
            break

        if expense["amount"] == 0:
            print("Error: Amount must be greater than zero.")
            continue

        if expense["amount"] > remaining:
            print(f"Error: That is more than the {format_money(remaining)} still unaccounted for.")
            continue

        expense["description"] = get_description()

        while True:
            spent_on = get_date(
                f"Date {name} spent it (YYYY-MM-DD): "
            )
            if spent_on < earliest_send:
                print(f"Error: Cannot be before the money was sent ({earliest_send:%Y-%m-%d}).")
                continue
            break

        expense["spent_on"] = spent_on
        expense["recipient"] = name
        items.append(expense)
        remaining -= expense["amount"]

        print(f"Added: {expense['category']} - {format_money(expense['amount'])}")

    return items


def record_transfer_return(user_id):
    pending = fetch_pending_transfers(user_id)

    if not pending:
        print("No sent money is waiting to be settled.")
        return

    groups = _group_by_recipient(pending)
    options = {
        str(number): (
            f"{g['name']} | {len(g['sends'])} send(s) | "
            f"total {format_money(sum(s['amount'] for s in g['sends']))}"
        )
        for number, g in enumerate(groups, start=1)
    }
    show_menu("Money Sent - Awaiting Settlement", options)
    choice = get_choice("Select the person: ", {*options, "0"})

    if choice == "0":
        return

    group = groups[int(choice) - 1]
    name = group["name"]
    sends = group["sends"]

    if len(sends) > 1:
        sends = get_send_selection(sends, name)
        if sends is None:
            return

    total_sent = sum(s["amount"] for s in sends)
    earliest_send = min(s["spent_on"] for s in sends)
    latest_send = max(s["spent_on"] for s in sends)

    print(f"\nSettling {len(sends)} send(s) to {name}:")
    for s in sends:
        print(f"{s['spent_on']:%Y-%m-%d}  {format_money(s['amount'])}")
    print(f"Total sent: {format_money(total_sent)}")

    # what did the recipient spend it on?
    items = collect_transfer_spending(name, total_sent, earliest_send)
    remaining = total_sent - sum(i["amount"] for i in items)

    returned = remaining
    unaccounted = 0

    if remaining > 0:
        if get_choice(f"Was the full {format_money(remaining)} returned? (y/n): ", {"y", "n"}) == "n":
            while True:
                returned = get_amount(f"Balance actually returned by {name} ({CURRENCY}): ")
                if returned > remaining:
                    print(f"Error: Cannot be more than the {format_money(remaining)} left.")
                    continue
                break

            unaccounted = remaining - returned

    latest = max([latest_send] + [i["spent_on"] for i in items])

    while True:
        returned_on = get_date("Date settled (YYYY-MM-DD): ")
        if returned_on < latest:
            print(f"Error: Cannot be before {latest:%Y-%m-%d}.")
            continue
        break

    if unaccounted > 0:
        other = create_expense("Other", "Not itemized", unaccounted)
        other["description"] = f"Spent by {name} (not itemized)"
        other["spent_on"] = returned_on
        other["recipient"] = name
        items.append(other)

    print(f"\n{'=' * 10} CONFIRM SETTLEMENT {'=' * 10}")
    print(f"Sent to {name}: {format_money(total_sent)}")
    for item in items:
        print(f"  Spent - {item['category']}: {format_money(item['amount'])} ({item['description']})")
    print(f"Returned: {format_money(returned)}")

    if get_choice("Save settlement? (y/n): ", {"y", "n"}) == "n":
        print("Settlement cancelled.")
        return

    with db_connection() as conn, conn.cursor() as cur:
        cur.execute(""" INSERT INTO expenses(user_id, category, subcategory, recipient, description, amount, spent_on) VALUES (%s, 'Money Transfer', 'Receive Money', %s, %s, %s, %s) RETURNING expense_id """, (user_id, name, f"Returned by {name} (settles {len(sends)} send(s))", returned, returned_on),)
        return_id = cur.fetchone()[0]

        for item in items:
            _insert_expense(cur, user_id, item, funded_by=return_id)

        cur.execute(
            "UPDATE expenses SET settled_by = %s WHERE user_id = %s AND expense_id = ANY(%s)",
            (return_id, user_id, [s["expense_id"] for s in sends]),
        )

    spent = sum(i["amount"] for i in items)
    print(f"\nSettled.✓ Sent {format_money(total_sent)}, spent {format_money(spent)}, "
          f"returned {format_money(returned)}.")
    print(
        f"Money in hand as of {returned_on:%Y-%m-%d}:",
        format_money(get_money_in_hand(user_id, returned_on)),
    )


# adding expense flow 
def show_expense_confirmation(expense):
    print(f"\n{'=' * 10} CONFIRM EXPENSE {'=' * 10}")
    print("Category:", expense["category"])
    print("Subcategory:", expense["subcategory"])
    print("Description:", expense["description"])
    print("Date spent:", f"{expense['spent_on']:%Y-%m-%d}")

    if "food_cost" in expense:
        print("Food cost:", format_money(expense["food_cost"]))
        print("Delivery fee:", format_money(expense["delivery_fee"]))

    if expense.get("receipt_data"):
        print("Receipt: attached")

    if expense.get("recipient"):
        print("Sent to:", expense["recipient"])

    print("Total:", format_money(expense["amount"]))


def add_expense(user_id):
    expense = select_expense()

    if expense is None:
        print("No expense recorded.")
        return

    if expense.get("action") == "receive":
        record_transfer_return(user_id)
        return

    expense["description"] = get_description()
    expense["spent_on"] = get_date("Date money was spent (enter YYYY-MM-DD or a day number): ")
    show_expense_confirmation(expense)

    if get_choice("Save expense? (y/n): ", {"y", "n"}) == "n":
        print("Expense cancelled.")
        return

    in_hand = get_money_in_hand(user_id, expense["spent_on"])

    if expense["amount"] > in_hand:
        print(f"Warning: This expense exceeds your money in hand on {expense['spent_on']:%Y-%m-%d} "
            f"({format_money(in_hand)}).")
              
        if get_choice("Record it anyway? (y/n): ", {"y", "n"}) == "n":
            print("Expense cancelled.")
            return

    save_expense(user_id, expense)
    
    print("Expense saved successfully.")