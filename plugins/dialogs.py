from pyrogram import Client
from pyrogram.errors import BadRequest
from .shared import cmd_filter
import time


@Client.on_message(cmd_filter('chats'))
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

    private_users = client.get_users(private_ids)
    for user in private_users:
        if user.is_bot:
            chats['bot'] += 1
        else:
            chats['private'] += 1

    text = '<i>chats</i>'

    for i in chats:
        f = i
        if f == 'private':
            f += ' chat'
        f += 's'
        text += f'\n{f}: {chats[i]}'

    text += f'\n<b>total: {sum(chats[i] for i in chats)}</b> -> {int(time.time() - start)}s'

    client.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=message.message_id,
        parse_mode='html')


@Client.on_message(cmd_filter('channels'))
def get_channels(client, message):
    start = time.time()
    text = '<i>channels</i>'
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
        text=text,
        chat_id=message.chat.id,
        message_id=message.message_id,
        parse_mode='html')


@Client.on_message(cmd_filter('members'))
def get_members(client, message):
    text = '<i>members</i>'
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
        text=text,
        chat_id=message.chat.id,
        message_id=message.message_id,
        parse_mode='html')
