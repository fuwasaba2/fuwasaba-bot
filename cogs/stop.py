import discord
from discord.ext import commands
import os
from time import sleep
from discord.ext import tasks
import asyncio
import configparser

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]


class stop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="stop", description="BOTを停止します。")
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.respond("BOTを停止します。", ephemeral=True)
        print("BOTを停止しました。\n------")
        await self.bot.close()
        await asyncio.sleep(1)
        loop = asyncio.get_event_loop()
        loop.stop


def setup(bot):
    bot.add_cog(stop(bot))