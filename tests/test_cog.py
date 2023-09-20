import unittest
from unittest.mock import Mock
from cogs.admincommands import new

class TestNewCommand(unittest.TestCase):
    def test_new_command(self):
        # Create a mock context
        ctx = Mock()

        # Create an instance of YourCog
        your_cog = new()

        # Call the new command function with test arguments
        your_cog.new(ctx, "player1")

        # Assert that ctx.send() was called with the expected message
        ctx.send.assert_called_once_with("Added new player with a generic score of 77: player1")

if __name__ == '__main__':
    unittest.main()