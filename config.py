import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Log all environment variables (except sensitive ones)
logger.info("Available environment variables:")
for key in os.environ:
    if key not in ['BOT_TOKEN', 'DB_PASSWORD']:  # Don't log sensitive data
        logger.info(f"{key}: {os.environ[key]}")

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
logger.info(f"BOT_TOKEN is set: {bool(BOT_TOKEN)}")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Database configuration
DB_NAME = os.getenv('DB_NAME', 'telegram_bot_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Log database configuration (without sensitive data)
logger.info(f"Database configuration:")
logger.info(f"DB_NAME: {DB_NAME}")
logger.info(f"DB_USER: {DB_USER}")
logger.info(f"DB_HOST: {DB_HOST}")
logger.info(f"DB_PORT: {DB_PORT}") 