import discord
from discord.ext import commands


# DEVELOPER ONLY module
class DEV(commands.GroupCog, name='dev', description='The dev subcommand, this is for developer use only!'):
    def __init__(self, bot):
        self.bot = bot


# Adds the module/extension to the main bot
async def setup(bot):
    await bot.add_cog(DEV(bot))