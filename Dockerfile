FROM python:3.10-alpine
WORKDIR /BIRTHDAY-BOT
ENV BOT_APP=bot.py
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
# ENTRYPOINT [ "sleep", "10000" ]
ENTRYPOINT [ "python","bot.py","--debug" ]