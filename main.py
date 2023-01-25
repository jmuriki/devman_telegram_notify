import os
import json
import time
import requests
import telegram

from dotenv import load_dotenv


def send_message(telegram_token, chat_id, message):
    bot = telegram.Bot(token=telegram_token)
    while True:
        try:
            bot.send_message(
                chat_id=chat_id,
                text=message,
            )
            return True
        except telegram.error.NetworkError:
            time.sleep(1)


def handle_response(raw_response, telegram_token, chat_id):
    response = json.loads(raw_response.text)
    if response.get("status") == "timeout":
        timestamp = response.get("timestamp_to_request")
        send_message(telegram_token, chat_id, "Ожидайте проверки.")
    elif response.get("status") == "found":
        timestamp = response.get("last_attempt_timestamp")
        for attempt in response["new_attempts"]:
            send_message(
                telegram_token,
                chat_id,
                f'С проверки вернулась работа "{attempt["lesson_title"]}".',
            )
            send_message(
                telegram_token,
                chat_id,
                attempt["lesson_url"],
            )
            if attempt["is_negative"]:
                send_message(
                    telegram_token,
                    chat_id,
                    "Доделайте работу и отправьте снова.",
                )
            elif not attempt["is_negative"]:
                send_message(
                    telegram_token,
                    chat_id,
                    "Преподавателю всё понравилось. \
                    Можно приступать к следующему уроку!",
                )
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
            raw_response = requests.get(
                long_polling_url,
                headers=header,
                params=params,
            )
            raw_response.raise_for_status()
            timestamp = handle_response(raw_response, telegram_token, chat_id)
        except requests.exceptions.ReadTimeout as error:
            print("ERROR", error)
            continue
        except requests.exceptions.ConnectionError as error:
            print("ERROR", error)
            time.sleep(1)
            continue


if __name__ == "__main__":
    main()
