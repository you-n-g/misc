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


#: Instance for project specific settings.
settings = Settings()

#: Instance for system level settings.
global_settings = GlobalSettings()

_env_file = "~/.dotfiles/.teleread"
if Path(_env_file).expanduser().exists():
    logging.warning(f"loading environtment file from `{_env_file}`")
else:
    _env_file = None
TELEREADSETTINGS = TeleRead(_env_file=_env_file)
