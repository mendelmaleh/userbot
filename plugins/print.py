from html import escape

from pyrogram import Client, Message
from .utils import mefilter


@Client.on_message(mefilter('print'))
async def _(cl, msg: Message):
    m = msg.reply_to_message or msg # or copy.copy(msg)\n del m.from_user

    if len(msg.command) > 1:
        if msg.command[1] == 'timestamp':
            m = m['date']
        if msg.command[1] == 'chatmember':
            m = await cl.get_chat_member(m.chat.id, m.from_user.id)

    await msg.edit(text='<pre>' + escape(str(m)) + '</pre>', parse_mode='html')
