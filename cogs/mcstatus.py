import discord
from discord.ext import commands
import requests
import configparser

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]

class mcstatus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="mcstatus", description="ふわ鯖のサーバーステータスを確認します。")
    async def mcstatus(self, ctx):
        url = f"https://api.mcstatus.io/v2/status/java/fuwasaba.f5.si"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data['online']:
                embed = discord.Embed(title="Minecraft Server Status", description=f"サーバーアドレス: fuwasaba.f5.si", color=discord.Color.green())
                embed.add_field(name="オンライン", value="Yes", inline=True)
                embed.add_field(name="ホスト", value=data['host'], inline=True)
                embed.add_field(name="バージョン", value=data['version']['name_clean'], inline=True)
                embed.add_field(name="プレイヤー数", value=f"{data['players']['online']} / {data['players']['max']}", inline=True)
                embed.add_field(name="MOTD", value=data['motd']['clean'], inline=False)
            else:
                embed = discord.Embed(title="Minecraft Server Status", description=f"サーバーアドレス: fuwasaba.f5.si", color=discord.Color.red())
                embed.add_field(name="オンライン", value="No", inline=True)

            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.respond(f"サーバー情報の取得に失敗しました: HTTP {response.status_code}", ephemeral=True)



def setup(bot):
    bot.add_cog(mcstatus(bot))