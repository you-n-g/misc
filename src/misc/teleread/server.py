# https://github.com/LonamiWebs/Telethon
# How to autodownload file in telegram with Python
# TODO:
# - It seems I have to verify when starting ...  I'm not sure if it is by design.

from datetime import datetime, timedelta, timezone
from pathlib import Path

from telethon import TelegramClient, events

from misc.settings import TELEREADSETTINGS


def get_client():
    return TelegramClient("CaiXin", TELEREADSETTINGS.app_id, TELEREADSETTINGS.api_hash)


CHANNEL = "https://t.me/keeplovess"


async def download_message_media(message):
    date_str = message.date.strftime("%Y-%m-%d %H:%M:%S")
    fname = None
    for at in message.media.document.attributes:
        fname = f"{date_str} {at.file_name}"
        break
    assert fname is not None

    data_dir = Path(TELEREADSETTINGS.data_dir).expanduser()
    data_dir.mkdir(parents=True, exist_ok=True)
    target_path = data_dir / fname
    if target_path.exists():
        print(f"skip {fname}")
    else:
        print(f"downloading {fname}")
        path = await message.download_media()
        Path(path).rename(target_path)


async def update_data_to_recent():
    """
    If you want to run this function in a script, you can follow the code below.

    with client:
        client.loop.run_until_complete(update_data_to_recent())
    """
    client = get_client()
    async for message in client.iter_messages(CHANNEL):
        if datetime.now(tz=timezone.utc) - message.date > timedelta(days=60):
            break

        await download_message_media(message)


async def my_event_handler(event):
    if event.message.file:
        await download_message_media(event.message)


def start_client():
    client = get_client()
    client.on(events.NewMessage(chats=CHANNEL))(my_event_handler)
    client.start()
    client.run_until_disconnected()
