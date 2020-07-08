from pyrogram import Client, Message
from .utils import mefilter

import timeago


@Client.on_message(mefilter('inactive'))
async def _(cl: Client, msg: Message):
    await msg.edit('...')

    await msg.edit(text='\n'.join([
        f'{m.from_user:mention}\'s last <a href="https://t.me/c/{int(m.chat.id + 100e10) * -1}/{m.message_id}">message</a> was {timeago.format(m.date)}'
        for m in sorted(
            [m async for member in cl.iter_chat_members(msg.chat.id) async for m in cl.search_messages(msg.chat.id, limit=1, from_user=member.user.id)],
            key=lambda k: k['date']
        )[:5]
    ]), parse_mode='html')
