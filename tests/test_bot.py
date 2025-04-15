import unittest
from bot import get_main_keyboard, get_messages_keyboard
import pytest
from bot import Bot

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

def test_bot_initialization():
    bot = Bot()
    assert bot is not None

def test_message_storage():
    bot = Bot()
    test_message = "Test message"
    bot.store_message(test_message)
    assert test_message in bot.get_messages()

def test_message_deletion():
    bot = Bot()
    test_message = "Test message"
    bot.store_message(test_message)
    bot.delete_message(0)
    assert test_message not in bot.get_messages()

if __name__ == '__main__':
    unittest.main() 