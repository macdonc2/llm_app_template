import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.String(64), primary_key=True, index=True)
    email = sa.Column(sa.String, unique=True, nullable=False, index=True)
    salt = sa.Column(sa.String(32), nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    openai_api_key = sa.Column(sa.String(255), nullable=True)
