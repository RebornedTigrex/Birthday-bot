import logging
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Text, Index
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv
import os

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

Base = declarative_base()

# Определение моделей
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String, unique=True, nullable=False)

    birthday_reminders = relationship("BirthdayRemind", back_populates="user")

    @classmethod
    def get_or_create(cls, session, telegram_id):
        logger.info(f"Проверка существования пользователя с telegram_id={telegram_id}")
        user = session.query(cls).filter_by(telegram_id=telegram_id).first()
        if not user:
            logger.info(f"Пользователь с telegram_id={telegram_id} не найден. Создание нового пользователя.")
            user = cls(telegram_id=telegram_id)
            session.add(user)
            session.commit()
        return user


class BirthdayRemind(Base):
    __tablename__ = "birthday_remind"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    message = Column(Text)
    remind_date = Column(Date, nullable=False)
    telegram_id = Column(String, ForeignKey("user.telegram_id"), nullable=False)

    user = relationship("User", back_populates="birthday_reminders")

    @classmethod
    def add_reminder(cls, session, telegram_id, name, birth_date, message, remind_date):
        logger.info(f"Добавление напоминания для telegram_id={telegram_id}, имя={name}")
        reminder = cls(
            telegram_id=telegram_id,
            name=name,
            birth_date=birth_date,
            message=message,
            remind_date=remind_date,
        )
        session.add(reminder)
        session.commit()
        logger.info(f"Напоминание для {name} успешно добавлено.")
        return reminder


# Создание индексов
Index("user_index_1", User.telegram_id)
Index("birthday_remind_index_0", BirthdayRemind.telegram_id, BirthdayRemind.name)

# Загрузка переменных из .env
load_dotenv()

# Настройка подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL", "default_path_to_db.db")
engine = create_engine(f"sqlite:///{DATABASE_URL}", echo=True)
session_local = sessionmaker(bind=engine)

# Инициализация базы данных
def init_db():
    logger.info("Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    logger.info("База данных успешно инициализирована.")

# Пример использования
if __name__ == "__main__":
    init_db()
    try:
        session = session_local()

        # Пример добавления пользователя
        user = User.get_or_create(session, telegram_id="123456")

        # Пример добавления напоминания
        BirthdayRemind.add_reminder(
            session,
            telegram_id="123456",
            name="John Doe",
            birth_date="1990-01-01",
            message="Happy Birthday!",
            remind_date="2025-04-07",
        )
    except Exception as e:
        logger.error(f"Ошибка при работе с базой данных: {e}")
    finally:
        session.close()
        logger.info("Сессия базы данных закрыта.")