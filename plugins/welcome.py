import asyncio

from pyrogram import Client, Filters

chats = [-1001221450384, -1001372920765]
welcome = ['👋‎', '✋‎']

@Client.on_message(Filters.new_chat_members & Filters.chat(chats))
async def _(cl, msg):
    msg = await cl.send_message(
        chat_id=msg.chat.id,
        text=welcome[0]
    )

    for i in range(2):
        await awall(asyncio.sleep(1/4), msg.edit(welcome[1]))
        await awall(asyncio.sleep(1/4), msg.edit(welcome[0]))

    await awall(asyncio.sleep(2), msg.delete())
