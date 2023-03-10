import json
import os
import typing
import discord
from discord import app_commands
from discord.ext import commands
from cryptography.fernet import Fernet
from pathlib import Path
import fnmatch
from main import load_key

# Load encryption key for later use
f = Fernet(load_key())


def decryptDecode(data: str) -> str:
    """
    Decrypts and decodes a piece of data using Fernet.

    :param data: The data to be decrypted, then turned into a string.
    :return:
    """
    return f.decrypt(data).decode('utf-8')


# Hunger Games Module?
# noinspection PyUnresolvedReferences
class HG(commands.GroupCog, name='hg', description='The main subcommand of hunger games.'):
    def __init__(self, bot):
        self.bot = bot

    """
        Main commands of the Hunger Games module:
            /hg start
            /hg stop
    """

    @app_commands.command(name='start', description='Start the hunger games!')
    @app_commands.guild_only()
    async def start(self, interaction: discord.Interaction) -> None:
        """ Starts the hunger games simulation. """

    @app_commands.command(name='stop', description='Stop the game at the end of the current day.')
    @app_commands.guild_only()
    async def stop(self, interaction: discord.Interaction) -> None:
        """ Stops the hunger games simulation. """

    """
        Message subgroup of the Hunger Games module, includes:
            /hg message list [type]
            /hg message add [type] [message]
            /hg message remove [type] [id]
    """
    message_sub = app_commands.Group(name='message', description='The messages subgroup of hg.', guild_only=True)

    """
        Player subgroup of the Hunger Games module, includes:
            /hg player include [option] [user]/[bot_user] [profile_url]
            /hg player exclude [option] [user]
    """
    player_sub = app_commands.Group(name='player', description='The players subgroup of hg.', guild_only=True)

    @player_sub.command(name='include', description='Add a player to be in the simulation.')
    async def include(self, interaction: discord.Interaction, option: typing.Literal["all", "user", "bot"],
                      user: typing.Optional[discord.User], bot_name: typing.Optional[str],
                      profile_url: typing.Optional[str]):
        """

        :param interaction:
        :param option:
        :param user:
        :param bot_name:
        :param profile_url:
        :return:
        """
        if option == 'all':
            for user_object in interaction.guild.members:
                user_info = {
                    "id": user_object.id,
                    "name": f.encrypt(user_object.name.encode('utf-8')).decode('utf-8'),
                    "display_name": f.encrypt(user_object.display_name.encode('utf-8')).decode('utf-8'),
                    "avatar": f.encrypt(user_object.display_avatar.url.encode('utf-8')).decode('utf-8')
                }

                with Path(f'../data/guilds/{interaction.guild.id}/players/{user_object.id}.json').open('w') as i:
                    json.dump(user_info, i)

            return await interaction.response.send_message('All players have been included.')
        elif option == 'user':
            return await interaction.response.send_message('Work in progress.')
        else:
            return await interaction.response.send_message('Work in progress.')

    @player_sub.command(name='exclude', description='Remove a player from the simulation')
    async def exclude(self, interaction: discord.Interaction, option: typing.Literal["all", "user", "bot"],
                      user: typing.Optional[discord.User], bot_id: typing.Optional[int]):
        if option == 'all':
            player_total = len(fnmatch.filter(os.listdir(f'../data/guilds/{interaction.guild.id}/players'), '*.json'))
            for i in Path(f'../data/guilds/{interaction.guild.id}/players').glob('*.json'):
                os.remove(i)
            return await interaction.response.send_message(f'{player_total} players removed.')
        elif option == 'user':
            return await interaction.response.send_message('Work in progress.')
        else:
            return await interaction.response.send_message('Work in progress.')

    """
        Config subgroup of the Hunger Games module, includes:
            /hg config repair
            /hg config only_custom_messages [option]
    """
    config_sub = app_commands.Group(name='config', description='The configuration subgroup of hg.', guild_only=True)


# Adds the module/extension to the main bot
async def setup(bot):
    await bot.add_cog(HG(bot))