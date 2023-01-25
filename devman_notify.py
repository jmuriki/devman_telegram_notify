import os
import time
import requests
import telegram

from dotenv import load_dotenv


def handle_response(response, telegram_token, chat_id):
    bot = telegram.Bot(token=telegram_token)
    task_review = response.json()
    if task_review.get("status") == "timeout":
        timestamp = task_review.get("timestamp_to_request")
        message = None
    elif task_review.get("status") == "found":
        timestamp = task_review.get("last_attempt_timestamp")
        for attempt in task_review["new_attempts"]:
            if attempt["is_negative"]:
                status_message = "Доделайте работу и отправьте снова."
            elif not attempt["is_negative"]:
                status_message = """Преподавателю всё понравилось.
                    \nМожно приступать к следующему уроку!"""
            message = f"""
                С проверки вернулась работа "{attempt["lesson_title"]}".
                \n{status_message}\n
                \n{attempt["lesson_url"]}"""
    while message:
        try:
            bot.send_message(
                chat_id=chat_id,
                text=message,
            )
            return True
        except telegram.error.NetworkError:
            time.sleep(1)
    return timestamp


def main():
    load_dotenv()
    devman_token = os.environ["DEVMAN_TOKEN"]
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    long_polling_url = "https://dvmn.org/api/long_polling/"
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
            timestamp = handle_response(response, telegram_token, chat_id)
        except requests.exceptions.ReadTimeout as error:
            print("ERROR:", error)
            continue
        except requests.exceptions.ConnectionError as error:
            print("ERROR:", error)
            time.sleep(1)
            continue


if __name__ == "__main__":
    main()
