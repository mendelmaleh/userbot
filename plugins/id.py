'''
usage: id [-h] [-x | -b | -p] [-c | -m | -r | -f]

  -h, --help        help message

  -x, --hex         id in hex
  -b, --bin         id in binary
  -p, --permalink   id as permalink

  -c, --chat        chat id (default)
  -m, --me          user id
  -r, --replied     sender from rtm
  -f, --forwarded   'forwarded from' from rtm
'''

from pyrogram import Client, Message, User, Chat
from docopt import docopt, DocoptExit

from .utils import edrep, gefilter, err


@Client.on_message(gefilter('id'))
async def _(_, msg: Message):
    text = await get_id(msg)
    await edrep(msg, text=text)


async def get_id(msg: Message):
    try:
        a = docopt(__doc__, argv=msg.command[1:], help=False)
    except DocoptExit as e:
        return f'<pre>{e.usage}</pre>'

    if a['--help']:
        return f'<pre>{__doc__.strip()}</pre>'

    if a['--me']:
        chat = msg.from_user
    elif a['--replied']:
        if msg.reply_to_message:
            chat = msg.reply_to_message.from_user
        else:
            return err('msg.rtm is None')
    elif a['--forwarded']:
        if msg.reply_to_message.forward_from_chat:
            chat = msg.reply_to_message.forward_from_chat
        elif msg.reply_to_message.forward_from:
            chat = msg.reply_to_message.forward_from
        else:
            return err('msg.rtm is not a forwarded msg')
    else:
        chat = msg.chat

    if a['--hex']:
        return f'<code>{hex(chat.id)}</code>'

    if a['--bin']:
        return f'<code>{bin(chat.id)}</code>'

    if a['--permalink']:
        if (type(chat) == Chat and chat.type == 'private') or (type(chat) == User and not chat.is_bot):
            return f'permalink for <a href=tg://user?id={chat.id}>{chat.id}</a>'
        return err('permalink available only for users')

    return f'<code>{chat.id}</code>'
