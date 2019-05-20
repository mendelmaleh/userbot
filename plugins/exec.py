from pyrogram import Client, Filters
from contextlib import redirect_stdout
from functools import partial
from cgi import escape
from io import StringIO
import re

from .shared import cmd_filter

RUNNING = "<b>Exec:</b>\n<code>{}</code>\n<b>Running...</b>"
ERROR = "<b>Exec:</b>\n<code>{}</code>\n<b>Error:</b>\n<code>{}</code>"
SUCCESS = "<b>Exec:</b>\n<code>{}</code>\n<b>Success</b>"
RESULT = "<b>Exec:</b>\n<code>{}</code>\n<b>Result:</b>\n<code>{}</code>"


@Client.on_message(Filters.me & cmd_filter('exec'))
def _(client, message):
    exp = ' '.join(message.command[1:])
    edit = partial(
            client.edit_message_text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            parse_mode='html'
    )

    edit(text=RUNNING.format(exp))

    try:
        with StringIO(newline='\n') as buf, redirect_stdout(buf):
            exec(exp)
            res = buf.getvalue()
    except Exception as err:
        edit(text=ERROR.format(exp, err))
    else:
        if res is None:
            edit(text=SUCCESS.format(exp))
        else:
            edit(text=RESULT.format(exp, escape(res.rstrip())))

