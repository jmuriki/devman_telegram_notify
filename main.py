import os
import json
import time
import requests
import telegram

from dotenv import load_dotenv


def send_message(telegram_token, chat_id, message):
	bot = telegram.Bot(token=telegram_token)
	bot.send_message(
        chat_id=chat_id,
        text=message,
    )

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
			response = requests.get(long_polling_url, headers=header, params=params)
			response.raise_for_status()
			message = "RESPONSE"
			print(message, response.text)
			send_message(telegram_token, chat_id, message)
			response_dict = json.loads(response.text)
			if response_dict.get("status") == "timeout" and not response_dict.get("request_query"):
				timestamp = response_dict.get("timestamp_to_request")
				message = "WAITING FOR THE FIRST TIME"
				print(message, timestamp)
				send_message(telegram_token, chat_id, message)
			elif response_dict.get("status") == "timeout" and response_dict.get("request_query"):
				timestamp = response_dict.get("timestamp_to_request")
				message = "WAITING"
				print(message, timestamp)
				send_message(telegram_token, chat_id, message)
			elif response_dict.get("status") == "found" and not response_dict.get("request_query"):
				timestamp = response_dict.get("last_attempt_timestamp")
				message = "GOT IT FAST"
				print(message, timestamp)
				send_message(telegram_token, chat_id, message)
			elif response_dict.get("status") == "found" and response_dict.get("request_query"):
				timestamp = response_dict.get("last_attempt_timestamp")
				message = "GOT IT"
				print(message, timestamp)
				send_message(telegram_token, chat_id, message)
			else:
				message = "!!!!!!!!!!!!!!!!!!!!!!"
				print(message)
				send_message(telegram_token, chat_id, message)
		except requests.exceptions.ReadTimeout as error:
			message = f"ERROR: {error}"
			print(message)
			send_message(telegram_token, chat_id, message)
			continue
		except requests.exceptions.ConnectionError as error:
			message = f"ERROR: {error}"
			print(message)
			send_message(telegram_token, chat_id, message)
			time.sleep(1)
			continue


if __name__ == "__main__":
    main()
