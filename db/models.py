# from datetime import datetime
import sqlite3

from utils import configActions as config

# class Base(DeclarativeBase):
#     pass


#TODO: Добавить логирование через декоратор (Я ебал менять каждую функцию)

'''Храни блять меня господь. Я не хочу запускать и тестировать это дерьмо

PS - Tigrex'''


class SqliteSession:
    def __init__(self, dbLocation = config.takeCfg("dbLocation") ):
        execute_script = '''
            CREATE TABLE IF NOT EXISTS "User" (
                "id" INTEGER NOT NULL UNIQUE,
                "telegram_id" TEXT NOT NULL, 
                PRIMARY KEY("id")
            );

            CREATE INDEX IF NOT EXISTS "User_index_1"
            ON "User" ("telegram_id");
            CREATE TABLE IF NOT EXISTS "birthday_remind" (
                "id" INTEGER NOT NULL UNIQUE,
                "name" TEXT NOT NULL,
                "birth_date" DATE NOT NULL,
                "message" TEXT,
                "remind_date" DATE NOT NULL,
                "telegram_id" TEXT NOT NULL UNIQUE,
                PRIMARY KEY("id"),
                FOREIGN KEY ("telegram_id") REFERENCES "User"("telegram_id")
                ON UPDATE NO ACTION ON DELETE NO ACTION
            );

            CREATE INDEX IF NOT EXISTS "birthday_remind_index_0"
            ON "birthday_remind" ("telegram_id", "name");
            '''
        
        self.dbLocation = dbLocation 
        
        self.conn = sqlite3.connect(dbLocation, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Создание таблицы, если её нет
        self.cursor.execute(execute_script)
        self.conn.commit()

        # self._engine = create_engine("sqlite:///db.db")
        self._session = self.conn #sessionmaker(bind=self._engine)
        # self._session = #Session()
        pass
    
    def __call__(self):
        return self._session()

    def __getattr__(self, name):
        return getattr(self._session, name)
    
    # async def create_all(self):
    #     async with self._engine.begin() as conn:
    #         await conn.run_sync(Base.metadata.create_all)
    #     await self._engine.dispose()

dbSession = SqliteSession()


# from sqlalchemy import exc
# from sqlalchemy.schema import ForeignKey
# from sqlalchemy.types import Text, BigInteger 
# from sqlalchemy.sql import select, insert, update as sqlalchemy_update
# from sqlalchemy.sql.functions import func
# from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy.orm.strategy_options import load_only


class ModelAdmin:
    @classmethod
    def _create(cls, **kwargs) -> int:
        """
        Создает новую запись в таблице.
        :param kwargs: Поля и значения для записи
        :return: Идентификатор PK
        """
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?'] * len(kwargs))
        query = f'INSERT INTO {cls.__tablename__} ({columns}) VALUES ({placeholders})'
        
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, list(kwargs.values()))
            session.commit()
            return cursor.lastrowid

    @classmethod
    def add(cls, **kwargs) -> None:
        """
        Добавляет новую запись в таблицу.
        :param kwargs: Поля и значения для записи
        """
        cls._create(**kwargs)

    def update(self, **kwargs) -> None:
        """
        Обновляет текущую запись.
        :param kwargs: Поля и значения, которые нужно обновить
        """
        set_values = ', '.join([f'{key} = ?' for key in kwargs.keys()])
        query = f'UPDATE {self.__tablename__} SET {set_values} WHERE id = ?'
        
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, list(kwargs.values()) + [self.id])
            session.commit()

    def delete(self) -> None:
        """
        Удаляет текущую запись.
        """
        query = f'DELETE FROM {self.__tablename__} WHERE id = ?'
        
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, (self.id,))
            session.commit()

    @classmethod
    def _get(cls, **kwargs):
        """
        Возвращает одну запись, удовлетворяющую условиям.
        :param kwargs: Поля и значения для фильтрации
        :return: Объект или None
        """
        conditions = ' AND '.join([f'{key} = ?' for key in kwargs.keys()])
        query = f'SELECT * FROM {cls.__tablename__} WHERE {conditions}'
        
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, list(kwargs.values()))
            result = cursor.fetchone()
            if result:
                return cls(**dict(zip([col[0] for col in cursor.description], result)))
            return None

    @classmethod
    def filter(cls, **kwargs):
        """
        Возвращает все записи, удовлетворяющие условиям.
        :param kwargs: Поля и значения для фильтрации
        :return: Список объектов
        """
        conditions = ' AND '.join([f'{key} = ?' for key in kwargs.keys()])
        query = f'SELECT * FROM {cls.__tablename__} WHERE {conditions}'
        
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, list(kwargs.values()))
            results = cursor.fetchall()
            return [cls(**dict(zip([col[0] for col in cursor.description], row))) for row in results]

    @classmethod
    def all(cls):
        """
        Возвращает все записи из таблицы.
        :return: Список объектов
        """
        query = f'SELECT * FROM {cls.__tablename__}'
        
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return [cls(**dict(zip([col[0] for col in cursor.description], row))) for row in results]


class User(ModelAdmin):
    __tablename__ = "User"

    def __init__(self, id=None, telegram_id=None):
        self.id = id
        self.telegram_id = telegram_id

    @classmethod
    def _create(cls, telegram_id: str) -> int:
        """
        Создает нового пользователя.
        :param telegram_id: ID пользователя в Telegram (тип TEXT, как в базе данных)
        :return: ID созданного пользователя
        """
        query = '''
            INSERT INTO "User" (telegram_id)
            VALUES (?)
        '''
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, (telegram_id,))
            session.commit()
            return cursor.lastrowid

    @classmethod
    def _get(cls, **kwargs):
        """
        Получает пользователя по указанным параметрам.
        :param kwargs: Параметры для поиска (например, telegram_id="12345")
        :return: Объект User или None
        """
        conditions = ' AND '.join([f'{key} = ?' for key in kwargs.keys()])
        query = f'SELECT * FROM "User" WHERE {conditions}'
        
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, list(kwargs.values()))
            result = cursor.fetchone()
            if result:
                return cls(**dict(zip([col[0] for col in cursor.description], result)))
            return None
        
    @classmethod
    def all(cls):
        """
        Возвращает всех пользователей из таблицы.
        :return: Список объектов User
        """
        query = 'SELECT * FROM "User"'
        
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return [cls(**dict(zip([col[0] for col in cursor.description], row))) for row in results]
  
    # Высокоуровневые методы для работы с таблицей birthday_remind
    @classmethod
    def get_birthday_reminders(cls, telegram_id):
        """
        Получает все напоминания о днях рождения для пользователя по telegram_id.
        :param telegram_id: ID пользователя в Telegram
        :return: Список напоминаний
        """
        query = '''
            SELECT * FROM "birthday_remind"
            WHERE telegram_id = ?
        '''
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, (telegram_id,))
            results = cursor.fetchall()
            return results

    @classmethod
    def delete_birthday_reminder(cls, reminder_id):
        """
        Удаляет конкретное напоминание по его ID.
        :param reminder_id: ID напоминания
        """
        query = '''
            DELETE FROM "birthday_remind"
            WHERE id = ?
        '''
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, (reminder_id,))
            session.commit()

    @classmethod
    def add_birthday_reminder(cls, telegram_id, name, birth_date, message, remind_date):
        """
        Добавляет новое напоминание о дне рождения для пользователя.
        :param telegram_id: ID пользователя в Telegram
        :param name: Имя человека
        :param birth_date: Дата рождения (в формате DATE)
        :param message: Сообщение для напоминания
        :param remind_date: Дата напоминания (в формате DATE)
        """
        query = '''
            INSERT INTO "birthday_remind" (name, birth_date, message, remind_date, telegram_id)
            VALUES (?, ?, ?, ?, ?)
        '''
        with dbSession() as session:
            cursor = session.cursor()
            cursor.execute(query, (name, birth_date, message, remind_date, telegram_id))
            session.commit()
        

# class User(Base, ModelAdmin):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     tg_id: Mapped[int] = mapped_column(BigInteger())
#     fullname: Mapped[str] = mapped_column(Text())
#     username: Mapped[str] = mapped_column(Text())
#     inviter_id: Mapped[int] = mapped_column(BigInteger())
#     reg_datetime: Mapped[datetime] = mapped_column(
#         server_default=func.now(), nullable=True
#     )

#     @classmethod
#     def get_or_create(cls, tg_id: int, fullname: str = None,
#                       username: str = None, inviter_id: int = None) -> "User":
#         user: User = User.get(tg_id=tg_id)
#         if user is None:
#             user: User = User.get(id=User.create(tg_id=tg_id, fullname=fullname,
#                                                  username=username, inviter_id=inviter_id))
#         return user


# class Payments(Base, ModelAdmin): # Интересно, нужно разобрать
#     __tablename__ = "payments"

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     yoo_id: Mapped[str] = mapped_column(Text())
#     link: Mapped[str] = mapped_column(Text())
#     status: Mapped[str] = mapped_column(Text())
#     reg_datetime: Mapped[datetime] = mapped_column(
#         server_default=func.now(), nullable=True
#     )


# engine = create_engine("sqlite:///db.db")
# Base.metadata.create_all(engine)