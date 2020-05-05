from html import escape

from pyrogram import Client, Message
from .utils import mefilter


@Client.on_message(mefilter('print'))
async def _(_, msg: Message):
    m = msg.reply_to_message or msg # or copy.copy(msg)\n del m.from_user
    await msg.edit(text='<pre>' + escape(str(m)) + '</pre>', parse_mode='html')
