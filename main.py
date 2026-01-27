import asyncio
import signal
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot import router
from src.utils import get_logger, BOT_TOKEN, SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID

logger = get_logger(__name__)


async def main() -> None:
    """Точка входа для запуска бота."""
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    dp.include_router(router)
    
    # Graceful shutdown для Linux (Docker)
    loop = asyncio.get_running_loop()
    shutdown_event = asyncio.Event()
    
    def handle_signal(sig: signal.Signals) -> None:
        logger.info(f"Получен сигнал {sig.name}, завершаем работу...")
        shutdown_event.set()
    
    # Регистрируем обработчики сигналов (только для Unix/Linux)
    if sys.platform != "win32":
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, handle_signal, sig)
    
    logger.info("Бот запущен!")
    logger.info(f"Канал-источник: {SOURCE_CHANNEL_ID}")
    logger.info(f"Целевой канал: {TARGET_CHANNEL_ID}")
    
    # Запускаем polling в отдельной задаче
    polling_task = asyncio.create_task(dp.start_polling(bot))
    
    # Ждём сигнала завершения или окончания polling
    done, pending = await asyncio.wait(
        [polling_task, asyncio.create_task(shutdown_event.wait())],
        return_when=asyncio.FIRST_COMPLETED
    )
    
    # Останавливаем polling если ещё работает
    if not polling_task.done():
        await dp.stop_polling()
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            pass
    
    # Закрываем сессию бота
    await bot.session.close()
    logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
