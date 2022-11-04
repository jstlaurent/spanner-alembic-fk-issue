import os
from logging.config import fileConfig

from alembic import context
from alembic.ddl.impl import DefaultImpl

from demo import models
from demo.config import settings


class SpannerImpl(DefaultImpl):
    """Makes dialect discoverable by alembic"""

    __dialect__ = 'spanner+spanner'


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the environment variable for the database name
os.environ['SPANNER_DATABASE'] = config.config_ini_section

# Load and set any additional environment variables
env_section = config.get_section(f'{config.config_ini_section}_env', {})
for key, value in env_section.items():
    os.environ[key] = value

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = models.Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.SPANNER_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = target_metadata.bind

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
            version_table_pk=False,
            transaction_per_migration=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
