# https://github.com/ChainBoy300/Ultimate-Potato-Master
import os
import json
import logging
import typing
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
from cryptography.fernet import Fernet


# IMPORTANT VARIABLES
# IF SELF HOSTING, SET THIS TO YOUR DISCORD ID (ex: owner_id: int = 123456789123456789)
owner_id: int = int(os.getenv('MY_DISCORD_ID'))


# Main function
def main() -> None:
    # Initializes an instance of the bot
    bot = Bot()

    # Modules to be loaded by default
    modules: list[str] = ['hg']

    # When the bot is ready to go
    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')
        for module in modules:
            try:
                await bot.load_extension(module)
            except commands.ExtensionFailed:
                print(f'{module.capitalize()} failed to load!')
                raise commands.ExtensionFailed
            else:
                print(f'{module.capitalize()} has loaded.')

    # Initial setup when the bot joins a new guild
    @bot.event
    async def on_guild_join(join_guild):
        configure_files(join_guild)

    # Configure files for a specified guild or current
    @bot.command(name='config_files', description='Configure files for current server or server of given ID')
    @commands.guild_only()
    async def config_files(ctx: commands.Context, guild_id: typing.Optional[int] = None) -> discord.Message or None:
        """
        Command to configure the initial folders/files of a guild.

        :param ctx:
        :param guild_id: Guild ID.
        :return: An error or nothing.
        """
        # Only one person can use this command as well, this is returned if someone else tries to use it
        if ctx.author.id != owner_id:
            return await ctx.send('You are not allowed to do this!', ephemeral=True)

        # If a guild ID is given, configure files for that guild
        if guild_id:
            guild: discord.Guild = bot.get_guild(guild_id)
            if guild:
                configure_files(guild)
                await ctx.send("Files for specified server have been created.")
            else:
                await ctx.send("I do not have access to that server or it doesn't exist!")
        else:
            configure_files(ctx.guild)
            await ctx.send("Files for current server have been created.")

    # SYNC command, to sync all the slash commands (IMPORTANT!)
    @bot.hybrid_command(name='sync', description='Sync globally or to the current server.')
    @commands.guild_only()
    async def sync_commands(ctx: commands.Context, guild_id: typing.Optional[int] = None) -> discord.Message or None:
        """
        Command to sync app_commands.

        :param ctx:
        :param guild_id: Guild ID.
        :return: An error or nothing.
        """
        # Only one person can use the sync command, this is returned if someone else tries to use it
        if ctx.author.id != owner_id:
            return await ctx.send('You are not allowed to do this!', ephemeral=True)

        # If a guild ID is given, sync commands to that guild
        if guild_id:
            guild: discord.Guild = bot.get_guild(guild_id)
            if guild:
                synced = await bot.tree.sync(guild=guild)
                await ctx.send(f"Synced {len(synced)} commands to the given guild.", ephemeral=True)
            else:
                await ctx.send("I could not sync commands to that server!")
        # If no guild ID is given, sync commands globally
        else:
            synced = await bot.tree.sync()
            await ctx.send(f"Synced {len(synced)} commands globally.", ephemeral=True)

    # COMMAND RELATING TO MODULES HERE
    @bot.hybrid_command(name='module', description='Reload, unload or load modules.')
    @commands.guild_only()
    async def modify_modules(ctx: commands.Context, option: typing.Literal["reload", "unload", "load"],
                             value: str = None) -> discord.Message or None:
        """
        Command to manipulate bot modules.

        :param ctx:
        :param option: Action to be executed by the command.
        :param value: Module to be manipulated.
        :return: An error or nothing.
        """
        # Only one person can use this command as well, this is returned if someone else tries to use it
        if ctx.author.id != owner_id:
            return await ctx.send('You are not allowed to do this!', ephemeral=True)

        # What the command will do for every option
        if option == 'load':  # Option chosen is 'load'
            try:
                await bot.load_extension(value)
            except commands.ExtensionFailed:
                await ctx.send(f"{value.capitalize()} failed to load!", ephemeral=True)
                raise commands.ExtensionFailed
            except commands.ExtensionNotFound:
                await ctx.send("No such extension.", ephemeral=True)
                raise commands.ExtensionNotFound
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"{value.capitalize()} was already loaded.", ephemeral=True)
                raise commands.ExtensionAlreadyLoaded
            except commands.NoEntryPointError:
                await ctx.send("Module not set up correctly.", ephemeral=True)
                raise commands.NoEntryPointError
            else:
                modules.append(value)
                await ctx.send(f"{value.capitalize()} loaded.", ephemeral=True)
        elif option == 'unload':  # Option chosen is 'unload'
            try:
                await bot.unload_extension(value)
            except commands.ExtensionNotFound:
                await ctx.send("No such extension.", ephemeral=True)
                raise commands.ExtensionNotFound
            except commands.ExtensionNotLoaded:
                await ctx.send(f"{value.capitalize()} was not loaded or does not exist.", ephemeral=True)
                raise commands.ExtensionNotLoaded
            else:
                modules.remove(value)
                await ctx.send(f"{value.capitalize()} unloaded.", ephemeral=True)
        else:  # Option chosen is 'reload'
            if value is None or value == '':  # No specific module is given, so reload all of them
                for module in modules:
                    try:
                        await bot.reload_extension(module)
                    except commands.ExtensionFailed:
                        await ctx.send(f"{module.capitalize()} failed to reload!", ephemeral=True)
                        raise commands.ExtensionFailed
                    except commands.ExtensionNotFound:
                        await ctx.send(f"{module.capitalize()} not found!", ephemeral=True)
                        raise commands.ExtensionNotFound
                    except commands.NoEntryPointError:
                        await ctx.send("Module not set up correctly.", ephemeral=True)
                        raise commands.NoEntryPointError
                    else:
                        await ctx.send(f"{module.capitalize()} reloaded.", ephemeral=True)
            else:  # A specific module is being reloaded
                try:
                    await bot.reload_extension(value)
                except commands.ExtensionFailed:
                    await ctx.send(f"{value.capitalize()} failed to reload!", ephemeral=True)
                    raise commands.ExtensionFailed
                except commands.ExtensionNotLoaded:
                    await ctx.send(f"{value.capitalize()} was not loaded!", ephemeral=True)
                    raise commands.ExtensionNotLoaded
                except commands.ExtensionNotFound:
                    await ctx.send(f"{value.capitalize()} not found!", ephemeral=True)
                    raise commands.ExtensionNotFound
                except commands.NoEntryPointError:
                    await ctx.send("Module not set up correctly.", ephemeral=True)
                    raise commands.NoEntryPointError
                else:
                    await ctx.send(f"{value.capitalize()} reloaded.", ephemeral=True)

    # Bot logging and bot token
    handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
    bot.run(os.getenv('TOKEN'), log_handler=handler)


# Initial bot configuration
def configure() -> None:
    """
    Configuration upon bot boot up.

    :return:
    """
    load_dotenv()  # Loads all environment variables from the .env file
    # Make the initial path for data storage IF it does not exist
    Path("../data").mkdir(parents=True, exist_ok=True)


def configure_files(guild: discord.Guild) -> None:
    """
    Configures the initial folders/files of a guild.

    :param guild: The guild object, aka guild being affected.
    :return:
    """
    path: str = f"../data/{guild.id}"  # Guild storage path

    # Folder to store all data for a guild
    Path(path).mkdir(parents=True, exist_ok=True)
    # Folder to store custom messages
    Path(f"{path}/messages").mkdir(parents=True, exist_ok=True)
    # Folder to store players
    Path(f"{path}/players").mkdir(parents=True, exist_ok=True)

    # Initial server configuration
    config_dict: dict = {
        "guild": guild.name,
        "running": False,
        "stopping": False,
        "only_custom_messages": False
    }
    with Path(f"{path}/config.json").open(mode="w") as conf:
        json.dump(config_dict, conf)

    # Makes the json for alive custom messages if it does not exist
    if not Path(f"{path}/messages/alive.json").exists():
        Path(f"{path}/messages/alive.json").open(mode="x").close()

    # Makes the json for dead custom messages if it does not exist
    if not Path(f"{path}/messages/dead.json").exists():
        Path(f"{path}/messages/dead.json").open(mode="x").close()

    # Makes the json for lucky custom messages if it does not exist
    if not Path(f"{path}/messages/lucky.json").exists():
        Path(f"{path}/messages/lucky.json").open(mode="x").close()


# ENCRYPTION
def generate_key() -> None:
    """
    Generates a Fernet key and stores it as a file. THIS FILE IS IMPORTANT, KEEP IT SAFE!

    :return:
    """
    key = Fernet.generate_key()
    with Path('../data/encryption.key').open('wb') as key_file:
        key_file.write(key)


def load_key() -> bytes:
    """
    Reads the encryption key file and returns it as bytes, which are usable by Fernet.

    :return:
    """
    return Path('../data/encryption.key').open('rb').read()


# Sets up the bot object
class Bot(commands.Bot):
    def __init__(self):
        intents: discord.Intents = discord.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned_or('$$'), intents=intents)


# Runs everything
if __name__ == '__main__':
    # generate_key()  # UNCOMMENT THIS UPON FIRST BOOT UP, THEN COMMENT AGAIN!
    configure()  # Initial configuration
    main()  # The MEAT of the bot :)
