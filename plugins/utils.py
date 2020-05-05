from configparser import ConfigParser

from pyrogram import Filters


def isnumber(text: str) -> bool:
    text = text[1:] if text[0] == '-' else text
    return text.isnumeric()


config = ConfigParser()
config.read("config.ini")

p = list(config['commands'].get('prefixes', '.'))
allowed = [int(c) if isnumber(c) else c for c in config['commands']['chats'].split()]


def gefilter(cmd):
    return Filters.command(cmd, prefixes=p) & (Filters.me | Filters.chat(allowed) & ~Filters.edited)

def err(text):
    return f'<i>{text}</i>'

async def awall(*args):
    for a in args:
        await a
