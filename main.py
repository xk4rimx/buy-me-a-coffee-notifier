import argparse
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }

    response = requests.post(url, params=params)
    response.raise_for_status()


def get_latest_coffees(username: str):
    url = f"https://app.buymeacoffee.com/api/creators/slug/{username}/coffees"
    params = {
        "web": 1,
        "username": username,
        "page": 1,
        "per_page": 10,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    latest_coffees = []

    for coffee in data["data"]:
        latest_coffees.append(
            {
                "name": coffee["supporter_name"],
                "amount": coffee["support_coffees"],
                "date": coffee["support_created_on"],
            }
        )

    return latest_coffees


def make_coffee_message(coffee: dict) -> str:
    name = coffee["name"]
    amount = coffee["amount"]
    if amount > 1:
        message = f"{name} bought {amount} coffees!"
    else:
        message = f"{name} bought a coffee!"
    return message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "username",
        help="username of the Buy Me a Coffee creator",
    )
    parser.add_argument(
        "sleep",
        nargs="?",
        default=60 * 60,
        type=int,
        help="delay between checks in seconds",
    )

    args = parser.parse_args()
    username = args.username
    sleep = args.sleep

    old_latest_coffees = get_latest_coffees(username)
    try:
        while True:
            time.sleep(sleep)
            latest_coffees = get_latest_coffees(username)
            for coffee in latest_coffees:
                if coffee not in old_latest_coffees:
                    message = make_coffee_message(coffee)
                    send_telegram_message(message)
                    print(coffee["date"], message)
            old_latest_coffees = latest_coffees
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
