#!/usr/local/bin/python3 -u

from pyrogram import Client, Filters
from pyrogram.errors import BadRequest
import time

app = Client('userbot')
prefixes = '.:!'


@app.on_message(Filters.command('chats', prefixes))
def get_chats(client, message):
    start = time.time()
    chats = {
        'private': 0,
        'channel': 0,
        'group': 0,
        'supergroup': 0,
        'bot': 0
    }
    private_ids = []

    for dialog in client.iter_dialogs():
        if dialog.chat.type == 'private':
            private_ids.append(dialog.chat.id)
            continue

        chats[dialog.chat.type] += 1

    private_users = app.get_users(private_ids)
    for user in private_users:
        if user.is_bot:
            chats['bot'] += 1
        else:
            chats['private'] += 1

    text = '<b>Chats</b>'

    for i in chats:
        f = i
        if f == 'private':
            f += ' chat'
        f += 's'
        text += f'\n{f}: {chats[i]}'

    text += f'\n<b>total: {sum(chats[i] for i in chats)}</b> -> {int(time.time() - start)}s'

    client.edit_message_text(
        message.chat.id,
        message.message_id,
        text,
        parse_mode='html')


@app.on_message(Filters.command('channels', prefixes))
def get_channels(client, message):
    start = time.time()
    text = '<b>Channels</b>'
    me = client.get_me()
    for dialog in client.iter_dialogs():
        if dialog.chat.type == 'channel':
            try:
                admins = client.get_chat_members(dialog.chat.id, filter='administrators')
            except BadRequest:
                continue

            for i in admins.chat_members:
                if i.user.id == me.id:
                    time.sleep(0.2)
                    chat = client.get_chat(dialog.chat.id)
                    text += f'\n<a href="{chat.invite_link}">{chat.title}</a>'

    text += f'\n<i>{int(time.time() - start)}s</i>'

    client.edit_message_text(
        message.chat.id,
        message.message_id,
        text,
        parse_mode='html')


@app.on_message(Filters.command('members', prefixes))
def get_members(client, message):
    text = '<b>Memebers</b>'
    members = {
            'users': 0,
            'creator': 0,
            'administrator': 0,
            'member': 0,
            'restricted': 0,
            'left': 0,
            'kicked': 0,
            'deleted': 0
    }

    for member in client.iter_chat_members(message.chat.id):
        members[member.status] += 1
        members['users'] += 1
        if member.user.is_deleted:
            members['deleted'] += 1

    for i in members:
        text += f'\n{i}: {members[i]}'

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
                reverse=True)  # this reverse gets messages after offset_id, rather than before it
            msgs = reversed(msgs.messages)  # this reverses the order of the messages to delete

        else:  # if cmd has int, but is not a reply
            msgs = client.get_history(message.chat.id, limit=n+1).messages

    else:  # if cmd doesn't have an int
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
