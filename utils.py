import asyncio
import random

from aiogram.types import Message, LinkPreviewOptions
from aiogram.exceptions import TelegramRetryAfter

from globals import SPECIAL_USER_ID, SPECIAL_USER_EMOJIS, EMOJIS


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