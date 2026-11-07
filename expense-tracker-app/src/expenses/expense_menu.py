from .expense_config import CURRENCY, MAIN_MENU
from .expense_service import add_expense, count_income, record_income
from .expense_reports import show_balance, show_expense_history
from .expense_utils import get_choice, show_menu

import traceback

def run_expense_menu(user_id, full_name):
    print(f"\n{'=' * 10} EXPENSE TRACKER: {full_name} {'=' * 10}")

    try:
        if count_income(user_id) == 0:
            print("\nNo money received has been recorded yet.")
            if get_choice("Record it now? (y/n): ", {"y", "n"}) == "y":
                record_income(user_id)

        while True:
            show_menu("Main Menu", MAIN_MENU, include_back=False)
            choice = get_choice("Select an option: ", MAIN_MENU)

            try:
                if choice == "1":
                    record_income(user_id)

                elif choice == "2":
                    add_expense(user_id)

                elif choice == "3":
                    show_balance(user_id)

                elif choice == "4":
                    show_expense_history(user_id)

                elif choice == "5":
                    print("Logged out. Thank you for using the Expense Tracker.\n")
                    return

            except (KeyboardInterrupt, EOFError):
                raise
            except Exception as error:
                traceback.print_exc()
                print(f"Something went wrong: {error}❌")

    except (KeyboardInterrupt, EOFError):
        print("\nLogged out.\n")
    except Exception as error:
        print(f"Could not start the expense tracker: {error}❌")

                