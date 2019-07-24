from pyrogram import Filters
from functools import partial

prefix = '.:!'
separator = None

cmd_filter = partial(Filters.command, prefix=prefix, separator=separator)
