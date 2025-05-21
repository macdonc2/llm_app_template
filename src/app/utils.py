import hmac, hashlib, secrets
from .config import settings

def new_salt() -> str:
    """
    Generate a new random cryptographic salt.

    Returns:
        str: A randomly generated hexadecimal string of length 32.
    """

    return secrets.token_hex(16)

def generate_userid(email: str, salt: str) -> str:
    """
    Generate a deterministic user ID by hashing the salt and email with HMAC-SHA256.

    Args:
        email (str): The user's email address.
        salt (str): A unique cryptographic salt.

    Returns:
        str: The generated user ID as a hexadecimal SHA256 hash.
    """
    
    pepper = settings.user_salt.encode()
    msg = (salt + email).encode()
    return hmac.new(pepper, msg, hashlib.sha256).hexdigest()
