import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timezone, datetime, date

from time_messages import send_event_cron, send_store_cron
from handlers.admin import *
from handlers.registration_user import *
from handlers.other_handlers import *

# Инициализация логгера
logger = logging.getLogger(__name__)

# Объявление конфигурации
config: Config = load_config()

# Инициализация бота и диспетчера
bot: Bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # WTF
dp: Dispatcher = Dispatcher()


# Функция конфигурирования и запуска бота
async def main() -> None:
    # Логгирование
    logging.basicConfig(
        level=logging.INFO, filemode='w', filename='runner_tests.log', encoding='UTF-8',
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    global bot

    # Сообщения по расписанию
    scheduler = AsyncIOScheduler(timezone='Asia/Novokuznetsk')
    scheduler.add_job(send_event_cron, trigger='cron', hour=7, minute=30, start_date=datetime.now(),
                      kwargs={'bot': bot})
    scheduler.add_job(send_store_cron, trigger='cron', hour=17, minute=0, start_date=datetime.now(),
                      kwargs={'bot': bot})
    scheduler.start()

    # Регистрация роутеров
    dp.include_router(router)

    # Пропускать накопившиеся апдейты и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
