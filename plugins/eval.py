from pyrogram import Client, Filters
from functools import partial
from .shared import cmd_filter

RUNNING = "<b>Eval:</b>\n<code>{}</code>\n<b>Running...</b>"
ERROR = "<b>Eval:</b>\n<code>{}</code>\n<b>Error:</b>\n<code>{}</code>"
SUCCESS = "<b>Eval:</b>\n<code>{}</code>\n<b>Success</b>"
RESULT = "<b>Eval:</b>\n<code>{}</code>\n<b>Result:</b>\n<code>{}</code>"


@Client.on_message(Filters.me & cmd_filter('eval'))
def _(client, message):
    exp = ' '.join(message.command[1:])

    if exp:
        edit = partial(
                client.edit_message_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode='html'
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
