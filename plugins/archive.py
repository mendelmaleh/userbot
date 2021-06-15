import asyncio

from pyrogram import Client
from pyrogram.types import Message
from .utils import mefilter


@Client.on_message(mefilter('archive'))
async def _(_, msg: Message):
    try:
        ok = await msg.chat.archive()
    except Exception as e:
        await msg.edit(f'error:\n<code>{e}</code>')
    else:
        msg = await msg.edit(f'returned <code>{ok}</code>')
        await asyncio.sleep(5)
        await msg.delete()
