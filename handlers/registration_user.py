from handlers.other_handlers import *
from bot import bot


# Здесь начинается путь регистрации
# Создание состояний пользователя
class UserState(StatesGroup):
    username = State()
    user_id = State()


@router.message(Command('registration'))
async def start_command(message: Message, state: FSMContext):
    ban = get_ban()
    if message.from_user.id is ban:
        await message.answer('Ты заблокирован в этом чате.')
    users = get_users()
    if message.from_user.id is users:
        await message.answer('Ты уже .')
    else:
        await message.answer('Через это надо пройти, но только один раз.\n'
                             'Для отмены вызови команду /back', reply_markup=keyboard_reg)
        await state.set_state(UserState.user_id)


# Галя, у нас отмена
@router.message(Command('back'), ~StateFilter(default_state))
async def back(message: Message, state: FSMContext):
    await message.answer(
        text='Введённые данные сброшены.\n'
             'Чтобы снова перейти к заполнению анкеты - \n'
             'отправь команду /registration'
    )
    await state.clear()


# Coхранение user_id
@router.callback_query(F.data == 'reg', StateFilter(UserState.user_id))
async def id_save(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.from_user.id)
    state_data = await state.get_data()
    await state.set_state(UserState.username)
    await callback.message.answer('Введи своё имя:')


# Coхранение username, сохранение в БД
@router.message(StateFilter(UserState.username))
async def username_save(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    state_data = await state.get_data()
    us_name, us_id = state_data['username'], state_data['user_id']
    users = get_users()
    for user in range(len(users)):
        if us_id == users[user][0]:
            await message.answer(f'Пользователь с id {us_id} уже есть в базе.')
            continue
        else:
            create_user(username=us_name, user_id=us_id, block=True)
            await message.answer('Спасибо, данные сохранены, ожидай допуска.')
    await bot.send_message(
        chat_id=API_ADMIN,
        text=
        f'Поступил запрос на регистрацию:\n'
        f'ID пользователя:{message.from_user.id},\n'
        f'Имя пользователя: {message.text}',
        reply_markup=keyboard_inline_admin
    )
    await state.clear()
