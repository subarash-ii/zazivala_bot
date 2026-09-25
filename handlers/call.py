import asyncio
import time

from aiogram import Router, F
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message

from config import PREFIXES, MESSAGE_GROUP_SIZE, CALL_COOLDOWN
from member_fetcher import get_members
from utils import get_emoji, get_full_name, safe_answer

router = Router()
last_call_time = 0


@router.message(F.text.startswith(tuple(PREFIXES)))
async def call(message: Message):
    member = await message.chat.get_member(message.from_user.id)

    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await message.reply("❌ Эта команда доступна только администраторам.")
        return

    if member.status not in [ChatMemberStatus.CREATOR]:
        global last_call_time

        current_time = time.monotonic()

        if current_time - last_call_time < CALL_COOLDOWN:
            remaining = int(CALL_COOLDOWN - (current_time - last_call_time))
            await message.reply(f"⏳ Подождите ещё {remaining} сек., прежде чем использовать призыв.")

            return

        last_call_time = current_time

    users = [
        user
        for user in await get_members(message.chat.id)
        if user.username and not user.is_bot
    ]

    if not users:
        await message.answer("Не найдено пользователей для призыва.")
        return

    for i in range(0, len(users), MESSAGE_GROUP_SIZE):
        group = users[i:i + MESSAGE_GROUP_SIZE]

        text = "\n".join(
            f'{get_emoji(user)} '
            f'<a href="tg://user?id={user.id}">{get_full_name(user)}</a>'
            for user in group
        )

        if i == 0:
            text = (
                    f"<b>{message.from_user.full_name}</b> запустил призыв.\n\n"
                    + text
            )

        if i + MESSAGE_GROUP_SIZE >= len(users):
            text += "\n\nПризыв окончен."

        await safe_answer(message, text)
        await asyncio.sleep(0.3)