from utils.bot_instance import dp  # Импортируем dp из bot_instance
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram.types import ReplyKeyboardRemove, BotCommand

from core import UserData
from db.models import SessionLocal, BirthdayRemind



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в Birthday Bot! Вы можете использовать следующие команды:\n"
        "/add_birthday - Добавить новое напоминание о дне рождения\n"
        "/my_birthday - Просмотреть все напоминания\n"
        "/delete_birthday - Удалить напоминание о дне рождения\n"
        "/cancel - Отменить текущее действие"
    )


@dp.message(Command("add_birthday"))
async def cmd_add_birthday(message: types.Message, state: FSMContext):
    await state.set_state(UserData.name)
    await message.answer("Пожалуйста, введите имя человека, которого вы хотите поздравить:")


@dp.message(UserData.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserData.date)
    await message.answer("Теперь введите дату его рождения в формате YYYY-MM-DD:")


@dp.message(UserData.date)
async def process_birthday(message: types.Message, state: FSMContext):
    birthday = message.text

    # Проверка формата даты
    try:
        datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате YYYY-MM-DD.")
        return

    user_data = await state.get_data()
    name = user_data.get("name")
    await state.update_data(birthday=birthday)
    await state.set_state(UserData.message_remind)
    await message.answer(
        f"Спасибо! Дата рождения {name} сохранена: {birthday}. "
        "Теперь введите сообщение, которое вы хотите отправить в день напоминания:"
    )


@dp.message(UserData.message_remind)
async def process_message_remind(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("name")
    birthday = user_data.get("birthday")
    remind_message = message.text

    # Сохранение данных в базу
    session = SessionLocal()
    try:
        BirthdayRemind.add_reminder(
            session=session,
            telegram_id=message.from_user.id,
            name=name,
            birth_date=birthday,
            message=remind_message,
            remind_date=birthday,  # Здесь можно добавить логику для напоминания заранее
        )
        await message.answer(
            f"Напоминание сохранено! Вот что вы указали:\n\n"
            f"Имя: {name}\nДата рождения: {birthday}\nСообщение: {remind_message}"
        )
    except Exception as e:
        await message.answer("Произошла ошибка при сохранении напоминания.")
        print(e)
    finally:
        session.close()

    await state.clear()


@dp.message(Command("my_birthday"))
async def cmd_my_birthday(message: types.Message):
    session = SessionLocal()
    try:
        user_reminders = session.query(BirthdayRemind).filter_by(telegram_id=message.from_user.id).all()
        if user_reminders:
            response = "Ваши напоминания:\n\n"
            for reminder in user_reminders:
                response += (
                    f"Имя: {reminder.name}\n"
                    f"Дата рождения: {reminder.birth_date}\n"
                    f"Сообщение: {reminder.message}\n"
                    f"Дата напоминания: {reminder.remind_date}\n\n"
                )
            await message.answer(response)
        else:
            await message.answer("У вас пока нет сохранённых напоминаний.")
    except Exception as e:
        await message.answer("Произошла ошибка при получении данных.")
        print(e)
    finally:
        session.close()


@dp.message(Command("delete_birthday"))
async def cmd_delete_birthday(message: types.Message, state: FSMContext):
    session = SessionLocal()
    try:
        user_reminders = session.query(BirthdayRemind).filter_by(telegram_id=message.from_user.id).all()
        if user_reminders:
            response = "Выберите напоминание для удаления, отправив его ID:\n\n"
            for reminder in user_reminders:
                response += (
                    f"ID: {reminder.id}\n"
                    f"Имя: {reminder.name}\n"
                    f"Дата рождения: {reminder.birth_date}\n\n"
                )
            await state.set_state(UserData.delete_id)
            await message.answer(response)
        else:
            await message.answer("У вас пока нет сохранённых напоминаний.")
    except Exception as e:
        await message.answer("Произошла ошибка при получении данных.")
        print(e)
    finally:
        session.close()


@dp.message(UserData.delete_id)
async def process_delete_birthday_by_id(message: types.Message, state: FSMContext):
    session = SessionLocal()
    try:
        reminder_id = message.text
        reminder = session.query(BirthdayRemind).filter_by(
            telegram_id=message.from_user.id, id=reminder_id
        ).first()
        if reminder:
            session.delete(reminder)
            session.commit()
            await message.answer(f"Напоминание с ID {reminder_id} успешно удалено.")
        else:
            await message.answer(f"Напоминание с ID {reminder_id} не найдено.")
    except Exception as e:
        await message.answer("Произошла ошибка при удалении напоминания.")
        print(e)
    finally:
        session.close()
        await state.clear()


@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=ReplyKeyboardRemove())