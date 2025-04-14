# Telegram Message Storage Bot

A simple Telegram bot that helps you store and manage your messages.

## Features
- Save messages
- View your message history
- Delete specific messages
- Delete all messages
- Simple and intuitive interface

## Setup

### Local Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your bot token:
```
BOT_TOKEN=your_bot_token_here
```

3. Run the bot:
```bash
python bot.py
```

### Docker Setup
1. Build the Docker image:
```bash
docker build -t telegram-bot .
```

2. Run the container:
```bash
docker run -d --name telegram-bot \
  -e BOT_TOKEN=your_bot_token_here \
  telegram-bot
```

3. To view logs:
```bash
docker logs telegram-bot
```

4. To stop the bot:
```bash
docker stop telegram-bot
```

## Usage
- Send any message to save it
- Use the keyboard buttons to:
  - View your messages
  - Clear all messages
  - Get help
  - View about information
- To delete a specific message:
  1. Click "View My Messages"
  2. Type the number of the message you want to delete
  3. The message will be deleted automatically

## Requirements
- Python 3.7+ or Docker
- aiogram
- python-dotenv 