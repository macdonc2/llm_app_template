import hmac, hashlib, secrets
from .config import settings

def new_salt() -> str:
    return secrets.token_hex(16)

def generate_userid(email: str, salt: str) -> str:
    pepper = settings.user_salt.encode()
    msg = (salt + email).encode()
    return hmac.new(pepper, msg, hashlib.sha256).hexdigest()
