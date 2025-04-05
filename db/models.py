# from datetime import datetime
import sqlite3

from utils import config

class SqliteSession:
    def __init__(self, dbLocation = config["dbLocation"]):
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

        self._session = self.conn

    
    def __call__(self):
        return self._session()

    def __getattr__(self, name):
        return getattr(self._session, name)

dbSession = SqliteSession()


class BirthdayRemind():
    __tablename__ = "birthday_remind"
    
    def __init__(self, id: int, name: str, birth_date: str, message: str, remind_date: str, telegram_id: str):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.message = message
        self.remind_date = remind_date
        self.telegram_id = telegram_id

    @classmethod
    def getCreate(cls, telegram_id: str, name: str, birth_date: str, remind_date: str, message: str = "") -> "BirthdayRemind":
        """Создает или обновляет напоминание"""
        cursor = dbSession.cursor
        
        try:
            cursor.execute(
                f"""INSERT INTO {cls.__tablename__} 
                (name, birth_date, message, remind_date, telegram_id)
                VALUES (?, ?, ?, ?, ?)
                RETURNING id""",
                (name, birth_date, message, remind_date, telegram_id)
            )
            result = cursor.fetchone()
            dbSession.conn.commit()
            return cls(id=result[0], name=name, birth_date=birth_date, 
                      message=message, remind_date=remind_date, telegram_id=telegram_id)
            
        except sqlite3.IntegrityError:
            dbSession.conn.rollback()
            cursor.execute(
                f"""UPDATE {cls.__tablename__} 
                SET birth_date = ?, message = ?, remind_date = ?
                WHERE telegram_id = ? AND name = ?""",
                (birth_date, message, remind_date, telegram_id, name))
            dbSession.conn.commit()
            return cls.getByUserAndName(telegram_id, name)

    @classmethod
    def getByUserAndName(cls, telegram_id: str, name: str) -> "BirthdayRemind":
        """Получает напоминание по пользователю и имени"""
        cursor = dbSession.cursor
        cursor.execute(
            f"SELECT id, name, birth_date, message, remind_date, telegram_id "
            f"FROM {cls.__tablename__} "
            "WHERE telegram_id = ? AND name = ? LIMIT 1",
            (telegram_id, name))
        result = cursor.fetchone()
        if not result:
            raise ValueError("Birthday reminder not found")
        return cls(*result)


class User():
    __tablename__ = "User"
    
    def __init__(self, id: int, telegram_id: str):
        self.id = id
        self.telegram_id = telegram_id

    @classmethod
    def getCreate(cls, telegram_id: str) -> "User":
        """Создает или возвращает существующего пользователя"""
        cursor = dbSession.cursor
        
        try:
            # Пытаемся создать нового пользователя
            cursor.execute(
                f"INSERT INTO {cls.__tablename__} (telegram_id) VALUES (?)",
                (telegram_id,)
            )
            user_id = cursor.lastrowid
            dbSession.conn.commit()
            return cls(id=user_id, telegram_id=telegram_id)
            
        except sqlite3.IntegrityError:
            # Если пользователь уже существует, получаем его данные
            dbSession.conn.rollback()
            cursor.execute(
                f"SELECT id, telegram_id FROM {cls.__tablename__} "
                "WHERE telegram_id = ? LIMIT 1",
                (telegram_id,)
            )
            result = cursor.fetchone()
            dbSession.conn.commit()
            
            if not result:
                raise ValueError("User not found after integrity error")
                
            return cls(id=result[0], telegram_id=result[1])
        
    def add_birthday(self, name: str, birth_date: str, remind_date: str, message: str = "") -> BirthdayRemind:
        """Добавляет или обновляет напоминание о дне рождения"""
        return BirthdayRemind.getCreate(
            telegram_id=self.telegram_id,
            name=name,
            birth_date=birth_date,
            remind_date=remind_date,
            message=message
        )