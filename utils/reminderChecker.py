from db import User, ModelAdmin

# TODO: Переписать под новый db.models

# - TODO: Асинхронный класс N, для получения всей базы данных раз в X недель(Дней)
#   TODO: кеширования дат на неделе в виде json'a и постоянной его проверкой раз в день

# (I)internal method, (E) - External
# Структура: cacheDriver classmethoods
# 1 (E) adminModel.all() -> (dict) Метод получения базы данных каждый понедельник (Используем adminModel) : Корутина -> dict
# 1.1 (E) Метод получения новых данных (Напрямую, не через db) (Должен вызываться перед добавлением/изменением полей db) : Корутина -> dict (в таком же виде того, что выдаёт метод выше)
#
# 2 (I) Метод отбора дат для кеширования (Выбираем из dict метода 1) : Корутина -> dict
# 3 (I) Метод кеширования пользователей используя модуль jsonActions (Я переделаю модуль configActions) : Корутина (Создаёт файл или перезаписывает его)

# Структура: dateChecker classmehoods
# 1 (E) Метод сравнения времени два раза в день из кешированных пользователей (Через jsonActions) : Корутина
# 1.1  (I) Метод 


# В пизду эту мешанину сверху. Я лучше просто хуйни накалякаю и спокойно выдохну

import asyncio
import json
from datetime import datetime, timedelta


class dataCheck:
    def __init__(self, adminModel=ModelAdmin):
        self.adminModel = adminModel
    
    async def _fetchAllData(self):
        """Метод получения всей базы данных"""
        return await self.adminModel.all()
    
    async def fetchLoop(self, checkDates=[0,3]) -> None:
        """:param: checkDates: Понедельник - 0,  Четверг - 3"""
        try:
            while True:
                now = datetime.weekday()
                if now in checkDates:
                    await self._fetchAllData()
                await asyncio.sleep(600)
        except Exception:
            pass
            
    
    async def _filterDates(self, data): # Хадкод
        """Метод отбора дат для кеширования"""
        now = datetime.now()
        lastWeek = now - timedelta(weeks=1)
        filteredData = {k: v for k, v in data.items() if datetime.fromisoformat(v['date']) > lastWeek}
        return filteredData
    
        
        



'''
class CacheDriver:
    def __init__(self, admin_model):
        self.admin_model = admin_model
        self.cache_file = 'cache.json'
        self.cache = {}
        self.last_update = None

    async def fetch_all_data(self):
        """Метод получения всей базы данных (E)"""
        return await self.admin_model.all()

    async def fetch_new_data(self):
        """Метод получения новых данных (E)"""
        # Здесь можно реализовать логику для получения только новых данных
        return await self.admin_model.all()

    async def filter_dates(self, data):
        """Метод отбора дат для кеширования (I)"""
        # Пример: отбираем данные за последнюю неделю
        now = datetime.now()
        last_week = now - timedelta(weeks=1)
        filtered_data = {k: v for k, v in data.items() if datetime.fromisoformat(v['date']) > last_week}
        return filtered_data

    async def cache_data(self, data):
        """Метод кеширования данных (I)"""
        self.cache = data
        self.last_update = datetime.now()
        with open(self.cache_file, 'w') as f:
            json.dump(data, f)

    async def load_cache(self):
        """Метод загрузки кеша из файла"""
        try:
            with open(self.cache_file, 'r') as f:
                self.cache = json.load(f)
        except FileNotFoundError:
            self.cache = {}

    async def update_cache(self):
        """Метод обновления кеша"""
        data = await self.fetch_all_data()
        filtered_data = await self.filter_dates(data)
        await self.cache_data(filtered_data)

'''
# '''Реализация дерьма. Делаю класс выше'''
# async def check_reminders():
#     while True:
#         today = date.today()
        
        
        
#         cursor.execute('SELECT telegram_id, message FROM "birthday_remind" WHERE remind_date = ?', (today,))
#         reminders = cursor.fetchall() 

#         for reminder in reminders:
#             telegram_id, message = reminder
#             await bot.send_message(telegram_id, f"Напоминание: {message}")

#         # Удаляем отправленные напоминания (или обновляем remind_date на следующий год)
#         cursor.execute('DELETE FROM "birthday_remind" WHERE remind_date = ?', (today,))
#         conn.commit()

#         # Проверяем напоминания каждые 60 секунд
#         await asyncio.sleep(600)