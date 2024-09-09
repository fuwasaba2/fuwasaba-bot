import discord
from discord.ext import commands
from discord import Option
from discord.ext.commands import MissingAnyRole
import json

Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

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