# Userbot
My personal telegram userbot. Built with [Pyrogram](https://github.com/pyrogram/pyrogram).

## Commands
- **id**: get the ID for the chat, message, or yourself, in various formats.
- **inactive**: get the 5 least active members of the group.
- **ping**: test your userbot's latency (only indicative).
- **print**: print message info.
- **spt**: get current song playing on spotify.
- **wttr**: get the weather for the given location, in various formats.

## Functions
- **welcome**: welcome newcomers to chats.

## Setup:
Create and start `venv` for the dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `config.ini` file with your Telegram API `id` and `hash` in the following format:
```ini
[pyrogram]
api_id = 12345
api_hash = 0123456789abcdef0123456789abcdef

[plugins]
root = plugins
```
The `root` is the folder with the plugins, in this repo it is `plugins`, so there is no need to change this.  More info at Pyrogram's [official docs.](https://docs.pyrogram.org/topics/config-file)
