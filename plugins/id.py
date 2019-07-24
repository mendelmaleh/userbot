import argparse
from pyrogram import Client, Filters, Message
from .shared import cmd_filter

@Client.on_message(cmd_filter('id') & Filters.me)
async def _(cl: Client, msg: Message):
    p = argparse.ArgumentParser()
    p.add_argument('-x', '--hex', action='store_true')

    e = p.add_mutually_exclusive_group()
    e.add_argument('-c', '--chat', action='store_true')
    e.add_argument('-m', '--me', action='store_true')
    e.add_argument('-r', '--replied', action='store_true')
    e.add_argument('-f', '--forwarded', action='store_true')

    a = p.parse_args(msg.command[1:])

    if a.me:
        u = await cl.get_me()
        id = u.id
    elif a.replied:
        if msg.reply_to_message:
            id = msg.reply_to_message.from_user.id
        else:
            err = "msg.rtm is None"
    elif a.forwarded:
        if msg.reply_to_message.forward_from_chat:
            id = msg.reply_to_message.forward_from_chat.id
        elif msg.reply_to_message.forward_from:
            id = msg.reply_to_message.forward_from.id
        else:
            err = "msg.rtm is not a forwarded msg"
    else:
        id = msg.chat.id

    try:
        if a.hex: id = hex(id)
        text = f'<code>{id}</code>'
    except NameError:
        text = f'<i>{err}</i>'

    await msg.edit_text(text)
