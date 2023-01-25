import os
import json
import time
import requests

from dotenv import load_dotenv


def main():
	load_dotenv()
	token = os.environ["DEVMAN_TOKEN"]
	long_polling_url = "https://dvmn.org/api/long_polling/"
	header = {
		"Authorization": f"Token {token}",
	}
	timestamp = None
	while True:
		params = {
			"timestamp": timestamp,
		}
		try:
			response = requests.get(long_polling_url, headers=header, params=params)
			response.raise_for_status()
			print(response.text)
			response_dict = json.loads(response.text)
			if response_dict.get("status") == "timeout" and not response_dict.get("request_query"):
				timestamp = response_dict.get("timestamp_to_request")
				print("WAITING FOR THE FIRST TIME", timestamp)
			elif response_dict.get("status") == "timeout" and response_dict.get("request_query"):
				timestamp = response_dict.get("timestamp_to_request")
				print("WAITING", timestamp)
			elif response_dict.get("status") == "found" and not response_dict.get("request_query"):
				timestamp = response_dict.get("last_attempt_timestamp")
				print("GOT IT FAST", timestamp)
			elif response_dict.get("status") == "found" and response_dict.get("request_query"):
				timestamp = response_dict.get("last_attempt_timestamp")
				print("GOT IT", timestamp)
			else:
				print("!!!!!!!!!!!!!!!!!!!!!!")
		except requests.exceptions.ReadTimeout as error:
			print("ERROR:", error)
			continue
		except requests.exceptions.ConnectionError as error:
			print("ERROR:", error)
			time.sleep(60)
			continue


if __name__ == "__main__":
    main()
