import time

from pyrogram import Client
from pyrogram.types import Chat, Message

from .utils import code, edrep, mefilter


@Client.on_message(mefilter('members'))
async def _members(cl: Client, msg: Message):
    chat = msg.chat
    if len(msg.command) > 1:
        chat = await cl.get_chat(msg.command[1])

    await msg.edit('...')
    start = time.time()
    status = await members(cl, chat)
    delta = time.time() - start
    await edrep(msg, text='\n'.join([f"{len(status[k])} users {k}" for k in status] + [code(f'{int(delta * 1000)}ms')]))


async def members(cl: Client, chat: Chat):
    status = {k: [] for k in ['online', 'offline', 'recently', 'within_week', 'within_month', 'long_time_ago', None]}
    async for member in chat.iter_members(filter='all'):
        status[member.user.status].append(member)

    return status


@Client.on_message(mefilter('list'))
async def _list(cl: Client, msg: Message):
    filters = ['all', 'kicked', 'restricted', 'bots', 'recent', 'administrators']
    status = ['within_week', 'within_month', 'long_time_ago']
    mode = 'recent'
    chat = msg.chat

    if len(msg.command) > 1:
        mode = msg.command[1]
        if mode not in filters+status:
            await msg.edit(f'invalid mode "{mode}"')
            return
    if len(msg.command) > 2:
        chat = await cl.get_chat(msg.command[2])

    await msg.edit('...')
    start = time.time()

    chat_members = []
    async for member in chat.iter_members(filter=mode if mode in filters else 'recent'):
        if mode in filters or member.user.status == mode:
            chat_members.append(member)

    delta = time.time() - start
    await msg.edit(f'got {len(chat_members)} "{mode}" members in {code(f"{int(delta * 1000)}ms")}...')
    await msg.edit('\n'.join(
        [f'got {len(chat_members)} "{mode}" members in {code(f"{int(delta * 1000)}ms")}:']
        + [f'{code(member.user.id)}: {member.user.mention if not member.user.is_deleted else "DELETED"}' for member in chat_members]
    ))


@Client.on_message(mefilter('purge'))
async def _purge(cl: Client, msg: Message):
    modes = ['all', 'within_week', 'within_month', 'long_time_ago']
    chat = msg.chat

    if len(msg.command) > 1:
        mode = msg.command[1]
        if mode not in modes:
            await edrep(msg, f'invalid mode "{mode}"')
            return
    if len(msg.command) > 2:
        chat = await cl.get_chat(msg.command[2])

    await msg.edit('...')
    start = time.time()
    chat_members = []
    async for member in chat.iter_members():
        if member.status == 'member' and not member.user.is_bot and (mode == 'all' or member.user.status == mode):
            chat_members.append(member)

    delta = time.time() - start
    await msg.edit(f'got {len(chat_members)} members in {code(f"{int(delta * 1000)}ms...")}')

    start = time.time()
    resp = []
    for index, member in enumerate(chat_members):
        if index % 5 == 0:
            await msg.edit(f'purged {index}/{len(chat_members)}')

        resp.append(await chat.kick_member(member.user.id, int(time.time()) + 60))
        # print(await chat.unban_member(member.user.id))

    ddelta = time.time() - start
    await cl.delete_messages(chat.id, [msg.message_id for msg in resp if isinstance(msg, Message)])
    await msg.edit(f'purged {len(chat_members)} members in {code(f"{int(ddelta * 1000)}ms")} (total {code(f"{int((delta+ddelta) * 1000)}ms")})')
