from pyrogram import Client, Filters
from contextlib import redirect_stdout
from functools import partial
from io import StringIO

from .shared import cmd_filter

RUNNING = "**Exec:**\n```{}```\n**Running...**"
ERROR = "**Exec:**\n```{}```\n**Error:**\n```{}```"
SUCCESS = "**Exec:**\n```{}```\n**Success**"
RESULT = "**Exec:**\n```{}```\n**Result:**\n```{}```"


@Client.on_message(Filters.me & cmd_filter('exec'))
def _(client, message):
    exp = ' '.join(message.command[1:])
    edit = partial(
            client.edit_message_text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            parse_mode='markdown'
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
            edit(text=RESULT.format(exp, res.rstrip()))
