import os
import time
import logging
import requests
import telegram

from textwrap import dedent
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(process)d %(levelname)s %(message)s",
        )


def handle_response(response, bot, chat_id):
    task_review = response.json()
    if task_review.get("status") == "timeout":
        timestamp = task_review.get("timestamp_to_request")
        message = None
    elif task_review.get("status") == "found":
        logger.info("Получен ответ:")
        timestamp = task_review.get("last_attempt_timestamp")
        for attempt in task_review["new_attempts"]:
            if attempt["is_negative"]:
                status_message = "Доделайте работу и отправьте снова."
            elif not attempt["is_negative"]:
                status_message = dedent("""
                    Преподавателю всё понравилось.
                    Можно приступать к следующему уроку!
                """)
            message = dedent(f"""
                С проверки вернулась работа "{attempt["lesson_title"]}".

                {status_message}

                {attempt["lesson_url"]}
            """)
    while message:
        try:
            bot.send_message(
                chat_id=chat_id,
                text=message,
            )
            return True
        except telegram.error.NetworkError as error:
            logger.error(error, exc_info=True)
            time.sleep(1)
    return timestamp


def main():
    load_dotenv()
    devman_token = os.environ["DEVMAN_TOKEN"]
    long_polling_url = "https://dvmn.org/api/long_polling/"
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    bot = telegram.Bot(token=telegram_token)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    header = {
        "Authorization": f"Token {devman_token}",
    }
    timestamp = None
    while True:
        params = {
            "timestamp": timestamp,
        }
        try:
            response = requests.get(
                long_polling_url,
                headers=header,
                params=params,
            )
            response.raise_for_status()
            timestamp = handle_response(response, bot, chat_id)
        except requests.exceptions.ReadTimeout as error:
            logger.error(error, exc_info=True)
            continue
        except requests.exceptions.ConnectionError as error:
            logger.error(error, exc_info=True)
            time.sleep(1)
            continue


if __name__ == "__main__":
    main()
