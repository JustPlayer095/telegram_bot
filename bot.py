from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
import logging
import os
from dotenv import load_dotenv
from database import init_db, save_message, get_user_messages_with_ids, delete_user_messages, delete_specific_message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# States
class MessageStates(StatesGroup):
    waiting_for_message_number = State()

# Create keyboard layouts
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 View My Messages"),
                KeyboardButton(text="🗑️ Clear Messages")
            ],
            [
                KeyboardButton(text="ℹ️ Help"),
                KeyboardButton(text="❓ About")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_messages_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔙 Back to Menu")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Welcome to Message Storage Bot!\n\n"
        "I can help you store and manage your messages. Use the buttons below to interact with me.",
        reply_markup=get_main_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📚 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/mymessages - View your saved messages\n"
        "/clear - Delete all your messages\n\n"
        "To delete a specific message:\n"
        "1. View your messages\n"
        "2. Type the number of the message you want to delete\n"
        "3. Confirm the deletion",
        reply_markup=get_main_keyboard()
    )

@dp.message(lambda message: message.text == "📝 View My Messages")
async def process_view_messages(message: Message, state: FSMContext):
    user_id = message.from_user.id
    messages = get_user_messages_with_ids(user_id)
    
    if not messages:
        await message.answer(
            "📭 You don't have any saved messages yet.\n"
            "Send me any message to save it!",
            reply_markup=get_main_keyboard()
        )
    else:
        # Show list of messages
        response = "📜 Your saved messages:\n\n"
        for i, (msg_id, text, timestamp) in enumerate(messages, 1):
            response += f"{i}. {text} (at {timestamp})\n"
        
        response += "\nTo delete a message, type its number (e.g., '1' for the first message)\n"
        response += "Or click '🔙 Back to Menu' to return to the main menu"
        
        # Store messages in state for later use
        await state.update_data(messages=messages)
        await state.set_state(MessageStates.waiting_for_message_number)
        
        await message.answer(
            response,
            reply_markup=get_messages_keyboard()
        )

@dp.message(lambda message: message.text == "🔙 Back to Menu")
async def process_back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏠 Returning to main menu...",
        reply_markup=get_main_keyboard()
    )

@dp.message(MessageStates.waiting_for_message_number)
async def process_message_number(message: Message, state: FSMContext):
    try:
        message_number = int(message.text)
        data = await state.get_data()
        messages = data.get('messages', [])
        
        if 1 <= message_number <= len(messages):
            msg_id = messages[message_number - 1][0]  # Get the message ID
            if delete_specific_message(msg_id, message.from_user.id):
                await message.answer(
                    "✅ Message deleted successfully!",
                    reply_markup=get_main_keyboard()
                )
            else:
                await message.answer(
                    "❌ Failed to delete message. Please try again later.",
                    reply_markup=get_main_keyboard()
                )
        else:
            await message.answer(
                f"❌ Please enter a valid message number (1-{len(messages)}).",
                reply_markup=get_main_keyboard()
            )
    except ValueError:
        await message.answer(
            "❌ Please enter a valid number.",
            reply_markup=get_main_keyboard()
        )
    
    await state.clear()

@dp.message(lambda message: message.text == "🗑️ Clear Messages")
async def process_clear_messages(message: Message):
    user_id = message.from_user.id
    if delete_user_messages(user_id):
        await message.answer(
            "✅ All your messages have been successfully deleted!",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            "❌ Failed to delete messages. Please try again later.",
            reply_markup=get_main_keyboard()
        )

@dp.message(lambda message: message.text == "ℹ️ Help")
async def process_help(message: Message):
    await message.answer(
        "📚 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/mymessages - View your saved messages\n"
        "/clear - Delete all your messages\n\n"
        "To delete a specific message:\n"
        "1. View your messages\n"
        "2. Type the number of the message you want to delete\n"
        "3. Confirm the deletion",
        reply_markup=get_main_keyboard()
    )

@dp.message(lambda message: message.text == "❓ About")
async def process_about(message: Message):
    await message.answer(
        "🤖 About Message Storage Bot\n\n"
        "Version: 1.0\n"
        "This bot helps you store and manage your messages in a secure database.\n\n"
        "Features:\n"
        "• Save unlimited messages\n"
        "• View message history\n"
        "• Delete specific messages\n"
        "• Delete all messages\n"
        "• Easy-to-use interface",
        reply_markup=get_main_keyboard()
    )

@dp.message()
async def handle_message(message: Message, state: FSMContext):
    # Check if we're waiting for a message number
    current_state = await state.get_state()
    if current_state == MessageStates.waiting_for_message_number.state:
        await process_message_number(message, state)
        return
    
    # Handle regular message saving
    user_id = message.from_user.id
    message_text = message.text
    
    if save_message(user_id, message_text):
        await message.answer(
            "✅ Message saved successfully!",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            "❌ Sorry, I couldn't save your message. Please try again later.",
            reply_markup=get_main_keyboard()
        )

async def main():
    # Initialize database
    init_db()
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 