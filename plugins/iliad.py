from pyrogram import Client
from pyrogram.types import Message
from .utils import code, config, mefilter

import iliad

if "iliad" in config:

    @Client.on_message(mefilter("iliad"))
    async def _(_, msg: Message):
        user = await iliad.get(config["iliad"]["user"], config["iliad"]["pass"])
        await msg.edit(code(f"data: {user.local.data} / {user.local.data_limit}"))
