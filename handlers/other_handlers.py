from datetime import datetime
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
    get_user_locale

from crud_functions_store import *
from crud_functions_user import *
from crud_functions_calendar import *
from keyboards.keyboards import *
from lexicon.lexicon import *

API_ADMIN = 130643448
CHAT_ID = 8065712864
router: Router = Router()
keyboard_start = create_keys(1, **MAIN_MENU)
keyboard_inline = create_inline_keys(1, **INLINE_BUTTON)


# start
@router.message(CommandStart())
async def start_bot(message: Message):
    await message.answer(f'Приветствую тебя, {message.from_user.full_name}.\n'
                         f' Для начала работы вызови команду /registration.\n'
                         f'Для администрирования вызови команду /admin.\n'
                         f' Если ты уже прошел регистрацию, воспользуйся меню.',
                         reply_markup=keyboard_start)


# Здесь выбираем, куда добавляем запись
@router.message(F.text == MAIN_MENU['menu_1'])  # убрать отправку сообщения MAIN_MENU['menu_1'] в чат
async def add_record(message: Message):
    user_ban = get_ban_id(message.from_user.id)
    if user_ban:
        await message.answer('Тебя заблокировали в этом чате.')
    else:
        user = get_user_id(message.from_user.id)
        if user:
            await message.answer('Здесь добавляем запись.', reply_markup=keyboard_inline)
        else:
            await message.answer('Для этого необходимо зарегистрироваться.')


#####Здесь добавляем запись в список###################################################################################
# Машина состояний
class StoreState(StatesGroup):
    title = State()
    address = State()


# Спросить наименование
@router.callback_query(F.data == 'add_1')
async def create_store(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Напиши, что нужно добавить в список:')
    await state.set_state(StoreState.title)


# Спросить ссылку
@router.message(StateFilter(StoreState.title))
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    state_data = await state.get_data()
    await message.answer('Отлично, хочешь добавить ссылку?', reply_markup=keyboard_inline_add_address)
    await state.set_state(StoreState.address)
    await state.update_data(address=message.text)


# Если хочет
@router.callback_query(F.data == 'add_3', StateFilter(StoreState.address))
async def add_address(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await callback.message.answer('Добавь ссылку:')


# Сохранить ссылку
@router.message(StateFilter(StoreState.address))
async def save_store_one(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    state_data = await state.get_data()
    title = state_data['title']
    address = state_data['address']
    create_new_store(title, address)
    await message.answer('Запись успешно добавлена.')
    await state.clear()


# Если не хочет
@router.callback_query(F.data == 'add_4', StateFilter(StoreState.address))
async def save_store_two(callback: CallbackQuery, state: FSMContext):
    await state.update_data(address=None)
    state_data = await state.get_data()
    title = state_data['title']
    address = state_data['address']
    create_new_store(title, address)
    await callback.message.answer('Запись успешно добавлена.')
    await state.clear()


#####Показываем список#################################################################################################
@router.message(F.text == MAIN_MENU['menu_2'])  # убрать отправку сообщения MAIN_MENU['menu_3'] в чат
async def show_store(message: Message):
    user_ban = get_ban_id(message.from_user.id)
    if user_ban:
        await message.answer('Тебя заблокировали в этом чате.')
    else:
        user = get_user_id(message.from_user.id)
        if user:
            await message.answer('Список покупок:')
            stores = get_stores()
            for store in range(len(stores)):
                if stores[store][1] == 'None':
                    show = str(stores[store][0])
                    await message.answer(show, reply_markup=keyboard_ready_store)
                else:
                    show = str(stores[store][0]) + ', ссылка:' + str(stores[store][1])
                    await message.answer(show, reply_markup=keyboard_ready_store)
        else:
            await message.answer('Для этого необходимо зарегистрироваться.')


# Удалить запись из списка
@router.callback_query(F.data == 'ready')
async def delete_store(callback: CallbackQuery):
    title = callback.message.text.split(', ссылка:')[0]
    del_store(title)
    await callback.message.edit_text('Запись удалена.')


#####Здесь добавляем запись в календарь################################################################################
# Машина состояний
class CalendarState(StatesGroup):
    user_id = State()
    date = State()
    title = State()
    repeat = State()


# Показываем календарь на текущую дату
@router.callback_query(F.data == 'add_2')
async def create_calendar(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.from_user.id)
    state_data = await state.get_data()
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2025, 1, 1), datetime(2025, 12, 31))
    await callback.message.answer(
        'Чтобы добавить мероприятие, выбери дату:',
        reply_markup=await calendar.start_calendar()
    )
    await state.set_state(CalendarState.date)


# Календарь 2025-2030, сохраняем дату мероприятия
@router.callback_query(SimpleCalendarCallback.filter(), StateFilter(CalendarState.date))
async def add_date(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2025, 1, 1), datetime(2030, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(f'Напиши, что нужно запланировать на {date.strftime("%Y-%m-%d")}:')
        await state.update_data(date=callback_query.answer(date.strftime("%Y-%m-%d")).text)
        state_data = await state.get_data()
        await state.set_state(CalendarState.title)


# Сохранение названия мероприятия
@router.message(StateFilter(CalendarState.title))
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text, )
    state_data = await state.get_data()
    await message.answer('Как часто мероприятие будет повторяться?', reply_markup=keyboard_inline_repeat_calendar)
    await state.set_state(CalendarState.repeat)


# Сохранение условий повтора и всего великолепия в БД
@router.callback_query(F.data.startswith('repeat_'), StateFilter(CalendarState.repeat))
async def add_repeat(callback: CallbackQuery, state: FSMContext):
    await state.update_data(repeat=callback.data)
    state_data = await state.get_data()
    user_id, date, title, repeat = state_data['user_id'], state_data['date'], state_data['title'], state_data['repeat']
    create_event(user_id, title, date, repeat)
    await callback.message.answer('Мероприятие внесено в календарь.')
    await state.clear()


#####Показываем все мероприятия########################################################################################
# Показываем
@router.message(F.text == MAIN_MENU['menu_3'])  # убрать отправку сообщения MAIN_MENU['menu_3'] в чат
async def show_calendar(message: Message):
    user_ban = get_ban_id(message.from_user.id)
    if user_ban:
        await message.answer('Тебя заблокировали в этом чате.')
    else:
        user = get_user_id(message.from_user.id)
        if user:
            list_event = get_event()
            await message.answer(f'Показываю все мероприятия:')
            for event in range(len(list_event)):
                await message.answer(f'{str(list_event[event][0]) + " на " + str(list_event[event][1])}',
                                     reply_markup=keyboard_ready_calendar)
        else:
            await message.answer('Для этого необходимо зарегистрироваться.')


# Удалить/апдейтнуть мероприятие
@router.callback_query(F.data == 'ready_calendar')
async def delete_store(callback: CallbackQuery):
    title = callback.message.text.split(" на ")[0]
    date = callback.message.text.split(" на ")[1]
    repeat = get_repeat(title, date)
    year, month, day = date.split('-')[0], date.split('-')[1], date.split('-')[2]
    for i in range(len(repeat)):
        if repeat[i][0] == 'repeat_no':
            del_event(title, date)
            await callback.message.edit_text('Запись удалена.')
        if repeat[i][0] == 'repeat_month':
            if int(month) < 12:
                new_month = int(month) + 1
            else:
                new_month = f'{1:02}'
            new_date = str(year) + '-' + f'{new_month:02}' + '-' + str(day)
            change_event(new_date, title)
            await callback.message.edit_text(f'Мероприятие перенесено на {new_date}')
        if repeat[i][0] == 'repeat_year':
            new_year = int(year) + 1
            new_date = str(new_year) + '-' + str(month) + '-' + str(day)
            change_event(new_date, title)
            await callback.message.edit_text(f'Мероприятие перенесено на {new_date}')
