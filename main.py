from pyrogram import Client, Filters

app = Client('userbot')

@app.on_message(Filters.command('id', '.'))
def get_id(client, message):
    text = f'<code>{message.chat.id}</code>'
    client.edit_message_text(
        message.chat.id,
        message.message_id,
        text,
        parse_mode='html')

@app.on_message((Filters.me | Filters.channel) & Filters.command('purge', '.'))
def purge_msgs(client, message):
    for msg in client.iter_history(
            message.chat.id,
            offset_id=message.reply_to_message.message_id,
            reverse=True):
        msg.delete()

app.run()
