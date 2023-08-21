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
    # the file should be edited in last 5 hours
    if p.stat().st_mtime < time.time() - 5 * 3600:
        info = f"{p} is not edited for at least 5 hours"
        logger.info(info)
        wan.ntf(info)
    else:
        logger.info("It is edited recently")


@app.command()
def start_teleread(channel: str, dirname: str, reg: Optional[str] = None, watch: bool = True) -> None:
    from misc.teleread.server import FileManager

    if watch:
        FileManager(channel, dirname, reg).start()
    else:
        FileManager(channel, dirname, reg).update()


@app.command()
def locate(module: str) -> None:
    locate_pack(module)


@app.command()
def notion_routine():
    import requests
    from settings import NOTIONSETTINGS

    def edit_page(page_block_id, data: dict):
        edit_url = f"https://api.notion.com/v1/blocks/{page_block_id}/children"

        payload = data

        res = requests.patch(edit_url, headers=headers, json=payload)
        if res.status_code == 200:
            print(f"{res.status_code}: Page edited successfully")
        else:
            print(f"{res.status_code}: Error during page editing")
        return res

    headers = {
        "Authorization": "Bearer " + NOTIONSETTINGS.secrets,
        "Content-Type": "application/json",
        "Notion-Version":
            "2022-06-28",  # Check what is the latest version here: https://developers.notion.com/reference/changes-by-version
    }

    import datetime
    cn_time_str = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d")

    def get_text(text=""):
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": text,
                    },
                },]
            },
        }

    blocks = {
        "children": [
            get_text(f"## {cn_time_str}"),
            get_text(),
        ],
        "after": NOTIONSETTINGS.page_pos_id,  # adjusting the position of the content.
    }
    # NOTE: Notino's will add part of the page name into url. But it is not the page id.
    page_block_id = NOTIONSETTINGS.page_id

    edit_page(page_block_id, blocks)


typer_click_object = typer.main.get_command(app)

if __name__ == "__main__":
    app()  # pragma: no cover
