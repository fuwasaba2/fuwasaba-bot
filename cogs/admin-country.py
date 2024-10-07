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
p_create_c = config_ini["PUBLIC_CHANNEL"]["CREATE_C"]
p_delete_c = config_ini["PUBLIC_CHANNEL"]["DELETE_C"]



#sqlite3
conn = sqlite3.connect('fuwasaba.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS country
             (country TEXT PRIMARY KEY, id TEXT )''')
c.execute('''CREATE TABLE IF NOT EXISTS users
             (country TEXT PRIMARY KEY, id TEXT, image TEXT )''')
c.execute('''CREATE TABLE IF NOT EXISTS deletes
             (country TEXT PRIMARY KEY, id TEXT )''')
c.execute('''CREATE TABLE IF NOT EXISTS peoples
             (id TEXT PRIMARY KEY, country TEXT )''')

conn.commit()



def save_country(country, user_id):
    with conn:
        c.execute("INSERT OR IGNORE INTO country (country, id) VALUES (?, ?)", (country, user_id))
        c.execute("UPDATE country SET id = ? WHERE country = ?", (user_id, country))

def get_country_info(country):
    c.execute("SELECT country, id FROM country WHERE country = ?", (country,))
    return c.fetchone()



def save_user(country, user_id, image_d):
    with conn:
        c.execute("INSERT OR IGNORE INTO users (country, id, image) VALUES (?, ?, ?)", (country, user_id, image_d))
        c.execute("UPDATE users SET id = ?, image = ? WHERE country = ?", (user_id, image_d, country))

def get_user_info(country):
    c.execute("SELECT country, id, image FROM users WHERE country = ?", (country,))
    return c.fetchone()



def save_delete(country, user_id):
    with conn:
        c.execute("INSERT OR IGNORE INTO deletes (country, id) VALUES (?, ?)", (country, user_id))
        c.execute("UPDATE deletes SET id = ? WHERE country = ?", (user_id, country))

def get_delete_info(country):
    c.execute("SELECT country, id FROM deletes WHERE country = ?", (country,))
    return c.fetchone()



def save_people(user_id, country):
    with conn:
        c.execute("INSERT OR IGNORE INTO peoples (id, country) VALUES (?, ?)", (user_id, country))
        c.execute("UPDATE peoples SET country = ? WHERE id = ?", (country, user_id))

def get_people_info(country):
    c.execute("SELECT id, country FROM peoples WHERE id = ?", (country,))
    return c.fetchone()


class admin_country(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    admin = discord.SlashCommandGroup("admin", "admin related commands")

    @admin.command(name="create_apply", description="建国を承認します。", guild_ids=GUILD_IDS)
    @commands.has_any_role(1282384396791320665)
    async def create(self, ctx: discord.ApplicationContext, name: discord.Option(str, description="国名を入力してください。")):

        existing_c = get_user_info(name)

        if existing_c:
            country = str(name)
            user_id = str(existing_c[1])
            save_country(country, user_id)
            save_people(user_id, country)

            ruler_id = str(existing_c[1])

            c.execute(f"""DELETE FROM users WHERE country="{name}";""")
            conn.commit()

            embed = discord.Embed(title="建国", description=f"以下の国家が建国されました。", color=0x38c571)
            embed.add_field(name="国名", value=f"{name}", inline=False)
            embed.add_field(name="国主", value=f"<@!{existing_c[1]}>", inline=False)
            embed.set_image(url=existing_c[2])

            await ctx.respond(embed=embed)
            role = await ctx.guild.create_role(name=name, mentionable=True)

            ruler = await ctx.guild.fetch_member(ruler_id)
            await ruler.add_roles(role)

            channel = await self.bot.fetch_channel(f"{p_create_c}")
            await channel.send(embed=embed)
        else:
            await ctx.respond(f"申請中の国家に指定された国名がありません。", ephemeral=True)

    @admin.command(name="delete_apply", description="国家の解体を承認します。", guild_ids=GUILD_IDS)
    @commands.has_any_role(1282384396791320665)
    async def delete_c(self, ctx: discord.ApplicationContext, name: discord.Option(str, description="国名を入力してください。")):
        name = str(name)

        delete_c = get_delete_info(name)

        if delete_c:
            c.execute(f"""DELETE FROM country WHERE country="{name}";""")
            conn.commit()
            c.execute(f"""DELETE FROM deletes WHERE country="{name}";""")
            conn.commit()

            embed = discord.Embed(title="解体", description="以下の国家が解体されました。")
            embed.add_field(name="国名", value=name, inline=False)

            await ctx.respond(embed=embed)

            channel = await self.bot.fetch_channel(f"{p_delete_c}")
            await channel.send(embed=embed)
        else:
            await ctx.respond("解体申請中の国家に指定された国名がありません。", ephemeral=True)




def setup(bot):
    bot.add_cog(admin_country(bot))