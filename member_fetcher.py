from pyrogram import Client

from globals import API_ID, API_HASH, TOKEN

pyrogram_app = Client(
    "member_fetcher",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)


async def get_members(chat_id: int):
    members = []

    async for member in pyrogram_app.get_chat_members(chat_id):
        members.append(member.user)

    return members