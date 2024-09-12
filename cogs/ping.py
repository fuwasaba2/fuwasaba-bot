import discord
from discord.ext import commands
import configparser

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]



class ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="BOTのPingを表示します。")
    async def ping(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="Ping", description="`{0}ms`".format(round(self.bot.latency * 1000, 2)))
        await ctx.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ping(bot))