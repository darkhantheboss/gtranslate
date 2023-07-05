from logging.config import fileConfig

from aiomysql.sa import Engine
from alembic import context

from helpers.engine import mysql_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from helpers.entity.sql import Base
from settings import build_sqlalchemy_database_uri

import models  # noqa: F401, F403 isort:skip No error! pylint: disable=unused-import


config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# WARNING: Replacing % to %% is a requirement for ConfigParser to not fail.
config.set_main_option("sqlalchemy.url", build_sqlalchemy_database_uri().replace("%", "%%"))
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    def do_migrations(connection: Engine) -> None:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

    async with mysql_engine.connect() as db_connection:
        await db_connection.run_sync(do_migrations)

    await mysql_engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
