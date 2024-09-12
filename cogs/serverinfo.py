import discord
from discord.ext import commands
import configparser

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]


class serverinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="serverinfo", description="サーバーの情報を表示します。")
    async def serverinfo(self, interaction: discord.ApplicationContext):
        embed = discord.Embed(title="サーバー情報", color=0x4169e1)
        embed.set_author(name=f"{interaction.guild.name}")
        embed.add_field(name="所有者", value=f"{interaction.guild.owner.mention}", inline=False)
        embed.add_field(name="id", value=f"{interaction.guild.id}", inline=False)
        embed.add_field(name="メンバー数", value=f"{interaction.guild.member_count}", inline=False)
        embed.add_field(name="サーバー作成日", value=f"{interaction.guild.created_at}", inline=False)
        embed.add_field(name="オンライン数", value=f"{interaction.guild.approximate_member_count}", inline=False)
        embed.set_thumbnail(url=interaction.guild.icon.replace(static_format='png'))
        embed.set_footer(text=f"{interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)



def setup(bot):
    bot.add_cog(serverinfo(bot))