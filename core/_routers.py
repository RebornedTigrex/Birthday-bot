from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core import UserData
from bot import dp, db, User

from db import User, Birthday

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(UserData.name)
    await message.answer("Пожалуйста, введите имя человека, которого вы хотите поздравить:")

#Хуйня
@dp.message(UserData.name)
async def process_birthday(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(UserData.date)
    await message.answer("Теперь введите дату его рождения в форме YYYY.MM.DD:")

#День рождения
@dp.message(UserData.date)
async def process_birthday(message: types.Message, state: FSMContext):
    # user_id = message.from_user.id
    birthday = message.text

    # TODO:Проверка формата даты (Можно добавить более сложную валидацию)
    if len(birthday) == 10 and birthday[4] == '.' and birthday[7] == '.':
        name = await state.get_data().get("name")
        await message.answer(f"Спасибо! Дата рождения {name} сохранена: {birthday}. Дополнительное сообщение: \n (Это поле может быть пустым)")
        await state.update_data(birthday = birthday)
        await state.set_state(UserData.message_remind)
    else:
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате YYYY.MM.DD.")

@dp.message(UserData.message_remind)
async def process_birthday(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("name")
    birthday = user_data.get("birthday")
    remind_date = user_data.get("remind")
    
    await message.answer(f"(Если всё правильно - вы можете написать 'Да'. Если хотите переделать напоминание, напишите к чему нужно вернуться: Имя, День рождения, Сообщение, Дата напоминания)\nВаше напоминание будет выглядеть так:\n\nСкоро день рождение у {name},\n{message.text}\nДень рождение {name} : {birthday}\nВы просили напомнить вам в эту дату: {remind_date}")
    if True:
        await state.update_data(message = message.text)
    
    # await state.clear()

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
        
@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    state.clear()
    await message.answer("Действие отменено.")