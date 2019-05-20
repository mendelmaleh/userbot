from pyrogram import Client, Filters

pyro_lounge = -1001221450384
welcome_msg = '👋'


@Client.on_message(Filters.new_chat_members & Filters.chat(pyro_lounge))
def _(client, message):
    client.send_message(
            chat_id=message.chat.id,
            text=welcome_msg
    )
