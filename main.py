#!/usr/local/bin/python3 -u
from pyrogram import Client

plugins = dict(root='plugins')
app = Client('userbot', plugins=plugins)
app.run()
