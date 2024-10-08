"""Command Line Interface."""
import time
from pathlib import Path
from typing import Optional

import typer
import wan
from loguru import logger

from misc.incu.pack import locate_pack

app = typer.Typer()


@app.command()
def run() -> None:
    """Run command."""


@app.command()
def check_health(p: Path) -> None:
    """Check the health of a specific service.

    - the file should be edited in last 5 hours fi the service is alive.
    """
    if p.stat().st_mtime < time.time() - 5 * 3600:
        info = f"{p} is not edited for at least 5 hours"
        logger.info(info)
        wan.ntf(info)
    else:
        logger.info("It is edited recently")


@app.command()
def start_teleread(
    channel: str,
    dirname: str,
    *,
    reg: Optional[str] = None,
    watch: bool = True,
    days: int = 60,
) -> None:
    """Tele read service."""
    from misc.teleread.server import FileManager
    from telethon.errors import TimedOutError

    if watch:
        while True:
            try:
                FileManager(channel, dirname, reg, days=days).start()
            except TimedOutError:
                print("TimedOutError: The request to the server timed out.")
            time.sleep(60)
    else:
        FileManager(channel, dirname, reg, days=days).update()


@app.command()
def locate(module: str) -> None:
    """Locate a package to find where it is installed."""
    locate_pack(module)


@app.command()
def notion_routine() -> None:
    """Routines for my notion."""
    import requests
    from settings import NOTIONSETTINGS

    headers = {
        "Authorization": "Bearer " + NOTIONSETTINGS.secrets,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",  # Check what is the latest version here: https://developers.notion.com/reference/changes-by-version
    }

    def edit_page(page_block_id: str, data: dict) -> None:
        edit_url = f"https://api.notion.com/v1/blocks/{page_block_id}/children"

        payload = data

        res = requests.patch(edit_url, headers=headers, json=payload, timeout=30)
        if res.ok:
            logger.info(f"{res.status_code}: Page edited successfully")
        else:
            logger.info(f"{res.status_code}: Error during page editing")

    import datetime

    cn_time_str = (
        datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=8)
    ).strftime("%Y-%m-%d")

    def get_text(text: str = "") -> dict:
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text,
                        },
                    },
                ],
            },
        }

    blocks = {
        "children": [
            get_text(f"## {cn_time_str}"),
            get_text(),
        ],
        "after": NOTIONSETTINGS.page_pos_id,  # adjusting the position of the content.
    }
    page_block_id = NOTIONSETTINGS.page_id

    edit_page(page_block_id, blocks)


typer_click_object = typer.main.get_command(app)

if __name__ == "__main__":
    app()  # pragma: no cover
