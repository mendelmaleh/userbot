from pyrogram import Filters
from functools import partial

prefixes = '.:!'
cmd_filter = partial(Filters.command, prefix=prefixes)
