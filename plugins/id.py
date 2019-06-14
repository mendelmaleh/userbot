from pyrogram import Client
from .shared import cmd_filter


@Client.on_message(cmd_filter('id'))
def get_id(client, message):
    text = f'<code>{message.chat.id}</code>'
    client.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=message.message_id,
        parse_mode='html')
