from pyrogram import Client
from pyrogram.types import Message
from .utils import code, mefilter


@Client.on_message(mefilter('print'))
async def _print(cl: Client, msg: Message):
    m = msg.reply_to_message or msg # or copy.copy(msg)\n del m.from_user

    if len(msg.command) > 1:
        if msg.command[1] == 'timestamp':
            m = m['date']
        if msg.command[1] == 'markup':
            m = m['reply_markup']
        if msg.command[1] == 'entities':
            m = m['entities']
        if msg.command[1] == 'restrictions':
            m = m.chat.restrictions or m.forward_from_chat.restrictions
        if msg.command[1] == 'chatmember':
            m = await cl.get_chat_member(m.chat.id, m.from_user.id)

    print(m)
    await msg.edit(text=code(m))
