"""Settings Module."""
import logging
from logging import getLevelName
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Project specific settings."""

    logging_level: Optional[str] = getLevelName(logging.INFO)

    class Config:
        """Config for settings."""

        env_prefix = "MISC_"


class GlobalSettings(BaseSettings):
    """System level settings."""

    ci: bool = False


class TeleRead(BaseSettings):
    """Telegram settings."""

    api_hash: str
    app_id: int

    data_dir: str


class Notion(BaseSettings):
    """Notion settings."""

    secrets: str
    page_id: str  # the page to be edited
    page_pos_id: str  # the position of the page to be edited


#: Instance for project specific settings.
settings = Settings()

#: Instance for system level settings.
global_settings = GlobalSettings()


def get_env_file(name: str) -> Optional[str]:
    """Get the environ path from dot directory."""
    _env_file = f"~/.dotfiles/{name}"
    if Path(_env_file).expanduser().exists():
        logging.warning("loading environtment file from `%s`", _env_file)
    else:
        _env_file = None
    return _env_file


TELEREADSETTINGS = TeleRead(_env_file=get_env_file(".teleread"))
NOTIONSETTINGS = Notion(_env_file=get_env_file(".notion"))
