from pyrogram import Client
from .shared import cmd_filter


@Client.on_message(cmd_filter('id'))
def get_id(client, message):
    text = f'<code>{message.chat.id}</code>'
    client.edit_message_text(
        message.chat.id,
        message.message_id,
        text,
        parse_mode='html')
