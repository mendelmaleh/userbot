from pyrogram import Filters

p = list('.:!')
chats_allowed = ['pyrogramlounge', -1001257291641]


def gefilter(cmd):
    return Filters.command(cmd, prefixes=p) & (Filters.me | Filters.chat(chats_allowed)) & ~Filters.edited


def err(text):
    return f'<i>{text}</i>'
