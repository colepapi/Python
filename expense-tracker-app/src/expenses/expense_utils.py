from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from datetime import date, datetime, timedelta
from pathlib import Path
from .expense_config import(CURRENCY, MAX_AMOUNT, MAX_BACKDATE_DAYS, MAX_DESCRIPTION_LENGTH, MAX_RECEIPT_BYTES, RECEIPT_TYPES)

CENT = Decimal("0.01")

def get_amount(prompt, allow_zero=True):
    while True:
        try:
            amount = Decimal(input(prompt).strip())
        except InvalidOperation:
            print("Error: Enter a valid number.")
            continue

        if not amount.is_finite() or amount < 0 or amount > MAX_AMOUNT:
            print(f"Error: Enter a non-negative amount up to {format_money(MAX_AMOUNT)}.")
            continue

        amount = amount.quantize(CENT, rounding=ROUND_HALF_UP)

        if not allow_zero and amount == 0:
            print("Error: Amount must be greater than zero.")
            continue

        return amount

def get_choice(prompt, options):
    while True:
        choice = input(prompt).strip()

        if choice in options:
            return choice

        print("Error: Invalid selection. Choose an available option.")

def format_money(amount):
    return f"{CURRENCY} {amount:,.2f}"

def get_description():
    while True:
        description = input("Description (what was the money spent on?): ").strip()

        if description:
            return description

        print("Description cannot be empty. Please enter a comment.")

def get_date(prompt):
    today = date.today()

    while True:
        raw = input(prompt).strip()

        try:
            if raw.isdigit() and len(raw) <= 2:
                value = today.replace(day=int(raw))
            else:
                value = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Enter the date as YYYY-MM-DD (e.g. 2026-10-13) or a day number.")
            continue

        if value > today:
            print("Error: The date cannot be in the future.")
        elif value < today - timedelta(days=MAX_BACKDATE_DAYS):
            print(f"Error: The date cannot be more than {MAX_BACKDATE_DAYS} days ago.")
        else:
            return value

def image_type(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data[4:12] == b"ftypheic" or data[4:12] == b"ftypmif1":
        return "image/heic"
    return None

def get_recipient():
    while True:
        name = input("Recipient's name: ").strip()

        if not name:
            print("Recipient's name cannot be empty.")
        elif len(name) > 100:
            print("Name is too long (max 100 characters).")
        else:
            return name

def get_receipt():
    while True:
        raw = input("Receipt image path (png/jpg/jpeg/heic) or press Enter to skip: ").strip().strip("\"'")

        if not raw:
            return None

        path = Path(raw).expanduser()

        if path.suffix.lower() not in RECEIPT_TYPES:
            print("Error: Only .png, .jpg, .jpeg and .heic files are allowed.")
            continue

        try:
            if not path.is_file():
                print("Error: File not found.")
                continue

            if path.stat().st_size > MAX_RECEIPT_BYTES:
                print(f"Error: File is larger than {MAX_RECEIPT_BYTES // (1024 * 1024)} MB.")
                continue

            data = path.read_bytes()
        except OSError as error:
            print(f"Error: Could not read the file ({error}).")
            continue

        mime = image_type(data)

        if mime is None:
            print("Error: That file is not a valid PNG, JPEG or HEIC image.")
            continue

        return {"receipt_data": data}

def show_menu(title, options, include_back=True):
    print(f"\n{'=' * 10} {title.upper()} {'=' * 10}")

    for number, label in options.items():
        print(f"{number}. {label}")

    if include_back:
        print("0. Back")