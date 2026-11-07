from decimal import Decimal

CURRENCY = "KES"
MAX_AMOUNT = Decimal("1000000000")
MAX_DESCRIPTION_LENGTH = 200

MAX_BACKDATE_DAYS = 365
MAX_RECEIPT_BYTES = 5 * 1024 * 1024
RECEIPT_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg", 
    ".jpeg": "image/jpeg",
    ".heic": "image/heic"
}

INCOME_TYPES = {
    "1": "Salary",
    "2": "Top-up"
}

INTERNET_PLANS = {
    "Safaricom": {
        "1": ("10 Mbps", Decimal("2500")),
        "2": ("20 Mbps", Decimal("3500")),
        "3": ("40 Mbps", Decimal("5000"))
    },
    "Zuku": {
        "1": ("10 Mbps", Decimal("2000")),
        "2": ("20 Mbps", Decimal("2800")),
        "3": ("60 Mbps", Decimal("4200"))
    },
    "Faiba": {
        "1": ("30 Mbps", Decimal("3500")),
        "2": ("50 Mbps", Decimal("5000")),
        "3": ("125 Mbps", Decimal("9500"))
    },
}

CATEGORIES = {
    "1": "Food",
    "2": "Transport",
    "3": "Medical Expenses",
    "4": "Utilities",
    "5": "Entertainment",
    "6": "Gym",
    "7": "Shopping",
    "8": "Water",
    "9": "Money Transfer"
}

MONEY_TRANSFER_OPTIONS = {
    "1": "Send Money",
    "2": "Receive Money",
    "3": "Airtime"
}

FOOD_OPTIONS = {
    "1": "Groceries",
    "2": "Restaurants",
    "3": "Fish",
    "4": "Githeri",
    "5": "Minced Meat",
    "6": "Milk",
    "7": "Unga ya Ugali",
    "8": "Beans",
    "9": "Bread",
    "10": "Meat",
    "11": "Eggs"
}

RESTAURANT_OPTIONS = {
    "1": "Dine-In",
    "2": "Delivery"
}

WATER_OPTIONS = {
    "1": "Cooking Water",
    "2": "Neville's Drinking Water",
    "3": "Adults Treated Drinking Water"
}

TRANSPORT_OPTIONS = {
    "1": "Matatu",
    "2": "Uber",
    "3": "Personal Vehicle",
    "4": "Motorbike"
}

UTILITY_OPTIONS = {
    "1": "House Rent",
    "2": "Water",
    "3": "Electricity",
    "4": "Home Decor",
    "5": "Internet"
}

ENTERTAINMENT_OPTIONS = {
    "1": "Cinema",
    "2": "Vacation",
    "3": "Concert",
    "4": "Other forms of Entertainment"
}

MAIN_MENU = {
    "1": "Record money received",
    "2": "Add expense",
    "3": "View balance",
    "4": "View expense history",
    "5": "Log out"
}