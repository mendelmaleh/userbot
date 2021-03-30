from configparser import ConfigParser
from html import escape
from inspect import getfullargspec

from pyrogram import filters
from pyrogram.types import Message


def isnumber(text: str) -> bool:
    return text.lstrip('-').isnumeric()


config = ConfigParser()
config.read("config.ini")

p = list(config['commands'].get('prefixes', '.'))
allowed = [int(c) if isnumber(c) else c for c in config['commands']['chats'].split()]


def mefilter(cmd: str) -> filters.Filter:
    return filters.command(cmd, prefixes=p) & filters.me


def gefilter(cmd: str) -> filters.Filter:
    return filters.command(cmd, prefixes=p) & (filters.me | filters.chat(allowed) & ~filters.edited)


def code(text: str) -> str:
    return '<pre>' + escape(str(text)) + '</pre>'


def err(text: str) -> str:
    return f'<i>{text}</i>'


async def awall(*args):
    for a in args:
        await a


async def edrep(msg: Message, **kwargs):
    func = msg.edit if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})
