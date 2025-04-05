from ..db import User, dbSession
from datetime import date

def run_full_cycle_test():
    # 1. Инициализация тестовых данных
    test_telegram_id = "TEST_12345"
    test_data = {
        "name": "Тестовый Пользователь",
        "birth_date": "1990-01-01",
        "remind_date": str(date.today()),
        "message": "Тестовое напоминание"
    }

    try:
        # 2. Тестирование создания пользователя
        print("=== Тест создания пользователя ===")
        user = User.getCreate(test_telegram_id)
        print(f"✅ Пользователь создан: ID={user.id}, TelegramID={user.telegram_id}")

        # 3. Тестирование добавления дня рождения
        print("\n=== Тест добавления дня рождения ===")
        birthday = user.add_birthday(
            name=test_data["name"],
            birth_date=test_data["birth_date"],
            remind_date=test_data["remind_date"],
            message=test_data["message"]
        )
        print(f"✅ Напоминание добавлено: ID={birthday.id}")
        print(f"Детали: {birthday.name}, {birthday.birth_date}, {birthday.message}")

        # 4. Тестирование получения данных
        print("\n=== Тест получения данных ===")
        same_user = User.getCreate(test_telegram_id)
        print(f"🔍 Поиск пользователя: {same_user.telegram_id}")

        # 5. Проверка целостности данных
        assert same_user.id == user.id, "Ошибка: ID пользователя не совпадают"
        assert same_user.telegram_id == test_telegram_id, "Ошибка: TelegramID не совпадает"

        # 6. Проверка существования напоминания
        print("\n=== Проверка напоминания ===")
        cursor = dbSession.cursor
        cursor.execute(
            "SELECT * FROM birthday_remind WHERE telegram_id = ? AND name = ?",
            (test_telegram_id, test_data["name"])
        )
        result = cursor.fetchone()
        
        if result:
            print(f"✅ Напоминание найдено в базе: ID={result[0]}")
            print("Проверка данных:")
            assert result[2] == test_data["birth_date"], "Дата рождения не совпадает"
            assert result[4] == test_data["remind_date"], "Дата напоминания не совпадает"
            print("Все данные верны!")
        else:
            raise Exception("Напоминание не найдено в базе данных")

        # 7. Очистка тестовых данных
        print("\n=== Очистка тестовых данных ===")
        cursor.execute("DELETE FROM birthday_remind WHERE telegram_id = ?", (test_telegram_id,))
        cursor.execute("DELETE FROM User WHERE telegram_id = ?", (test_telegram_id,))
        dbSession.conn.commit()
        print("✅ Тестовые данные удалены")

    except Exception as e:
        print(f"❌ Тест провален: {str(e)}")
        dbSession.conn.rollback()
    finally:
        dbSession.conn.close()

if __name__ == "__main__":
    run_full_cycle_test()