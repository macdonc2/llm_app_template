"""
utils.py

This module provides cryptographic utilities for secure user management in a microservices-based
FastAPI application. It centralizes functions for deterministic user ID generation and salt
creation, supporting robust authentication and user identity schemes in distributed, scalable systems.

Overview:
---------
- Supplies a secure method (`new_salt`) for generating random, cryptographic salts using Python's secrets library.
- Implements deterministic, HMAC-based user ID generation (`generate_userid`) by combining user email and per-user salt
  with a global pepper (from service configuration). This approach yields unique, non-guessable identifiers,
  improving user security and preventing enumeration or correlation attacks.

Key Features:
-------------
- **Random Salt Generation:** Produces strong, unique salts for each user, vital for password hashing and credential storage.
- **HMAC-SHA256 User ID:** User IDs are not simple UUIDs but are derived via a cryptographic HMAC (with secret pepper, per-user salt, and email), making them irreversible and collision-resistant.
- **Configuration-Driven Security:** The user pepper used for HMAC is pulled from environment- or settings-based configuration, in line with 12-factor and microservices best practices.
- **Stateless Scaling:** All routines work without database state, enabling horizontal scaling and easy migration between environments.

Intended Usage:
---------------
- Used during user registration/creation to initialize the salt and build a safe, opaque user identifier.
- Integrated into authentication, onboarding flows, or downstream service orchestration where user IDs must be collision-safe and privacy-preserving.

Dependencies:
-------------
- Python standard library: `secrets`, `hashlib`, `hmac`
- Application settings module (for secret pepper configuration)

Security and Best Practices:
----------------------------
- All salts and user IDs are generated with cryptographic randomness or secure HMAC algorithms.
- The secret pepper must be stored securely (not in code, preferably in environment or a secrets vault).

"""

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
