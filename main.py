import os
import json
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
		response = requests.get(long_polling_url, headers=header, params=params)
		response.raise_for_status()
		print(response.text)
		response_dict = json.loads(response.text)
		if response_dict.get("status") == "timeout" and not response_dict.get("request_query"):
			timestamp = response_dict.get("timestamp_to_request")
			print("FIRST WAITING", timestamp)
		elif response_dict.get("status") == "timeout" and response_dict.get("request_query"):
			timestamp = response_dict.get("timestamp_to_request")
			print("AGAIN WAITING", timestamp)
		elif response_dict.get("status") == "found" and not response_dict.get("request_query"):
			timestamp = response_dict.get("last_attempt_timestamp")
			print("GOT IT FAST", timestamp)
		elif response_dict.get("status") == "found" and response_dict.get("request_query"):
			timestamp = response_dict.get("last_attempt_timestamp")
			print("GOT IT", timestamp)
		else:
			print("!!!!!!!!!!!!!!!!!!!!!!")


if __name__ == "__main__":
    main()
