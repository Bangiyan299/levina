from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from utils import commands
from localization import use_chat_lang


def gen_categories_kb(strings_manager):
    categories = list(commands.commands)
    kb = []
    while categories:
        name = strings_manager(categories[0], context="cmds_list")
        a = [InlineKeyboardButton(name,
                                  callback_data="view_category "+categories[0])]
        categories.pop(0)
        if categories:
            name = strings_manager(categories[0], context="cmds_list")
            a.append(InlineKeyboardButton(name,
                                          callback_data="view_category "+categories[0]))
            categories.pop(0)
        kb.append(a)
    return kb


@Client.on_callback_query(filters.regex("^commands$"))
@use_chat_lang()
async def cmds_list(c: Client, m: CallbackQuery, strings):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        *gen_categories_kb(strings),
        [InlineKeyboardButton(strings("back_btn", context="general"), callback_data="start_back")]
    ])
    await m.message.edit_text(strings("select_command_category"), reply_markup=keyboard)


@Client.on_callback_query(filters.regex("^view_category .+"))
@use_chat_lang()
async def get_category(c: Client, m: CallbackQuery, strings):
    msg = commands.get_commands_message(strings, m.data.split(maxsplit=1)[1])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(strings("back_btn", context="general"), callback_data="commands")]
    ])
    await m.message.edit_text(msg, reply_markup=keyboard)
