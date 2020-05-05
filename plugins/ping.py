import time, asyncio

from pyrogram import Client, Message
from .utils import mefilter

async def ping(_, msg: Message):

@Client.on_message(mefilter('ping'))
    start = time.time()
    await msg.edit('...')
    delta = time.time() - start

    await msg.edit(f'`{int(delta * 1000)}ms`')
