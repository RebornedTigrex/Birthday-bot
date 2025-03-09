from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core import UserData
from core.bot_init import dp, db, User

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(UserData.waiting_for_birthday)
    await message.answer("Пожалуйста, введите дату рождения в формате ДД.ММ.ГГГГ:")

# Обработчик ввода даты рождения
@dp.message(UserData.waiting_for_birthday)
async def process_birthday(message: types.Message, state: FSMContext):
    # user_id = message.from_user.id #TODO: Допиши state имени
    birthday = message.text

    # TODO:Проверка формата даты (можно добавить более сложную валидацию)
    if len(birthday) == 10 and birthday[2] == '.' and birthday[5] == '.':
        # Сохраняем дату рождения в TinyDB
        db.upsert({'user_id': user_id, 'birthday': birthday}, User.user_id == user_id) #TODO: Перепиши это дерьмо
        await message.answer(f"Спасибо! Ваша дата рождения сохранена: {birthday}")
        await state.clear()
    else:
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")

# Обработчик команды /my_birthday
@dp.message(Command("my_birthday"))
async def cmd_my_birthday(message: types.Message):
    user_id = message.from_user.id
    # Ищем дату рождения пользователя в базе данных
    result = db.search(User.user_id == user_id)
    if result:
        await message.answer(f"Ваша дата рождения: {result[0]['birthday']}")
    else:
        await message.answer("Ваша дата рождения не найдена. Введите её с помощью команды /start.")