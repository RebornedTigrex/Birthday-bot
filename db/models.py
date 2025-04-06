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

class User():
    def __init__(self, ):
        pass