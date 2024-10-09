import discord
from discord.ext import commands
import sqlite3
import configparser

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]



#sqlite3
conn = sqlite3.connect('fuwasaba.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS register
             (id TEXT PRIMARY KEY, mcid TEXT )''')

conn.commit()



def save_mcid(user_id, mcid):
    with conn:
        c.execute("INSERT OR IGNORE INTO register (id, mcid) VALUES (?, ?)", (user_id, mcid))
        c.execute("UPDATE register SET mcid = ? WHERE id = ?", (mcid, user_id))

def get_mcid_info(user_id):
    c.execute("SELECT id, mcid FROM register WHERE id = ?", (user_id,))
    return c.fetchone()



class userinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="userinfo", description="ユーザー情報を取得します。")
    async def userinfo(self, ctx, user:discord.Member):
        user_id = str(user.id)
        mcid = get_mcid_info(user_id)

        try:
            embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
            embed.set_thumbnail(url=user.avatar.url)
        except:
            pass
        embed.add_field(name="表示名", value=user.display_name,inline=True)
        embed.add_field(name="ユーザーID", value=user.id,inline=True)
        embed.add_field(name="メンション", value=user.mention, inline=True)
        embed.add_field(name="アカウント作成日", value=user.created_at)
        embed.add_field(name="MCID", value=mcid[1], inline=False)
        embed.set_footer(text="Userinfoサービス")
        await ctx.respond(embed=embed, ephemeral=True)

class userinfo_c(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.user_command(name="userinfo")
    async def userinfo_c(self, ctx, user: discord.Member):

        user_id = str(user.id)
        mcid = get_mcid_info(user_id)

        try:
            embed = discord.Embed(title="User Info", description=f" <@!{user}>", color=0x4169e1)
            embed.set_thumbnail(url=user.avatar.url)
        except:
            pass
        embed.add_field(name="表示名", value=user.display_name,inline=True)
        embed.add_field(name="ユーザーID", value=user.id,inline=True)
        embed.add_field(name="メンション", value=user.mention, inline=True)
        embed.add_field(name="アカウント作成日", value=user.created_at, inline=True)
        embed.add_field(name="MCID", value=mcid[1], inline=True)
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(userinfo(bot))
    bot.add_cog(userinfo_c(bot))