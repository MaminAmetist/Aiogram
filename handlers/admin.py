from handlers.registration_user import *
from bot import bot


@router.message(Command('admin'), F.from_user.id == API_ADMIN)
async def start_admin(message: Message):
    await message.answer('Добро пожаловать в Админ-Панель! Выбери действие на клавиатуре',
                         reply_markup=keyboard_inline_admin)


# Машина состояний
class AdminState(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()


# Запрос текста рассылки
@router.callback_query(F.data == 'admin_1')
async def spam(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Напиши текст рассылки:')
    await state.set_state(AdminState.spam)


# Рассылка
@router.message(StateFilter(AdminState.spam))
async def start_spam(message: Message, state: FSMContext):
    spam_base = get_unban()
    for user in range(len(spam_base)):
        await bot.send_message(spam_base[user][0], message.text)
        await message.answer('Рассылка завершена.')
        await state.clear()


# Статистика
@router.callback_query(F.data == 'admin_2')
async def stat_info(callback: CallbackQuery):
    user_list = get_users()
    ban_list = get_ban()
    await callback.message.answer(
        f'В нашей группе {len(user_list)} пользователя, {len(ban_list)} из них заблокированы.')


# Блокировка пользователя
@router.callback_query(F.data == 'admin_3')
async def ban_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введи id пользователя, которого нужно заблокировать:')
    await state.set_state(AdminState.blacklist)


@router.message(StateFilter(AdminState.blacklist))
async def start_ban(message: Message, state: FSMContext):
    await state.update_data(blacklist=message.text)
    state_data = await state.get_data()
    us_id = state_data['blacklist']
    if message.text == 'Назад':
        await message.answer('Отмена! Возвращаю назад.', reply_markup=keyboard_inline_admin)
        await state.clear()
    else:
        if message.text.isdigit():
            result = get_user_id(us_id)
            if len(result) == 0:
                await message.answer('Такой пользователь не найден в базе данных.',
                                     reply_markup=keyboard_inline_admin)
            else:
                result = get_ban_id(us_id)
                if len(result) == 1:
                    await message.answer('Данный пользователь уже получил бан.',
                                         reply_markup=keyboard_inline_admin)
                else:
                    add_ban(us_id)
                    await message.answer('Пользователь успешно добавлен в ЧС.',
                                         reply_markup=keyboard_inline_admin)
                    await bot.send_message(chat_id=us_id, text='Ты был заблокирован.')
        else:
            await message.answer('Ты вводишь буквы...\nВведи ID.')
    await state.clear()


# РАЗБлокировка пользователя
@router.callback_query(F.data == 'admin_4')
async def unban_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введи id пользователя, которого нужно разблокировать:')
    await state.set_state(AdminState.whitelist)


@router.message(StateFilter(AdminState.whitelist))
async def start_unban(message: Message, state: FSMContext):
    await state.update_data(whitelist=message.text)
    state_data = await state.get_data()
    us_id = state_data['whitelist']
    if message.text == 'Назад':
        await message.answer('Отмена! Возвращаю назад.', reply_markup=keyboard_inline_admin)
    else:
        if message.text.isdigit():
            result = get_user_id(us_id)
            if len(result) == 0:
                await message.answer('Такой пользователь не найден в базе данных.',
                                     reply_markup=keyboard_inline_admin)
            else:
                result = get_ban_id(us_id)
                if len(result) == 1:
                    add_unban(us_id)
                    await message.answer('Пользователь успешно разблокирован.',
                                         reply_markup=keyboard_inline_admin)
                    await bot.send_message(chat_id=us_id, text='Теперь ты можешь пользоваться благами этого бота.')
                else:
                    await message.answer('Данный пользователь не получал бан.',
                                         reply_markup=keyboard_inline_admin)
        else:
            await message.answer('Ты воробушек...\nВведи ID.')
    await state.clear()
