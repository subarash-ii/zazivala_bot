import asyncio
import random

asyncio.set_event_loop(asyncio.new_event_loop())

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatMemberStatus
from aiogram.types import LinkPreviewOptions, Message
from aiogram.exceptions import TelegramRetryAfter
from pyrogram import Client
from pyrogram.types import User

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


def get_emoji(user):
    if user.id == SPECIAL_USER_ID:
        return random.choice(SPECIAL_USER_EMOJIS)

    return random.choice(EMOJIS)


def get_full_name(user):
    return f"{user.first_name} {user.last_name or ''}".strip()


async def safe_answer(message: Message, text: str):
    while True:
        try:
            return await message.answer(
                text,
                parse_mode="HTML",
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )
        except TelegramRetryAfter as e:
            print(f"Fool limit: waiting {e.retry_after} seconds...")
            await asyncio.sleep(e.retry_after + 0.5)


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

    users.extend([
        User(
            id=100000 + i,
            is_bot=False,
            first_name=f"user{i}",
            username=f"user{i}"
        )
        for i in range(1, 41)
    ])

    if not users:
        await message.answer("Не найдено пользователей для призыва.")
        return

    for i in range(0, len(users), MESSAGE_GROUP_SIZE):
        group = users[i:i + MESSAGE_GROUP_SIZE]

        text = "\n".join(
            f'{get_emoji(user)} '
            f'<a href="https://t.me/{user.username}">{get_full_name(user)}</a>'
            for user in group
        )

        if i == 0:
            text = (
                    f"<b>{message.from_user.full_name}</b> запустил призыв.\n\n"
                    + text
            )

        await safe_answer(message, text)
        await asyncio.sleep(0.3)

    await message.answer("Призыв окончен.")


async def main():
    print("Bot is running")

    await pyrogram_app.start()

    try:
        await dp.start_polling(bot)
    finally:
        await pyrogram_app.stop()


if __name__ == "__main__":
    asyncio.run(main())