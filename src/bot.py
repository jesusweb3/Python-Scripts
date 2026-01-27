from aiogram import Router
from aiogram.types import Message

from src.utils import get_logger, SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID

logger = get_logger(__name__)

router = Router()


def is_from_source_channel(message: Message) -> bool:
    """Проверяет, что сообщение из нужного канала-источника."""
    chat_id = message.chat.id
    username = message.chat.username
    
    if isinstance(SOURCE_CHANNEL_ID, int):
        return chat_id == SOURCE_CHANNEL_ID
    else:
        source_username = SOURCE_CHANNEL_ID.lstrip("@")
        return username == source_username


@router.channel_post()
async def forward_channel_post(message: Message) -> None:
    """
    Обрабатывает все посты из канала-источника и копирует их в целевой канал.
    Поддерживает все типы сообщений: текст, фото, видео, аудио, документы,
    голосовые сообщения, стикеры, анимации и т.д.
    """
    if not is_from_source_channel(message):
        return
    
    try:
        await message.copy_to(chat_id=TARGET_CHANNEL_ID)
        
        logger.info(
            f"Сообщение #{message.message_id} скопировано из канала "
            f"{message.chat.title or message.chat.id} в {TARGET_CHANNEL_ID}"
        )
        
    except Exception as e:
        logger.error(
            f"Ошибка при копировании сообщения #{message.message_id}: {e}"
        )


@router.edited_channel_post()
async def handle_edited_post(message: Message) -> None:
    """
    Обрабатывает отредактированные посты.
    Примечание: Telegram API не позволяет редактировать уже отправленные сообщения
    в другом канале, поэтому просто логируем это событие.
    """
    if not is_from_source_channel(message):
        return
    
    logger.info(
        f"Сообщение #{message.message_id} было отредактировано в канале "
        f"{message.chat.title or message.chat.id}. "
        f"Автоматическое обновление в целевом канале не поддерживается."
    )
