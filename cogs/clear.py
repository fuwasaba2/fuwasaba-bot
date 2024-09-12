import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import configparser

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]


class clear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="clear", description="指定された数のメッセージを削除します。")
    @commands.has_permissions(administrator = True)
    async def clear(self, interaction: discord.ApplicationContext, num: discord.Option(str, required=True, description="削除するメッセージ数を入力")):

        async for message in interaction.channel.history(limit=int(num)):
            await message.delete(delay=1.2)

        embed=discord.Embed(title="メッセージ削除", description=f"{num}メッセージを削除しました。", color=0x4169e1)
        embed.add_field(name="", value="")
        await interaction.respond(embeds=[embed], ephemeral=True)

    @clear.error
    async def clearerror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
        else:
            await ctx.respond("Something went wrong...", ephemeral=True)
        raise error



class cleanup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="cleanup", description="チャンネル内の全メッセージを削除します。※負荷対策で100が上限です。")
    @commands.has_permissions(administrator = True)
    async def cleanup(self, interaction: discord.ApplicationContext):

        async for message in interaction.channel.history(limit=int(100)):
            await message.delete(delay=1.2)

        embed=discord.Embed(title="メッセージ削除", description="メッセージを削除しました。", color=0x4169e1)
        embed.add_field(name="", value="")
        await interaction.respond(embeds=[embed], ephemeral=True)

    @cleanup.error
    async def cleanuperror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
        else:
            await ctx.respond("Something went wrong...", ephemeral=True)
        raise error

def setup(bot):
    bot.add_cog(clear(bot))
    bot.add_cog(cleanup(bot))