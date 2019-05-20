from pyrogram import Client, Filters

prefixes = '.:!'


@Client.on_message(Filters.command('id', prefixes))
def get_id(client, message):
    text = f'<code>{message.chat.id}</code>'
    client.edit_message_text(
        message.chat.id,
        message.message_id,
        text,
        parse_mode='html')
