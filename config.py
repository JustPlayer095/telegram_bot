import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    # If not in environment, try to read from file
    try:
        with open('/app/token.txt', 'r') as f:
            BOT_TOKEN = f.read().strip()
    except FileNotFoundError:
        raise ValueError("BOT_TOKEN not found in environment or token.txt file!")

# Database configuration
DB_NAME = os.getenv('DB_NAME', 'telegram_bot_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432') 