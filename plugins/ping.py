import time

from pyrogram import Client, Message
from .utils import mefilter


@Client.on_message(mefilter('ping'))
async def _(_, msg: Message):
    start = time.time()
    await msg.edit('...')
    delta = time.time() - start

    await msg.edit(f'<code>{int(delta * 1000)}ms</code>')
