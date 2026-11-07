import re
import secrets

from .database import db_connection

USER_ID_PATTERN = re.compile(r"^\d{8}$")


def is_valid_user_id(user_id: str) -> bool:
    return bool(USER_ID_PATTERN.fullmatch(user_id or ""))


def generate_unique_user_id(conn):
    while True:
        user_id = str(secrets.randbelow(90_000_000) + 10_000_000)

        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
            if cur.fetchone() is None:
                return user_id


# view user details without login into the expense menu
def view_user_details(user_id):
    if not is_valid_user_id(user_id):
        print("User ID must be exactly 8 digits.❌")
        return

    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, full_name, email, created_at FROM users WHERE user_id = %s", (user_id,),)
                user = cur.fetchone()

        if user is None:
            print("User not found.❌")
            return

        print("\n--- Registered User Details ---")
        print(f"User ID: {str(user[0]).strip()}")
        print(f"Full name: {user[1]}")
        print(f"Email: {user[2]}")
        print(f"Registered at: {user[3]}\n")

    except Exception as error:
        print(f"Could not retrieve user details: {error}❌")