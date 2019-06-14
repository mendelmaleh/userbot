from pyrogram import Client
from pyrogram import __version__ as pyro_version
from collections import OrderedDict
import platform
import distro

from .shared import cmd_filter


@Client.on_message(cmd_filter('info'))
def _(client, message):
    info = OrderedDict([
        ('pyrogram', f'{pyro_version}'),
        ('python', platform.python_version()),
        (distro.id(), distro.version())
    ])
    text = '__userbot:__'
    for i in info:
        text += f'\n**{i}** `{info[i]}`'
    client.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=message.message_id,
        parse_mode='markdown')
