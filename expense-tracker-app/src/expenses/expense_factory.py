from datetime import datetime

from .expense_utils import get_amount


def create_expense(category, subcategory, amount, **extra):
    return {
        "category": category,
        "subcategory": subcategory,
        "description": None,
        "amount": amount,
        "timestamp": datetime.now().astimezone(),
        **extra
    }

def ask_for_expense(category, subcategory, prompt):
    return create_expense(category, subcategory, get_amount(prompt))