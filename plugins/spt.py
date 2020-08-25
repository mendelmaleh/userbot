from pyrogram import Client
from pyrogram.types import Message
from .utils import config, mefilter

import tekore as tk


if 'spotify' in config and 'token' in config['spotify']:
    spotify = tk.Spotify(config['spotify']['token'])

    @Client.on_message(mefilter('spt'))
    async def spt(cl: Client, msg: Message):
        cur = spotify.playback_currently_playing()
        if not cur:
            await msg.edit('no songs playing')
            return

        artists = ', '.join(a.name for a in cur.item.artists)
        href = cur.item.external_urls['spotify'] if 'spotify' in cur.item.external_urls else ''

        await msg.edit(f'Now playing:\n<a href={href}>{cur.item.name} - {artists}</a>', disable_web_page_preview=True)
