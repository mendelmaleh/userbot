#!/usr/local/bin/python3 -u

from pyrogram import Client, Filters

app = Client('userbot')
prefixes = '.:!'

@app.on_message(Filters.command('id', prefixes))
def get_id(client, message):
    text = f'<code>{message.chat.id}</code>'
    client.edit_message_text(
        message.chat.id,
        message.message_id,
        text,
        parse_mode='html')

@app.on_message(Filters.command('chats', prefixes))
def get_chats(client, message):
    chats = {
        "private":0,
        "channel":0,
        "group":0,
        "supergroup":0,
        "bot":0
    }

    for dialog in client.iter_dialogs():
        chats[dialog.chat.type] += 1

    text = '<b>Chats</b>'
    for i in chats:
       text += f'\n{i}: {chats[i]}' 

    client.edit_message_text(
        message.chat.id,
        message.message_id,
        text,
        parse_mode='html')

"""
syntax: `purge [int]`
usage:
if replied to message:
  deletes [int] messages, starting from the replied to message,
  if [int] is not supplied then all messages since.
else:
  deletes last [int] messages,
  if [int] is not supplied then doesn't delete anything.
"""
@app.on_message((Filters.me | Filters.channel) & Filters.command('purge', prefixes))
def purge_msgs(client, message):

    # if cmd has an int argument
    if len(message.command) > 1 and message.command[1].isdigit():
        n = int(message.command[1])
        if message.reply_to_message:
            message.delete()
            msgs = client.get_history(
                message.chat.id,
                limit=n,
                offset_id=message.reply_to_message.message_id,
                reverse=True) # this reverse gets messages after offset_id, rather than before it
            msgs = reversed(msgs.messages) # this reverses the order of the messages to delete

        else: # if cmd has int, but is not a reply
            msgs = client.get_history(message.chat.id, limit=n+1).messages

    else: # if cmd doesn't have an int
        if not message.reply_to_message:
            return

        # if it is a reply
        msgs = reversed(list(client.iter_history(
            message.chat.id,
            offset_id=message.reply_to_message.message_id,
            reverse=True)))

    # finally
    for msg in msgs:
        msg.delete()

app.run()
