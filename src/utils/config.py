import os
from dotenv import load_dotenv

load_dotenv()


def get_channel_id(value: str) -> int | str:
    """Преобразует строку в ID канала (int или username)."""
    try:
        return int(value)
    except ValueError:
        return value


BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в .env файле")

SOURCE_CHANNEL_ID = os.getenv("SOURCE_CHANNEL_ID")
if not SOURCE_CHANNEL_ID:
    raise ValueError("SOURCE_CHANNEL_ID не установлен в .env файле")
SOURCE_CHANNEL_ID = get_channel_id(SOURCE_CHANNEL_ID)

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID")
if not TARGET_CHANNEL_ID:
    raise ValueError("TARGET_CHANNEL_ID не установлен в .env файле")
TARGET_CHANNEL_ID = get_channel_id(TARGET_CHANNEL_ID)
