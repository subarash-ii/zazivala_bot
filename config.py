import os
import unicodedata

import emoji
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

PREFIXES = ["call", ".call", "калл", ".калл"]
MESSAGE_GROUP_SIZE = 12

CALL_COOLDOWN = 30

SPECIAL_USER_ID = 6803905517
SPECIAL_USER_EMOJIS = [
    "🦜",
    "🪽",
    "💜",
    "💖",
    "🎸",
    "🌀",
]

EMOJIS = [
    e
    for e in emoji.EMOJI_DATA
    if len(e) == 1
    and unicodedata.category(e) not in ("Mn", "Me")
]


if not TOKEN:
    raise ValueError("Bot token is missing")

if not API_ID:
    raise ValueError("API ID is missing")

if not API_HASH:
    raise ValueError("API hash is missing")