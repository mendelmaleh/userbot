from html import escape

from pyrogram import Client
from pyrogram.types import Message
from .utils import mefilter


@Client.on_message(mefilter('print'))
async def _(cl: Client, msg: Message):
    m = msg.reply_to_message or msg # or copy.copy(msg)\n del m.from_user

    if len(msg.command) > 1:
        if msg.command[1] == 'timestamp':
            m = m['date']
        if msg.command[1] == 'restrictions':
            m = m.chat.restrictions or m.forward_from_chat.restrictions
        if msg.command[1] == 'chatmember':
            m = await cl.get_chat_member(m.chat.id, m.from_user.id)

    print(m)
    await msg.edit(text='<pre>' + escape(str(m)) + '</pre>')


@Client.on_message(mefilter('chat'))
async def _(cl: Client, msg: Message):
    chat_id = msg.command[1]
    if chat_id.startswith("-100"):
        chat_id = int(msg.command[1])

    chat = await cl.get_chat(chat_id)
    print(chat)
    await msg.edit(text='<pre>' + escape(str(chat)) + '</pre>')
