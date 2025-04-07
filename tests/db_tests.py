import pytest
from datetime import date
from sqlalchemy.orm import sessionmaker
from db.models import User, BirthdayRemind, Base
from sqlalchemy import create_engine

# Создаем тестовую базу данных SQLite в памяти
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Фикстура для создания тестовой базы данных и сессии"""
    Base.metadata.create_all(bind=engine)  # Создаем таблицы
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)  # Удаляем таблицы после теста

def test_user_creation(db_session):
    """Тест создания пользователя"""
    test_telegram_id = "TEST_12345"

    # Создаем пользователя
    user = User.get_or_create(db_session, telegram_id=test_telegram_id)
    db_session.commit()

    # Проверяем, что пользователь создан
    assert user.telegram_id == test_telegram_id
    assert user.id is not None

    # Проверяем, что пользователь существует в базе
    fetched_user = db_session.query(User).filter_by(telegram_id=test_telegram_id).first()  # Используем класс User
    assert fetched_user is not None
    assert fetched_user.id == user.id

def test_birthday_reminder(db_session):
    """Тест добавления напоминания"""
    test_telegram_id = "TEST_12345"
    test_data = {
        "name": "Тестовый Пользователь",
        "birth_date": date(1990, 1, 1),
        "remind_date": date.today(),
        "message": "Тестовое напоминание"
    }

    # Создаем пользователя
    user = User.get_or_create(db_session, telegram_id=test_telegram_id)

    # Добавляем напоминание
    reminder = BirthdayRemind.add_reminder(
        session=db_session,
        telegram_id=test_telegram_id,
        name=test_data["name"],
        birth_date=test_data["birth_date"],
        remind_date=test_data["remind_date"],
        message=test_data["message"]
    )
    db_session.commit()

    # Проверяем, что напоминание создано
    assert reminder.name == test_data["name"]
    assert reminder.birth_date == test_data["birth_date"]
    assert reminder.remind_date == test_data["remind_date"]
    assert reminder.message == test_data["message"]

    # Проверяем, что напоминание существует в базе
    fetched_reminder = db_session.query(BirthdayRemind).filter_by(
        telegram_id=test_telegram_id, name=test_data["name"]
    ).first()
    assert fetched_reminder is not None
    assert fetched_reminder.id == reminder.id

def test_cleanup(db_session):
    """Тест очистки данных"""
    test_telegram_id = "TEST_12345"

    # Создаем пользователя
    user = User.get_or_create(db_session, telegram_id=test_telegram_id)

    # Добавляем напоминание
    BirthdayRemind.add_reminder(
        session=db_session,
        telegram_id=test_telegram_id,
        name="Тестовый Пользователь",
        birth_date=date(1990, 1, 1),
        remind_date=date.today(),
        message="Тестовое напоминание"
    )
    db_session.commit()

    # Удаляем данные
    db_session.query(BirthdayRemind).filter_by(telegram_id=test_telegram_id).delete()
    db_session.query(User).filter_by(telegram_id=test_telegram_id).delete()  # Используем класс User
    db_session.commit()

    # Проверяем, что данные удалены
    assert db_session.query(User).filter_by(telegram_id=test_telegram_id).first() is None
    assert db_session.query(BirthdayRemind).filter_by(telegram_id=test_telegram_id).first() is None