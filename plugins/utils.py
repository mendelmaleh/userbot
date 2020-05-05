from configparser import ConfigParser
from inspect import getfullargspec

from pyrogram import Filters, Message


def isnumber(text: str) -> bool:
    text = text[1:] if text[0] == '-' else text
    return text.isnumeric()


config = ConfigParser()
config.read("config.ini")

p = list(config['commands'].get('prefixes', '.'))
allowed = [int(c) if isnumber(c) else c for c in config['commands']['chats'].split()]


def mefilter(cmd: str) -> pyrogram.client.filters.filter.Filter:
    return Filters.command(cmd, prefixes=p) & Filters.me


def gefilter(cmd):
    return Filters.command(cmd, prefixes=p) & (Filters.me | Filters.chat(allowed) & ~Filters.edited)

def err(text):
    return f'<i>{text}</i>'

async def awall(*args):
    for a in args:
        await a


async def edrep(msg: Message, **kwargs):
    func = msg.edit if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})
