import discord
from discord.ext import commands
import json

Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

class userinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="userinfo", description="ユーザー情報を取得します。")
    async def userinfo(self, ctx, user:discord.Member):
        user_id = str(ctx.author.id)

        data = load_data()
        if user_id not in data:
            try:
                embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
                embed.set_thumbnail(url=user.avatar.url)
            except:
                pass
            embed.add_field(name="表示名", value=user.display_name,inline=True)
            embed.add_field(name="ユーザーID", value=user.id,inline=True)
            embed.add_field(name="メンション", value=user.mention, inline=True)
            embed.add_field(name="アカウント作成日", value=user.created_at)
            embed.set_footer(text="Userinfoサービス")
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

class userinfo_c(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.user_command(name="userinfo")
    async def userinfo_c(self, ctx, user: discord.Member):
        user_id = str(ctx.author.id)

        data = load_data()

        if user_id not in data:
            try:
                embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
                embed.set_thumbnail(url=user.avatar.url)
            except:
                pass
            embed.add_field(name="表示名", value=user.display_name,inline=True)
            embed.add_field(name="ユーザーID", value=user.id,inline=True)
            embed.add_field(name="メンション", value=user.mention, inline=True)
            embed.add_field(name="アカウント作成日", value=user.created_at)
            embed.set_footer(text="Userinfoサービス")
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

def setup(bot):
    bot.add_cog(userinfo(bot))
    bot.add_cog(userinfo_c(bot))