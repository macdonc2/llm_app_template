import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load .env from project root so DATABASE_URL is available
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(dotenv_path=os.path.join(project_root, ".env"))

# Ensure DATABASE_URL is set 
raw_db_url = os.getenv("DATABASE_URL")
if not raw_db_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# If it's the async URL, swap to the sync driver for Alembic
if raw_db_url.startswith("postgresql+asyncpg://"):
    sync_db_url = raw_db_url.replace("postgresql+asyncpg://", "postgresql://", 1)
else:
    sync_db_url = raw_db_url

# Make your app’s code importable
sys.path.insert(0, os.path.join(project_root, "src"))

# Alembic Config object, reading alembic.ini by default
config = context.config

# Override the URL in alembic.ini with our sync URL
config.set_main_option("sqlalchemy.url", sync_db_url)

# (Optional) set up Python logging from the ini file 
try:
    fileConfig(config.config_file_name)
except Exception:
    pass

# Import your models’ metadata for ‘autogenerate’
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
    """Run migrations in 'online' mode (with a live DB connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # compare types so ALTER TYPE-diffs are detected
            compare_type=True,
            # render batch mode (needed if you ever migrate SQLite or do complex ALTERs)
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()


# Dispatch to offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
