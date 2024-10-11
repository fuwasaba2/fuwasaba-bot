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
    async def stop(self, ctx):
        if ctx.author.id == 822458692473323560:
            await ctx.respond("BOTを停止します。", ephemeral=True)
            print("BOTを停止しました。\n------")
            await self.bot.close()
            await asyncio.sleep(1)
            loop = asyncio.get_event_loop()
            loop.stop
        elif ctx.author.id == 827053187919511603:
            await ctx.respond("BOTを停止します。", ephemeral=True)
            print("BOTを停止しました。\n------")
            await self.bot.close()
            await asyncio.sleep(1)
            loop = asyncio.get_event_loop()
            loop.stop
        else:
            await ctx.respond("権限がありません。", ephemeral=True)


def setup(bot):
    bot.add_cog(stop(bot))