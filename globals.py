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

if not TOKEN:
    raise ValueError("Bot token is missing")

if not API_ID:
    raise ValueError("API ID is missing")

if not API_HASH:
    raise ValueError("API hash is missing")