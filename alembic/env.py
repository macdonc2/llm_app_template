import os
import sys

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv

# Load environment variables from .env file in the project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Optional: raise error if DATABASE_URL is still not set
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL environment variable is not set")

# 1) Ensure Alembic can import your “app” package under /app/src
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

# 2) Alembic Config object — reads alembic.ini by default from CWD (/app)
config = context.config

# ──────────────────────────────────────────────────────────────────────────────
# 3) Override the URL in alembic.ini with the in-cluster DATABASE_URL
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")
config.set_main_option("sqlalchemy.url", db_url)
# ──────────────────────────────────────────────────────────────────────────────

# 4) (Optional) configure Python logging via alembic.ini’s [loggers]/[handlers]/[formatters]
try:
    fileConfig(config.config_file_name)
except KeyError:
    # if your alembic.ini is missing [formatters], just skip logging setup
    pass

# 5) Point Alembic at your models’ metadata for autogeneration
from app.models import Base  # adjust if your Base lives elsewhere
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode (no DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode (with DB connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# 6) Dispatch to the correct mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
