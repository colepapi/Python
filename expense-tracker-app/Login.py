
from src.auth_service import register_user, user_login
from src.user_repository import view_user_details
from src.expenses.expense_menu import run_expense_menu

# main program
if __name__ == "__main__":

    print(f"{'=' * 10} Welcome to the Expense Tracker App! 💰 {'=' * 10} \n")

    while True:
        print("1. Register")
        print("2. View registered details")
        print("3. Login")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_user()

        elif choice == "2":
            user_id = input("Enter your 8-digit User ID: ").strip()
            view_user_details(user_id)

        elif choice == "3":
            user_id = input("Enter your 8-digit User ID: ").strip()
            session = user_login(user_id)
            if session:
                run_expense_menu(session["user_id"], session["full_name"])

        elif choice == "4":
            break

        else:
            print("Invalid option.❌\n")
