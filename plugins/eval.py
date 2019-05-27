from pyrogram import Client, Filters
from functools import partial
from .shared import cmd_filter

RUNNING = "**Eval:**\n```{}```\n**Running...**"
ERROR = "**Eval:**\n```{}```\n**Error:**\n```{}```"
SUCCESS = "**Eval:**\n```{}```\n**Success**"
RESULT = "**Eval:**\n```{}```\n**Result:**\n```{}```"


@Client.on_message(Filters.me & cmd_filter('eval'))
def _(client, message):
    exp = ' '.join(message.command[1:])

    if exp:
        edit = partial(
                client.edit_message_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode='markdown'
        )

        edit(text=RUNNING.format(exp))

        try:
            res = eval(exp)
        except Exception as err:
            edit(text=ERROR.format(exp, err))
        else:
            if res is None:
                edit(text=SUCCESS.format(exp))
            else:
                edit(text=RESULT.format(exp, res))
