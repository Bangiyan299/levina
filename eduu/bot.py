import logging
import time

import pyrogram
from pyrogram import Client, __version__
from pyrogram.enums import ParseMode
from pyrogram.errors import BadRequest
from pyrogram.raw.all import layer

import eduu
from eduu.config import API_HASH, API_ID, disabled_plugins, log_chat, TOKEN, WORKERS
from eduu.utils.utils import shell_exec

logger = logging.getLogger(__name__)


class Eduu(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            name=name,
            app_version=f"GuardBot v{eduu.__version__}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=TOKEN,
            parse_mode=ParseMode.HTML,
            workers=WORKERS,
            plugins=dict(root="eduu.plugins", exclude=disabled_plugins),
            sleep_threshold=180,
        )

    async def start(self):
        await super().start()

        # self.version_code = int((await shell_exec("git rev-list --count HEAD"))[0])
        self.me = await self.get_me()
        self.start_time = time.time()

        logger.info(
            "GuardBot running with Pyrogram v%s (Layer %s) started on @%s. Hi!",
            __version__,
            layer,
            self.me.username,
        )

        from eduu.database.restarted import del_restarted, get_restarted

        wr = await get_restarted()
        await del_restarted()

        start_message = (
            "✅ <b>GuardBot started!</b>\n\n"
            f"🔖 <b>Version:</b> <code>v{eduu.__version__} (753)</code>\n"
            f"🔥 <b>Pyrogram:</b> <code>v{pyrogram.__version__}</code>"
        )

        try:
            await self.send_message(chat_id=log_chat, text=start_message)
            if wr:
                await self.edit_message_text(
                    wr[0], wr[1], text="Bot has rebooted!"
                )
        except BadRequest:
            logger.warning("Unable to send message to log_chat.")

    async def stop(self):
        await super().stop()
        logger.warning("GuardBot stopped, Bye!")
