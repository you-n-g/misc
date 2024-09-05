# https://github.com/LonamiWebs/Telethon
# How to autodownload file in telegram with Python
# TODO:
# - It seems I have to verify when starting ...  I'm not sure if it is by design.

from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import yaml
from typing import Optional

import telethon
from telethon import TelegramClient, events
from telethon.errors import MsgIdInvalidError, TimedOutError
from telethon.types import MessageMediaDocument, DocumentAttributeFilename

from misc.settings import TELEREADSETTINGS


class FileManager:

    def __init__(self, channel: str, dirname: str, reg: Optional[str] = None, days: int = 60) -> None:
        self.channel, self.dirname = channel, dirname
        self.reg = re.compile(reg) if reg is not None else None
        # You will prompt to input your +86 phone. And then your telegram will receive a code.
        self.client = self.get_client(dirname)  # TODO: why can't I share clients
        self.days = days  # when updating records. How many days do we go back?

    @staticmethod
    def get_client(dirname):
        return TelegramClient(dirname, TELEREADSETTINGS.app_id, TELEREADSETTINGS.api_hash)

    async def download_message_media(self, message):
        if message.media is None or not isinstance(message.media, MessageMediaDocument):
            print("No document found")
            return
        date_str = message.date.strftime("%Y-%m-%d %H:%M:%S")
        at, fname = None, None
        for at in message.media.document.attributes:
            if isinstance(at, DocumentAttributeFilename):
                fname = f"{date_str} {at.file_name}"
                break
        if fname is None:
            return # if the media does not have filename, we skip it.
        assert fname is not None
        assert at is not None

        data_dir = (Path(TELEREADSETTINGS.data_dir) / self.dirname).expanduser()
        data_dir.mkdir(parents=True, exist_ok=True)
        target_path = data_dir / fname
        if target_path.exists():
            print(f"skip {fname}")
        elif self.reg is not None and self.reg.match(at.file_name) is None:
            print(f"skip {fname} due to fail to match {self.reg}")
        else:
            # # Forward the message to chat_id
            # config_path: str = "~/.dotfiles/.notifiers.yaml"
            # path = Path(config_path).expanduser()
            # with path.open() as f:
            #     config = yaml.load(f, Loader=yaml.FullLoader)
            # chat_id = int(config["kwargs"]["chat_id"])
            # # TODO: get EntityLike object based on chat_id
            # entity = await self.client.get_entity()
            try:
                entity = await self.client.get_me()
                await self.client.forward_messages(entity, message)
                print(f"Message forwarded to {entity}")
            except Exception as e:
                print(f"Failed to forward message: {e}")

            print(f"downloading {fname}")
            # NOTE: we have to add a progress_callback in case of Timedout error..
            import time
            last_current = 0
            last_time = time.time()
            def progress_callback(current, total):
                nonlocal last_current, last_time
                now = time.time()
                speed = round(((current-last_current)/(now-last_time))/1000)
                last_current = current
                last_time = now
                percent = int((current/total)*100)
                print('\r{} % .... {} KB/s'.format(percent, speed), end='')
                if percent == 100:
                    print()
            for i in range(3):
                try:
                    path = await message.download_media(progress_callback=progress_callback)
                    Path(path).rename(target_path)
                    break
                except TimedOutError as e:
                    print(f"Error: {e}")
                    print(f"Retry {i+1} times")

    async def update_data_to_recent(self):
        """If you want to run this function in a script, you can follow the code below.

        with client:
            client.loop.run_until_complete(update_data_to_recent())
        """
        async for message in self.client.iter_messages(self.channel):
            if datetime.now(tz=timezone.utc) - message.date > timedelta(days=self.days):
                break
            # Get replies and walk through them
            try:
                async for rm in self.client.iter_messages(self.channel, reply_to=message.id):
                    await self.download_message_media(rm)
            except MsgIdInvalidError:
                print("Invalid message id; Skip walking replies.")
            await self.download_message_media(message)

    async def new_message_handler(self, event):
        # The file is now in the comments now.
        # if event.message.file:
        #     await self.download_message_media(event.message)
        await self.update_data_to_recent()

    def start(self):
        self.client.on(events.NewMessage(chats=self.channel))(self.new_message_handler)
        self.client.start()
        print("run_until_disconnected")
        self.client.run_until_disconnected()

    def update(self):
        with self.client:
            self.client.loop.run_until_complete(self.update_data_to_recent())
