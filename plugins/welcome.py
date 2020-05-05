import asyncio

from pyrogram import Client, Filters

from .utils import config, isnumber, awall, mefilter

welcome_chats = [int(c) if isnumber(c) else c for c in config['welcome']['chats'].split()]
welcome = ['👋‎', '✋‎']


@Client.on_message(Filters.new_chat_members & Filters.chat(welcome_chats) | mefilter('hi'))
async def _(cl, msg):
    msg = await cl.send_message(
        chat_id=msg.chat.id,
        text=welcome[0]
    )

    for i in range(2):
        await awall(asyncio.sleep(1/4), msg.edit(welcome[1]))
        await awall(asyncio.sleep(1/4), msg.edit(welcome[0]))

    await awall(asyncio.sleep(2), msg.delete())
