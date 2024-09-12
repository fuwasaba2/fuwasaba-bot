import discord
from discord.ext import commands
from discord import Option
from discord.ext.commands import MissingAnyRole
import configparser

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]


class kick(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="kick", description="指定したユーザーをサーバーからキックします。")
    @commands.has_any_role(1282384396791320664, 1282384396791320665)
    async def kick(self, ctx, member: Option(discord.Member, description = "キックするユーザーを選択"), reason: Option(str, description = "キック理由を入力(ログに記載されます。)", required = False)):

        if member.id == ctx.author.id:
            await ctx.respond("自分自身をkickすることはできません。", ephemeral=True)
        elif member.guild_permissions.administrator:
            await ctx.respond("このコマンドは運営のみ実行できます。", ephemeral=True)
        else:
            if reason == None:
                reason = f"kick理由:{ctx.author}"
            await ctx.respond(f"{member.mention}がサーバーからキックされました。\n\nキック理由: {reason}", ephemeral=True)
            await member.kick(reason = reason)

    @kick.error
    async def banerror(ctx, error):
        if isinstance(error, MissingAnyRole):
            await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
        else:
            await ctx.respond("Something went wrong...", ephemeral=True)
            raise error



def setup(bot):
    bot.add_cog(kick(bot))