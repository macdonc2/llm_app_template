"""
models.py

This module defines the SQLAlchemy ORM layer for the user domain in a microservices-based
FastAPI application. It includes the declarative SQLAlchemy base, a secure salt generator,
and an extensible User model that integrates with the fastapi-users authentication framework.
The model is designed for scalability, security, and smooth integration into distributed, 
cloud-native service architectures.

Overview:
---------
- Initializes the declarative base (`Base`) for all ORM models in the service.
- Declares a cryptographically secure function for generating password salts.
- Defines the `User` model, which:
    * Inherits user table structure, UUID primary key logic, and authentication fields from FastAPI Users.
    * Stores per-user API keys for integration with external services (e.g., OpenAI, Tavily).
    * Implements custom fields and constraints for full-stack secure user management.

Key Features:
-------------
- **UUID-Based Identity:** Supports global uniqueness for users, facilitating cross-service identity management and data federation in microservices architectures.
- **Secure Password Salt:** Automatically assigns a random, cryptographically secure salt string to each user for protection against rainbow tables and credential leaks.
- **Pluggable API Key Storage:** Can store encrypted or plain API keys per provider, allowing for personalized AI and search tool usage at the user level.
- **Extensible via Declarative Base:** Central `Base` can be reused and extended for all domain models in the microservices suite.

Intended Usage:
---------------
- Used as the primary ORM model for user management, authentication, and federation.
- Passed to, and consumed by, user repository, auth, and service layers for persistence and access control.
- Compatible with fastapi-users out-of-the-box for rapid, standards-compliant authentication flows.

Dependencies:
-------------
- SQLAlchemy ORM (async or sync compatible)
- FastAPI-Users (for advanced user CRUD/auth management)
- Python standard library: secrets (for salt generation)

Security Considerations:
------------------------
- Password salting is automatic and unique per user, mitigating credential-reuse attacks.
- Per-user third-party credentials can be securely managed using environment or vault-based encryption extensions.

"""

import secrets
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

Base = declarative_base()

def generate_salt() -> str:
    # 32-byte hex string
    return secrets.token_hex(16)


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Represents a user in the application.

    Inherits from SQLAlchemyBaseUserTableUUID and Base.
    Stores credentials and API keys for OpenAI and Tavily access.

    Attributes:
        salt (str): Salt used for secure password hashing.
        openai_api_key (str, optional): OpenAI API key for user integration.
        tavily_api_key (str, optional): Tavily API key for user integration.
    """
     
    __tablename__ = "users"

    salt = sa.Column(
        sa.String(32),
        default=generate_salt,
        nullable=False,
    )

    openai_api_key = sa.Column(sa.String(255), nullable=True)
    tavily_api_key = sa.Column(sa.String(255), nullable=True)
    firecrawl_api_key = sa.Column(sa.String(255), nullable=True)
