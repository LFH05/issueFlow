from alembic.config import Config
from sqlalchemy import inspect

from alembic import command


def test_migrations_upgrade_downgrade_reupgrade(alembic_config: Config, test_engine) -> None:
    command.downgrade(alembic_config, "base")
    assert "users" not in inspect(test_engine).get_table_names()

    command.upgrade(alembic_config, "head")
    assert "users" in inspect(test_engine).get_table_names()

    command.downgrade(alembic_config, "base")
    assert "users" not in inspect(test_engine).get_table_names()

    command.upgrade(alembic_config, "head")
    assert "users" in inspect(test_engine).get_table_names()
