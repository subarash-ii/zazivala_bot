from os import getenv
from dotenv import load_dotenv
import emoji

load_dotenv()


PREFIXES = ["call", ".call", "калл", ".калл"]
TOKEN = getenv("TOKEN")
API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
EMOJIS = [
    e for e in emoji.EMOJI_DATA.keys()
    if len(e) == 1
]
SPECIAL_USER_ID = 6803905517
SPECIAL_USER_EMOJIS = ["🦜", "🪽", "💜", "💖", "🎸", "🌀"]
MESSAGE_GROUP_SIZE = 8

if not TOKEN:
    raise ValueError("Bot token is missing")

if not API_ID:
    raise ValueError("API ID is missing")

if not API_HASH:
    raise ValueError("API hash is missing")