import asyncio
import logging
from datetime import datetime, timedelta, date
from db.models import SessionLocal, BirthdayRemind

# Настройка логгера
logger = logging.getLogger(__name__)

class DataCheck:
    def __init__(self, check_dates=None, check_interval=600):
        """
        :param check_dates: Список дней недели для проверки (по умолчанию [0, 3]).
        :param check_interval: Интервал проверки в секундах (по умолчанию 600 секунд).
        """
        self.session = SessionLocal()
        self.check_dates = check_dates if check_dates is not None else [0, 3]
        self.check_interval = check_interval
        logger.info("DataCheck инициализирован с параметрами: check_dates=%s, check_interval=%s", self.check_dates, self.check_interval)

    async def _fetch_all_data(self):
        """Метод получения всех напоминаний из базы данных"""
        try:
            logger.info("Получение всех напоминаний из базы данных...")
            reminders = self.session.query(BirthdayRemind).all()
            logger.info("Получено %d напоминаний", len(reminders))
            return reminders
        except Exception as e:
            logger.error("Ошибка при получении данных из базы: %s", e)
            return []
        finally:
            self.session.close()
            logger.info("Сессия базы данных закрыта.")

    async def fetch_loop(self) -> None:
        """
        Циклическая проверка базы данных в указанные дни недели.
        """
        try:
            while True:
                now = datetime.now().weekday()
                if now in self.check_dates:
                    logger.info("Сегодня день проверки (день недели: %d)", now)
                    reminders = await self._fetch_all_data()
                    filtered_reminders = await self._filter_dates(reminders)
                    logger.info("Напоминания для обработки: %s", filtered_reminders)
                else:
                    logger.info("Сегодня не день проверки (день недели: %d)", now)
                await asyncio.sleep(self.check_interval)  # Интервал проверки
        except Exception as e:
            logger.error("Ошибка в цикле проверки: %s", e)

    async def _filter_dates(self, reminders):
        """
        Метод отбора напоминаний, которые актуальны для обработки.
        :param reminders: Список всех напоминаний из базы данных.
        :return: Список напоминаний, которые нужно обработать.
        """
        now = datetime.now()
        last_week = now - timedelta(weeks=1)
        filtered_reminders = [
            reminder for reminder in reminders
            if reminder.remind_date and reminder.remind_date > last_week.date()
        ]
        logger.info("Отфильтровано %d напоминаний для обработки", len(filtered_reminders))
        return filtered_reminders


class ReminderChecker:
    def __init__(self, bot, check_interval=600):
        """
        :param bot: Экземпляр бота.
        :param check_interval: Интервал проверки в секундах (по умолчанию 600 секунд).
        """
        self.bot = bot  # Сохраняем объект бота
        self.session = SessionLocal()
        self.check_interval = check_interval
        self.stop_event = asyncio.Event()  # Флаг для остановки цикла
        logger.info("ReminderChecker инициализирован с параметром: check_interval=%s", self.check_interval)

    async def check_reminders(self):
        """Метод проверки напоминаний и отправки сообщений"""
        while not self.stop_event.is_set():  # Проверяем, установлен ли флаг остановки
            try:
                today = date.today()
                logger.info("Проверка напоминаний на дату: %s", today)
                # Получаем напоминания на текущую дату
                reminders = self.session.query(BirthdayRemind).filter_by(remind_date=today).all()
                logger.info("Найдено %d напоминаний для сегодняшней даты", len(reminders))

                for reminder in reminders:
                    telegram_id = reminder.telegram_id
                    message = reminder.message

                    # Отправляем сообщение пользователю
                    logger.info("Отправка напоминания пользователю telegram_id=%s: %s", telegram_id, message)
                    await self.bot.send_message(telegram_id, f"Напоминание: {message}")

                    # Удаляем напоминание или обновляем remind_date (например, на следующий год)
                    self.session.delete(reminder)
                    logger.info("Напоминание для telegram_id=%s удалено из базы", telegram_id)

                self.session.commit()
                logger.info("Изменения в базе данных успешно сохранены.")
            except Exception as e:
                logger.error("Ошибка при проверке напоминаний: %s", e)
            finally:
                # Интервал проверки
                logger.info("Ожидание %d секунд до следующей проверки", self.check_interval)
                await asyncio.sleep(self.check_interval)

    async def stop(self):
        """Останавливает цикл проверки напоминаний"""
        self.stop_event.set()

    async def start(self):
        """Запуск проверки напоминаний"""
        logger.info("Запуск проверки напоминаний...")
        await self.check_reminders()
