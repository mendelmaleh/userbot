import time, asyncio

from pyrogram import Client, Message
from .utils import gefilter

@Client.on_message(gefilter('ping'))
async def ping(_, msg: Message):
    start = time.time()
    await msg.edit('...')
    delta = time.time() - start

    await msg.edit(f'`{int(delta * 1000)}ms`')
