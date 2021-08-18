'''
usage: inactive [-h] [-c CHAT] [-n INACTIVE] [-l LIMIT]

    -h, --help                  help message
    -c <chat>, --chat <chat>    chat to scan [default: current]
    -n <n>, --inactive <n>      number of most inactive users to show [default: 8]
    -l <l>, --limit <l>         number of members to be retrieved
'''

import time
import timeago

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.utils import get_channel_id
from .utils import edrep, mefilter, code

from docopt import docopt, DocoptExit


@Client.on_message(mefilter('inactive'))
async def _(cl: Client, msg: Message):
    text = await get_inactive(cl, msg)
    await edrep(msg, text=text)


async def get_inactive(cl: Client, msg: Message):
    try:
        a = docopt(__doc__, argv=msg.command[1:], help=False)
    except DocoptExit as e:
        return f'<pre>{e.usage}</pre>'

    if a['--help']:
        return f'<pre>{__doc__.strip()}</pre>'

    inactive = int(a['--inactive'])
    limit = int(a['--limit']) if a['--limit'] else 0
    chat = msg.chat

    if a['--chat'][0] == '@':
        chat = await cl.get_chat(a['--chat'])
    elif a['--chat'][1:].isdigit():
        chat = await cl.get_chat(int(a['--chat']))
    else:
        return code(f"--chat == {a['--chat']}")

    await msg.edit(f'scanning chat "{chat.title}"...')
    start = time.time()

    messages = [m
                async for member in cl.iter_chat_members(chat.id, limit=limit, filter='recent')
                if not member.user.is_deleted
                async for m in cl.search_messages(chat.id, limit=1, from_user=member.user.id)]

    delta = time.time() - start
    messages.sort(key=lambda k: k['date'])

    if inactive > 0:
        messages = messages[:inactive]

    return '\n'.join([
        f'{m.from_user.mention}\'s last <a href="https://t.me/c/{get_channel_id(m.chat.id)}/{m.message_id}">message</a> was {timeago.format(m.date)}'
        for m in messages
    ] + [f'<code>{int(delta * 1000)}ms</code>'])
