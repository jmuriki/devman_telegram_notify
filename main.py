import os
import requests

from dotenv import load_dotenv


def main():
	load_dotenv()
	token = os.environ["DEVMAN_TOKEN"]
	url = "https://dvmn.org/api/user_reviews/"
	header = {
		"Authorization": f"Token {token}",
	}
	response = requests.get(url, headers=header)
	response.raise_for_status()


if __name__ == "__main__":
    main()
