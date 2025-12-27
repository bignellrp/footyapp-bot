import unittest
from unittest.mock import Mock, patch, AsyncMock
import discord
from cogs.commands import Commands
import asyncio


class TestStatsCommand(unittest.IsolatedAsyncioTestCase):
    """Test the stats command to ensure it handles player stats correctly"""
    
    async def asyncSetUp(self):
        """Set up test fixtures"""
        self.bot = Mock()
        self.commands_cog = Commands(self.bot)
        self.ctx = Mock()
        self.ctx.send = AsyncMock()
    
    @patch('cogs.commands.player_stats')
    @patch('cogs.commands.discord.File')
    async def test_stats_command_success(self, mock_file, mock_player_stats):
        """Test that stats command successfully formats and sends player stats"""
        # Mock the player_stats function to return sample data
        mock_player_stats.return_value = [
            ('Player1', 10, 5, 3, 18, 55.6),
            ('Player2', 8, 6, 4, 18, 44.4),
            ('Player3', 12, 3, 3, 18, 66.7)
        ]
        
        # Mock the discord.File constructor
        mock_file.return_value = Mock()
        
        # Call the callback method directly
        await self.commands_cog.stats.callback(self.commands_cog, self.ctx)
        
        # Verify player_stats was called
        mock_player_stats.assert_called_once()
        
        # Verify ctx.send was called
        self.ctx.send.assert_called_once()
        
        # Get the arguments passed to ctx.send
        call_args = self.ctx.send.call_args
        
        # Verify that an embed was sent
        self.assertIn('embed', call_args.kwargs)
        embed = call_args.kwargs['embed']
        
        # Verify embed properties
        self.assertEqual(embed.title, "Player Stats")
        self.assertEqual(embed.url, "https://footyapp.richardbignell.co.uk/stats")
        self.assertEqual(embed.color, discord.Color.green())
        
        # Verify embed has the expected field
        self.assertEqual(len(embed.fields), 1)
        self.assertEqual(embed.fields[0].name, "W|D|L|T|%|Name")
        
        # Verify the rows contain the expected data
        rows_value = embed.fields[0].value
        self.assertIn('Player1', rows_value)
        self.assertIn('Player2', rows_value)
        self.assertIn('Player3', rows_value)
        self.assertIn('10 | 5 | 3 | 18 | 55.6 | Player1', rows_value)
    
    @patch('cogs.commands.player_stats')
    @patch('cogs.commands.discord.File')
    async def test_stats_command_empty_data(self, mock_file, mock_player_stats):
        """Test that stats command handles empty player stats gracefully"""
        # Mock the player_stats function to return empty data
        mock_player_stats.return_value = []
        
        # Mock the discord.File constructor
        mock_file.return_value = Mock()
        
        # Call the callback method directly
        await self.commands_cog.stats.callback(self.commands_cog, self.ctx)
        
        # Verify player_stats was called
        mock_player_stats.assert_called_once()
        
        # Verify ctx.send was called
        self.ctx.send.assert_called_once()
        
        # Get the arguments passed to ctx.send
        call_args = self.ctx.send.call_args
        
        # Verify that an embed was sent even with empty data
        self.assertIn('embed', call_args.kwargs)
        embed = call_args.kwargs['embed']
        
        # Verify embed has a field with empty value
        self.assertEqual(len(embed.fields), 1)
        self.assertEqual(embed.fields[0].value, '')
    
    @patch('cogs.commands.player_stats')
    @patch('cogs.commands.discord.File')
    async def test_stats_command_no_unboundlocalerror(self, mock_file, mock_player_stats):
        """Test that stats command does not raise UnboundLocalError"""
        # This is the specific test for the bug fix
        # Mock the player_stats function
        mock_player_stats.return_value = [
            ('TestPlayer', 5, 2, 1, 8, 62.5)
        ]
        
        # Mock the discord.File constructor
        mock_file.return_value = Mock()
        
        # Call the callback method directly - should not raise UnboundLocalError
        try:
            await self.commands_cog.stats.callback(self.commands_cog, self.ctx)
            # If we get here, the command executed without error
            test_passed = True
        except UnboundLocalError as e:
            # If we get an UnboundLocalError, the bug still exists
            test_passed = False
            self.fail(f"UnboundLocalError was raised: {e}")
        
        self.assertTrue(test_passed, "stats command should not raise UnboundLocalError")
        
        # Verify the function was called correctly
        mock_player_stats.assert_called_once()


if __name__ == '__main__':
    unittest.main()
