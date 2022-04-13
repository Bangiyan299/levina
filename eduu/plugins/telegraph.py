from pyrogram.types import Message
from pyrogram import Client, filters

from eduu.config import prefix
from eduu.utils import commands, http
from eduu.utils.localization import use_chat_lang


@Client.on_message(filters.command(["telegraph", "tgm"], prefix))
@use_chat_lang()
async def telegraph(c: Client, m: Message, strings):
    if m.reply_to_message:
        if (
            m.reply_to_message.photo
            or m.reply_to_message.video
            or m.reply_to_message.document
            or m.reply_to_message.animation
        ):
            d_file = await m.reply_to_message.download()
            response = await http.post(
                "https://telegra.ph/upload", files={"upload-file": open(d_file, "rb")}
            )
            tele_link = "https://telegra.ph" + response.json()[0]["src"]

            await m.reply_text(tele_link)
    else:
        await m.reply_text(strings("telegraph_err_no_reply"))


commands.add_command("telegraph", "tools")
