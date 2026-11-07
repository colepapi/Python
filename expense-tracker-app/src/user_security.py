from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

pin_hasher = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2, hash_len=32, salt_len=16)

def hash_pin(pin: str) -> str:
    return pin_hasher.hash(pin)

def verify_pin(pin: str, stored_hash: str) -> bool:
    try:
        return pin_hasher.verify(stored_hash, pin)
    except (VerifyMismatchError, VerificationError, InvalidHashError, ValueError):
        return False

def pin_hash_needs_update(stored_hash: str) -> bool:
    return pin_hasher.check_needs_rehash(stored_hash)