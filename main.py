from pyrogram import Client

plugins = dict(root='plugins')
Client('userbot-async', plugins=plugins).run()
