from .expense_config import(CATEGORIES, CURRENCY, ENTERTAINMENT_OPTIONS, FOOD_OPTIONS, INTERNET_PLANS, RESTAURANT_OPTIONS, TRANSPORT_OPTIONS, UTILITY_OPTIONS, MONEY_TRANSFER_OPTIONS)
from .expense_factory import ask_for_expense, create_expense
from .expense_utils import format_money, get_amount, get_choice, show_menu, get_receipt, get_recipient


def select_food_expense():
    while True:
        show_menu("Food", FOOD_OPTIONS)
        choice = get_choice("Select an option: ", {*FOOD_OPTIONS, "0"})

        if choice == "0":
            return None

        if FOOD_OPTIONS[choice] == "Restaurants":
            return select_restaurant_expense()
        elif FOOD_OPTIONS[choice]:
            return ask_for_expense(
            "Food",
            f"{FOOD_OPTIONS[choice]}",
            f"{FOOD_OPTIONS[choice]} amount ({CURRENCY}): ")


def select_restaurant_expense():
    while True:
        show_menu("Restaurants", RESTAURANT_OPTIONS)
        choice = get_choice("Select an option: ", {*RESTAURANT_OPTIONS, "0"})

        if choice == "0":
            return None

        service = RESTAURANT_OPTIONS[choice]

        if service == "Dine-In":
            return ask_for_expense(
                "Food", "Restaurants", f"Restaurant food cost ({CURRENCY}): ", detail="Dine-In"
            )

        food_cost = get_amount(f"Food cost ({CURRENCY}): ")
        delivery_fee = get_amount(f"Delivery fee ({CURRENCY}): ")

        return create_expense(
            category="Food",
            subcategory="Restaurants",
            food_cost=food_cost,
            delivery_fee=delivery_fee,
            amount=food_cost + delivery_fee
        )


def select_transport_expense():
    prompts = {
        "Matatu": f"Matatu cost ({CURRENCY}): ",
        "Uber": f"Uber cost ({CURRENCY}): ",
        "Personal Vehicle": f"Cost of fuel consumption ({CURRENCY}): ",
        "Motorbike": f"Motorbike cost ({CURRENCY}): "
    }

    show_menu("Transport", TRANSPORT_OPTIONS)
    choice = get_choice("Select a category: ", {*TRANSPORT_OPTIONS, "0"})

    if choice == "0":
        return None

    method = TRANSPORT_OPTIONS[choice]
    return ask_for_expense("Transport", method, prompts.get(method, f"{method} cost ({CURRENCY}): "))


def select_utilities_expense():
    while True:
        show_menu("Utilities", UTILITY_OPTIONS)
        choice = get_choice("Select a category: ", {*UTILITY_OPTIONS, "0"})

        if choice == "0":
            return None

        utility = UTILITY_OPTIONS[choice]

        if utility == "Internet":
            expense = select_internet_expense()
            if expense is not None:
                return expense
            continue

        return ask_for_expense("Utilities", utility, f"{utility} amount ({CURRENCY}): ")


def select_internet_expense():
    providers = {str(number): name for number, name in enumerate(INTERNET_PLANS, start=1)}

    while True:
        show_menu("Internet Providers", providers)
        choice = get_choice("Select a provider: ", {*providers, "0"})

        if choice == "0":
            return None

        provider = providers[choice]
        plans = INTERNET_PLANS[provider]

        plan_options = {
            number: f"{speed} ({format_money(price)})"
            for number, (speed, price) in plans.items()
        }

        show_menu(f"{provider} Internet Plans", plan_options)
        plan_choice = get_choice("Select a plan: ", {*plans, "0"})

        if plan_choice == "0":
            continue

        speed, price = plans[plan_choice]

        return create_expense(
            category="Utilities",
            subcategory="Internet",
            amount=price
        )


def select_entertainment_expense():
    show_menu("Entertainment", ENTERTAINMENT_OPTIONS)
    choice = get_choice("Select an option: ", {*ENTERTAINMENT_OPTIONS, "0"})

    if choice == "0":
        return None

    activity = ENTERTAINMENT_OPTIONS[choice]
    return ask_for_expense("Entertainment", activity, f"{activity} cost ({CURRENCY}): ")


def select_shopping_expense():
    expense = ask_for_expense("Shopping", "Shopping", f"Shopping amount ({CURRENCY}): ")
    receipt = get_receipt() 

    if receipt:
        expense.update(receipt)

    return expense


def select_water_expense():
    prompts = {
        "Cooking Water": f"Cooking Water cost ({CURRENCY}): ",
        "Neville's Drinking Water": f"Mineral Water Cost ({CURRENCY}): ",
        "Adults Treated Drinking Water": f"Treated Water (Refill) ({CURRENCY}): "
    }

    show_menu("Water", WATER_OPTIONS)
    choice = get_choice("Select a category: ", {*WATER_OPTIONS, "0"})

    if choice == "0":
        return None

    method = WATER_OPTIONS[choice]
    return ask_for_expense("Water", method, prompts.get(method, f"{method} cost ({CURRENCY}): "))


def select_money_transfer_expense():
    while True:
        show_menu("Money Transfer", MONEY_TRANSFER_OPTIONS)
        choice = get_choice("Select an option: ", {*MONEY_TRANSFER_OPTIONS, "0"})

        if choice == "0":
            return None

        transaction = MONEY_TRANSFER_OPTIONS[choice]

        if transaction == "Airtime":
            return ask_for_expense("Money Transfer", transaction, f"{transaction} cost ({CURRENCY}): ")

        elif transaction[choice] == "Receive Money":
            return {"action": "receive"}  

        receiver = get_recipient()
        amount = get_amount(f"Amount to send ({CURRENCY}): ", allow_zero=False)

        return create_expense(
            category="Money Transfer",
            subcategory="Send Money",
            amount=amount,
            recipient=receiver
        )


def select_expense(allow_transfers=True):
    handlers = {
        "1": select_food_expense,
        "2": select_transport_expense,
        "4": select_utilities_expense,
        "5": select_entertainment_expense,
        "7": select_shopping_expense,
        "8": select_water_expense,
        "9": select_money_transfer_expense
    }

    categories = {
        key: name for key, name in CATEGORIES.items()
        if allow_transfers or name != "Money Transfer"
    }

    while True:
        show_menu("Expense Categories", CATEGORIES)
        choice = get_choice("Select a category: ", {*CATEGORIES, "0"})

        if choice == "0":
            return None

        if choice in handlers:
            expense = handlers[choice]()
            if expense is not None:
                return expense
            continue

        category = CATEGORIES[choice]
        return ask_for_expense(category, category, f"{category} amount ({CURRENCY}): ")