import json

import discord
from discord import app_commands
from discord.ext import commands


# Hunger Games Module?
class HG(commands.GroupCog, name='hg', description='The main subcommand of hunger games.'):
    def __init__(self, bot):
        self.bot = bot

    """
        Main commands of the Hunger Games module:
            /hg start
            /hg stop
    """

    @app_commands.command(name='start', description='Start the hunger games!')
    @commands.guild_only()
    async def start(self, interaction: discord.Interaction) -> None:
        """

        :param interaction:
        :return:
        """

    @app_commands.command(name='stop', description='Stop the game at the end of the current day.')
    @commands.guild_only()
    async def stop(self, interaction: discord.Interaction) -> None:
        """

        :param interaction:
        :return:
        """

    """
        Message subgroup of the Hunger Games module, includes:
            /hg message list [type]
            /hg message add [type] [message]
            /hg message remove [type] [id]
    """

    message_sub = app_commands.Group(name='message', description='The messages subgroup of hg.', guild_only=True)

    """
        Player subgroup of the Hunger Games module, includes:
            /hg player include [option] [optional user]
            /hg player exclude [option] [optional user]
    """

    player_sub = app_commands.Group(name='player', description='The players subgroup of hg.', guild_only=True)

    """
        Config subgroup of the Hunger Games module, includes:
            /hg config repair
            /hg config only_custom_messages [option]
    """

    config_sub = app_commands.Group(name='config', description='The configuration subgroup of hg.', guild_only=True)


# Adds the module/extension to the main bot
async def setup(bot):
    await bot.add_cog(HG(bot))