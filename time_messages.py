from aiogram import Bot
from datetime import datetime

from crud_functions_calendar import get_event_today
from crud_functions_store import get_stores
from crud_functions_user import get_users, get_username
from handlers.other_handlers import API_ADMIN


# Напоминание о запланированных мероприятий по расписанию
async def send_event_cron(bot: Bot):
    user_id = get_users()
    if len(user_id) >= 1:
        for user in range(len(user_id)):
            date = datetime.date(datetime.now())
            list_event = get_event_today(user_id=user_id[user][0], date=date)
            for event in range(len(list_event)):
                today_event = str(list_event[event][0])
                username = get_username(user_id[user][0])
                await bot.send_message(chat_id=user_id[user][0],
                                       text=f'{username[0][0]}, на сегодня запланировано: {today_event}')


# Мамкупи
async def send_store_cron(bot: Bot):
    stores = get_stores()
    if len(stores) >= 1:
        await bot.send_message(chat_id=API_ADMIN, text='Ваш народ голодает, необходимо пополнить запасы провизии.')
