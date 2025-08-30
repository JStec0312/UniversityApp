# migrations/env.py
import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine
from app.core.db import Base

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

DB_URL = os.getenv("DB_URL", "postgresql+psycopg://user:pass@localhost:5432/dbname")
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine = create_engine(DB_URL)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
