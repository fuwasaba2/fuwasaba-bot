import discord
from discord.ext import commands
from discord import Option
from discord.ext.commands import MissingPermissions
import json

Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

class ban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ban", description="指定したユーザーをサーバーからBANします。")
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member: Option(discord.Member, description = "BANするユーザーを選択"), reason: Option(str, description = "BAN理由を入力(ログに記載されます。)", required = False)):
        user_id = str(ctx.author.id)

        data = load_data()

        if user_id not in data:
            if member.id == ctx.author.id:
                await ctx.respond("自分自身をBANすることはできません。", ephemeral=True)
            elif member.guild_permissions.administrator:
                await ctx.respond("このコマンドは管理者のみ実行できます。", ephemeral=True)
            else:
                if reason == None:
                    reason = f"BAN理由:{ctx.author}"
                await member.ban(reason = reason)
                await ctx.respond(f"<@{member.id}> がサーバーからBANされました。\n\nBAN理由: {reason}", ephemeral=True)
        else:
            await ctx.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

    @ban.error
    async def banerror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
        else:
            await ctx.respond("Something went wrong...", ephemeral=True)
            raise error

def setup(bot):
    bot.add_cog(ban(bot))