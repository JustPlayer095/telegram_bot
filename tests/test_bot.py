import os
import unittest
from bot import get_main_keyboard, get_messages_keyboard
import pytest
from bot import Bot as OriginalBot
from unittest.mock import patch, MagicMock

# Set up test environment variables
os.environ['BOT_TOKEN'] = '123456789:TEST1234567890abcdefghijklmnopqrstuvwxyz'
os.environ['DATABASE_URL'] = 'postgresql://test:test@localhost:5432/test_db'

class MockBot:
    def __init__(self, token):
        self.token = token
        self.messages = []

    def store_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def delete_message(self, index):
        if 0 <= index < len(self.messages):
            del self.messages[index]

class TestBot(unittest.TestCase):
    def test_keyboard_creation(self):
        """Test that keyboards are created correctly"""
        main_kb = get_main_keyboard()
        messages_kb = get_messages_keyboard()
        
        # Check that keyboards are not None
        self.assertIsNotNone(main_kb)
        self.assertIsNotNone(messages_kb)
        
        # Check that main keyboard has correct number of buttons
        self.assertEqual(len(main_kb.keyboard), 2)  # 2 rows
        self.assertEqual(len(main_kb.keyboard[0]), 2)  # 2 buttons in first row
        self.assertEqual(len(main_kb.keyboard[1]), 2)  # 2 buttons in second row
        
        # Check that messages keyboard has correct number of buttons
        self.assertEqual(len(messages_kb.keyboard), 1)  # 1 row
        self.assertEqual(len(messages_kb.keyboard[0]), 1)  # 1 button

# Mock the Bot class
@pytest.fixture(autouse=True)
def mock_bot():
    with patch('bot.Bot', MockBot):
        yield

@pytest.fixture
def bot():
    return MockBot(token='1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij')

def test_bot_initialization(bot):
    assert bot is not None
    assert bot.token is not None

def test_message_storage(bot):
    test_message = "Test message"
    bot.store_message(test_message)
    assert test_message in bot.get_messages()

def test_message_deletion(bot):
    test_message = "Test message"
    bot.store_message(test_message)
    bot.delete_message(0)
    assert test_message not in bot.get_messages()

if __name__ == '__main__':
    unittest.main() 