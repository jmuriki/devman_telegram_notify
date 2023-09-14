# syntax=docker/dockerfile:1

FROM python:3.9
RUN pip install requests==2.28.2 python-dotenv==0.21.1 python-telegram-bot==13.15
WORKDIR /app
COPY . .
CMD ["python", "devman_telegram_notify.py"]
