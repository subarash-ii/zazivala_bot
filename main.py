import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LinkPreviewOptions
from aiogram.enums import ChatMemberStatus

from pyrogram import Client

import random

from globals import *

bot = Bot(token=TOKEN)
dp = Dispatcher()

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


@dp.message(F.text.startswith(tuple(PREFIXES)))
async def call(message: Message):
    member = await message.chat.get_member(message.from_user.id)

    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await message.reply("❌ Эта команда доступна только администраторам.")
        return

    users = [
        user
        for user in await get_members(message.chat.id)
        if user.username and not user.is_bot
    ]

    if not users:
        await message.answer("Не найдено пользователей для призыва.")
        return

    await message.answer(
        f"<b>{message.from_user.full_name}</b> запустил призыв.\n\n"
        f'{random.choice(EMOJIS)} '
        f'<a href="https://t.me/{users[0].username}">{users[0].first_name}</a>',
        parse_mode="HTML",
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

    for user in users[1:-1]:
        await message.answer(
            f'{random.choice(EMOJIS)} '
            f'<a href="https://t.me/{user.username}">{user.first_name}</a>',
            parse_mode="HTML",
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )

    if len(users) > 1:
        await message.answer(
            f'{random.choice(EMOJIS)} '
            f'<a href="https://t.me/{users[-1].username}">{users[-1].first_name}</a>\n\n'
            f"Призыв окончен.",
            parse_mode="HTML",
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )

@dp.message(F.text.startswith("!"))
async def random_emoji(message: Message):
    await message.answer(random.choice(EMOJIS))


async def main():
    print("Bot is running")

    await pyrogram_app.start()

    try:
        await dp.start_polling(bot)
    finally:
        await pyrogram_app.stop()


if __name__ == "__main__":
    asyncio.run(main())