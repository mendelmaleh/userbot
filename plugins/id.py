'''
usage: id [-h] [-x] [-c | -m | -r | -f]

  -h, --help        help message
  -x, --hex         id as hex

  -c, --chat        chat id (default)
  -m, --me          user id
  -r, --replied     sender from rtm
  -f, --forwarded   'forwarded from' from rtm
'''

from pyrogram import Client, Filters, Message
from docopt import docopt, DocoptExit
from .shared import gefilter


@Client.on_message(gefilter('id'))
async def _(cl: Client, msg: Message):
    try:
        a = docopt(__doc__, argv=msg.command[1:], help=False)
    except DocoptExit as e:
        text = f'<pre>{e.usage}</pre>'
    else:
        if a['--help']:
            text = f'<pre>{__doc__.strip()}</pre>'
        else:
            if a['--me']:
                u = await cl.get_me()
                id = u.id
            elif a['--replied']:
                if msg.reply_to_message:
                    id = msg.reply_to_message.from_user.id
                else:
                    err = "msg.rtm is None"
            elif a['--forwarded']:
                if msg.reply_to_message.forward_from_chat:
                    id = msg.reply_to_message.forward_from_chat.id
                elif msg.reply_to_message.forward_from:
                    id = msg.reply_to_message.forward_from.id
                else:
                    err = "msg.rtm is not a forwarded msg"
            else:
                id = msg.chat.id

            try:
                if a['--hex']: id = hex(id)
                text = f'<code>{id}</code>'
            except NameError:
                text = f'<i>{err}</i>'

    await msg.edit_text(text, parse_mode='html')
