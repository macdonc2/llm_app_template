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
