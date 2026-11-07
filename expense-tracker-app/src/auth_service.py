import getpass
import hmac
import pwinput

from .user_config import MAX_ATTEMPTS, RETRY_DELAY, LOCKOUT_TIME
from .database import db_connection
from .user_security import hash_pin, verify_pin, pin_hash_needs_update
from .ui_helpers import animated_countdown
from .user_repository import generate_unique_user_id, is_valid_user_id

weak_pins = {
    "000000", "111111", "123456", "222222", "333333", "444444", "555555", "666666", "777777", "888888", "999999", "654321"
}


def _is_valid_pin_format(pin: str) -> bool:
    return pin.isascii() and pin.isdigit() and len(pin) == 6


# Register the user
def register_user():
    full_name = input("Enter your full Name: ").strip()
    email = input("Enter your email address: ").strip().lower()

    # Pin creation & security
    while True:
        pin = pwinput.pwinput(prompt="Create a Strong 6-Digit Pin: ", mask="*")
        if not _is_valid_pin_format(pin):
            print("PIN must contain exactly 6 numbers.❌")
            continue

        if pin in weak_pins:
            print("Choose a Recommended Strong Pin! This is too obvious.❌")
            continue

        confirm_pin = pwinput.pwinput(prompt="Confirm your PIN: ", mask="*")

        if not hmac.compare_digest(pin, confirm_pin):
            print("PINs do not match. Try again.❌")
            continue

        break

    print("PIN successfully created!✓")

    # hash the pin before storing it
    stored_hash = hash_pin(pin)

    try:
        with db_connection() as conn:
            user_id = generate_unique_user_id(conn)

            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (user_id, full_name, email, pin_hash) VALUES (%s, %s, %s, %s)", (user_id, full_name, email, stored_hash))

        print("\nUser registered successfully.✓")
        # print(f"Name: {full_name}")
        print(f"Your User ID is: {user_id}  (keep it, you need it to log in)\n")
        return user_id

    except Exception as error:
        print(f"Registration failed. Check your input and database.❌\nDetails: {error}")
        return None


def _reset_failures(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE user_id = %s", (user_id,))
    conn.commit()


# User logging in
def _attempt_login(user_id, pin):
    if not is_valid_user_id(user_id):
        return None, "User ID must be exactly 8 digits.", False

    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT full_name, pin_hash, locked_until, clock_timestamp() FROM users WHERE user_id = %s", (user_id,))
                user = cur.fetchone()

            if user is None:
                return None, "User not found.", False

            full_name, stored_hash, locked_until, now = user

            if locked_until is not None:
                if now < locked_until:
                    remaining = max(1, int((locked_until - now).total_seconds()) + 1)
                    return None, f"Account locked. Try again in {remaining} seconds.", False
                _reset_failures(conn, user_id)  

            valid_format = _is_valid_pin_format(pin)

            if valid_format and verify_pin(pin, stored_hash):
                with conn.cursor() as cur:
                    if pin_hash_needs_update(stored_hash):
                        cur.execute("UPDATE users SET pin_hash = %s WHERE user_id = %s", (hash_pin(pin), user_id))

                    cur.execute("UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE user_id = %s", (user_id,))
                conn.commit()
                return {"user_id": user_id, "full_name": full_name}, "Login successful.", False

            # Failed attempt
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE user_id = %s RETURNING failed_attempts", (user_id,))
                attempts = cur.fetchone()[0]
            conn.commit()

            if attempts >= MAX_ATTEMPTS:
                with conn.cursor() as cur:
                    cur.execute("UPDATE users SET locked_until = clock_timestamp() + (%s * INTERVAL '1 second') WHERE user_id = %s", (LOCKOUT_TIME, user_id))
                conn.commit()
                return None, f"Too many failed attempts. Account locked for {LOCKOUT_TIME} seconds.🔒", False

            reason = "Incorrect PIN." if valid_format else "PIN must contain exactly 6 digits."
            return None, f"{reason} {MAX_ATTEMPTS - attempts} attempt(s) remaining before your account is locked.", True

    except Exception as error:
        return None, f"Login could not be completed: {error}", False


# Used by the Streamlit dashboard
def authenticate(user_id, pin):
    session, message, _ = _attempt_login(user_id, pin)
    return session, message


# Used by the terminal: prompts, prints, waits between retries
def user_login(user_id):
    if not is_valid_user_id(user_id):
        print("User ID must be exactly 8 digits.❌\n")
        return None

    try:
        while True:
            pin = getpass.getpass("Enter your 6-Digit PIN: ")
            session, message, can_retry = _attempt_login(user_id, pin)

            if session:
                print(f"\nLogin successful.✓\n")
                return session

            print(f"{message}❌\n")

            if not can_retry:
                return None

            animated_countdown(RETRY_DELAY, "Wait before retrying: ")

    except KeyboardInterrupt:
        print("\nLogin cancelled.")
        return None

