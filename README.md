# Buy Me a Coffee Notifier

This script sends you a Telegram message whenever someone buys a coffee for a specified creator on Buy Me a Coffee.

## Setup

1. Clone this repository.
2. Install the required dependencies via `pip install -r requirements.txt`.
3. Create a `.env` file with your Telegram information:

```env
TELEGRAM_API_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

4. Run the script via `python main.py username`. Replace `username` with the username of the creator you want to track.

The script checks for new coffees every hour by default. To change this, add a number of seconds after your username. Example: `python main.py username 900` (checks every 15 minutes).
