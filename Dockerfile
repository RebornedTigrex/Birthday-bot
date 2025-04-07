FROM python:3.12-slim

# Устанавливаем зависимости
WORKDIR /BIRTHDAY-BOT
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV BOT_APP=bot.py

# Копируем весь проект
COPY . .



EXPOSE 5000
# ENTRYPOINT [ "sleep", "10000" ]
ENTRYPOINT [ "python","bot.py","--debug" ]

# Указываем команду по умолчанию
CMD ["python", "bot.py"]