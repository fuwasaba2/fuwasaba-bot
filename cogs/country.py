import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import toml
import sqlite3
import configparser
import aiofiles
import os
from discord.ext.pages import Paginator, Page
from discord.utils import get



config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]



#sqlite3
conn = sqlite3.connect('fuwasaba.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS country
             (country TEXT PRIMARY KEY, id TEXT )''')
c.execute('''CREATE TABLE IF NOT EXISTS users
             (country TEXT PRIMARY KEY, id TEXT )''')

conn.commit()



def save_country(country, user_id):
    with conn:
        c.execute("INSERT OR IGNORE INTO country (country, id) VALUES (?, ?)", (country, user_id))
        c.execute("UPDATE country SET id = ? WHERE country = ?", (user_id, country))

def get_country_info(country):
    c.execute("SELECT country, id FROM country WHERE country = ?", (country,))
    return c.fetchone()



def save_user(country, user_id):
    with conn:
        c.execute("INSERT OR IGNORE INTO users (country, id) VALUES (?, ?)", (country, user_id))
        c.execute("UPDATE users SET id = ? WHERE country = ?", (user_id, country))

def get_user_info(country):
    c.execute("SELECT country, id FROM users WHERE country = ?", (country,))
    return c.fetchone()



class country(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    country = discord.SlashCommandGroup("country", "admin related commands")

    @country.command(name="create", description="建国を行います。", guild_ids=GUILD_IDS)
    async def create(self, ctx: discord.ApplicationContext, name: discord.Option(str, required=True, description="a")):

        existing_c = get_country_info(name)
        apply_c = get_user_info(name)

        if existing_c:
            await ctx.respond("すでにこの国名の国家が存在しています。", ephemeral=True)
        else:
            if name != apply_c[0]:
                country = str(name)
                user_id = str(ctx.author.id)
                save_user(country, user_id)

                embed = discord.Embed(title="建国申請", description="建国申請を行いました。", color=0x38c571)
                embed.add_field(name="国名", value=f"{name}", inline=False)
                embed.add_field(name="申請者", value=f"{ctx.author.mention}", inline=False)

                await ctx.respond(embed=embed)
            else:
                await ctx.respond(f"現在申請中の国家と国名が同一です。", ephemeral=True)


    @country.command(name="info", guild_ids=GUILD_IDS)
    async def info(self, ctx:discord.ApplicationContext, name: discord.Option(str)):

        c_name = get_user_info(name)
        await ctx.respond(f"{c_name[1]}", ephemeral=True)



def setup(bot):
    bot.add_cog(country(bot))