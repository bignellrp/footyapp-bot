import unittest
from unittest.mock import Mock, patch, AsyncMock

from cogs.admincommands import AdminCommands


class TestNewCommand(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = Mock()
        self.cog = AdminCommands(self.bot)
        self.ctx = Mock()
        self.ctx.send = AsyncMock()

    @patch('cogs.admincommands.add_player')
    @patch('cogs.admincommands.validate_name', return_value=True)
    @patch('cogs.admincommands.player_names', return_value=[])
    async def test_new_command_adds_player(self, mock_player_names, mock_validate_name, mock_add_player):
        await self.cog.new.callback(self.cog, self.ctx, 'player1')
        mock_add_player.assert_called_once_with('player1')
        self.ctx.send.assert_called_once_with('Added new player with a generic score of 77: player1')

if __name__ == '__main__':
    unittest.main()