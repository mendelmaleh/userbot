from html import escape

from pyrogram import Client
from pyrogram.types import Message
from .utils import edrep, gefilter

from docopt import DocoptExit
from wttr import wttr


@Client.on_message(gefilter('wttr'))
async def weather(cl: Client, msg: Message):
    args = msg.command[1:]
    defs = {
        '--days': 0,
        '--narrow': True,
        '--no-terminal': True,
        '<location>': 'New York',
    }

    try:
        wt = await wttr(args, defs)
    except DocoptExit as e:
        wt = e.usage

    text = f'<pre>{escape(wt)}</pre>‎'
    await edrep(msg, text=text, quote=False)
