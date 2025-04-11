import logging
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Text, Index, inspect
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
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

# Определение абсолютного пути к корневой папке
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# Загрузка переменных из .env только если они не заданы
if not os.getenv("DATABASE_URL"):
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

# Настройка подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL", "birtdays.db")
dbUrl = os.path.join(ROOT_DIR, DATABASE_URL)
engine = create_engine(f"sqlite:///{dbUrl}", echo=True)
SessionLocal = sessionmaker(bind=engine)

# Инициализация базы данных
def init_db():
    logger.info("Инициализация базы данных...")
    try:
        inspector = inspect(engine)  # Создаем инспектор для проверки таблиц
        if not inspector.has_table("user") or not inspector.has_table("birthday_remind"):
            Base.metadata.create_all(bind=engine)
            logger.info("Таблицы успешно созданы.")
        else:
            logger.info("Таблицы уже существуют. Пропуск создания.")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
    logger.info("Инициализация базы данных завершена.")

# Пример использования
if __name__ == "__main__":
    init_db()
    try:
        session = SessionLocal()

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