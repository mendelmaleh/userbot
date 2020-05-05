import asyncio

from pyrogram import Client, Filters

from .utils import config, isnumber, awall, mefilter

welcome_chats = [int(c) if isnumber(c) else c for c in config['welcome']['chats'].split()]
welcome = ['👋‎', '✋‎']


@Client.on_message(Filters.new_chat_members & Filters.chat(welcome_chats) | mefilter('hi'))
async def _(cl, msg):
    w = await cl.send_message(
        chat_id=msg.chat.id,
        text=welcome[0]
    )

    if msg.from_user.is_self:
        await msg.delete()

    for i in range(2):
        await awall(asyncio.sleep(1/4), w.edit(welcome[1]))
        await awall(asyncio.sleep(1/4), w.edit(welcome[0]))

    await awall(asyncio.sleep(1), w.delete())
