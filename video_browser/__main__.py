"""Container Launcher CLI interface."""
import asyncio
import logging

from importlib import resources
from sqlalchemy.ext.asyncio import AsyncEngine
from typer import Typer

from video_browser.__about__ import __version__
from video_browser.models import get_engine
from video_browser.settings import settings


if settings.dev:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARN)

logger = logging.getLogger(__name__)
app = Typer()


async def execute_setup(drop_existing: bool = False, rerun_last: bool = False) -> None:
    """Run as an async command."""
    from alembic.config import Config
    from alembic import command

    alembic_config = Config()
    alembic_config.set_main_option("script_location", str(resources.files("video_browser") / "alembic"))
    alembic_config.set_main_option("sqlalchemy.url", str(settings.dsn))

    def sync_db_ops(conn: AsyncEngine) -> None:
        """Run the commands synchronously."""
        try:
            alembic_config.attributes["connection"] = conn
            if drop_existing:
                logger.debug("Removing existing tables")
                command.downgrade(alembic_config, "base")
            elif rerun_last:
                logger.debug("Reverting the last upgrade")
                command.downgrade(alembic_config, "-1")
            logger.debug("Running upgrade")
            command.upgrade(alembic_config, "head")
        except Exception as e:  # noqa: cov
            logger.error(e)

    async with get_engine().begin() as conn:
        await conn.run_sync(sync_db_ops)


@app.command()
def setup(drop_existing: bool = False, rerun_last: bool = False) -> None:
    """Set up the database."""
    asyncio.run(execute_setup(drop_existing=drop_existing, rerun_last=rerun_last))


@app.command()
def version() -> None:
    """Output the current version."""
    print(__version__)


if __name__ == "__main__":
    app()
