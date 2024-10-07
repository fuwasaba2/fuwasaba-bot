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
import re



config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]
a_create_c = config_ini["ADMIN_CHANNEL"]["CREATE_C"]
a_delete_c = config_ini["ADMIN_CHANNEL"]["DELETE_C"]
p_join_c = config_ini["PUBLIC_CHANNEL"]["JOIN_C"]
target_channel_id = config_ini["PUBLIC_CHANNEL"]["JOIN_C"]



#sqlite3
conn = sqlite3.connect('fuwasaba.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS country
             (country TEXT PRIMARY KEY, id TEXT )''')
c.execute('''CREATE TABLE IF NOT EXISTS users
             (country TEXT PRIMARY KEY, id TEXT, image TEXT )''')
c.execute('''CREATE TABLE IF NOT EXISTS deletes
             (country TEXT PRIMARY KEY, id TEXT )''')
c.execute('''CREATE TABLE IF NOT EXISTS joins
             (id TEXT PRIMARY KEY, country TEXT )''')
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



def save_join(user_id, country):
    with conn:
        c.execute("INSERT OR IGNORE INTO joins (id, country) VALUES (?, ?)", (user_id, country))
        c.execute("UPDATE joins SET country = ? WHERE id = ?", (country, user_id))

def get_join_info(country):
    c.execute("SELECT id, country FROM joins WHERE id = ?", (country,))
    return c.fetchone()



def save_people(user_id, country):
    with conn:
        c.execute("INSERT OR IGNORE INTO peoples (id, country) VALUES (?, ?)", (user_id, country))
        c.execute("UPDATE peoples SET country = ? WHERE id = ?", (country, user_id))

def get_people_info(country):
    c.execute("SELECT id, country FROM peoples WHERE id = ?", (country,))
    return c.fetchone()



class country(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    country = discord.SlashCommandGroup("country", "admin related commands")

    @country.command(name="create", description="建国を行います。", guild_ids=GUILD_IDS)
    async def create(self, ctx: discord.ApplicationContext, name: discord.Option(str, description="国名を入力してください。"), image: discord.Attachment):

        user_id = str(ctx.author.id)
        existing_c = get_country_info(name)
        apply_c = get_user_info(name)
        people = get_people_info(user_id)

        if people:
            await ctx.respond("あなたはすでに国家に所属しています。", ephemeral=True)
        else:
            if existing_c:
                await ctx.respond("すでにこの国名の国家が存在しています。", ephemeral=True)
            else:
                if name != apply_c:
                    country = str(name)
                    user_id = str(ctx.author.id)
                    image_d = str(image.url)
                    save_user(country, user_id, image_d)

                    embed = discord.Embed(title="建国申請", description="建国申請が届きました。\n/admin create_applyコマンドで承認できます。", color=0x38c571)
                    embed.add_field(name="国名", value=f"{name}", inline=False)
                    embed.add_field(name="申請者", value=f"{ctx.author.mention}", inline=False)
                    embed.set_image(url=image.url)

                    await ctx.respond("建国を申請しました。", ephemeral=True)

                    apply_channel = await self.bot.fetch_channel(f"{a_create_c}")
                    await apply_channel.send(embed=embed)
                else:
                    await ctx.respond(f"すでに同じ名称の国家が申請されています。", ephemeral=True)

    @country.command(name="delete", description="国家を解体します。", guild_ids=GUILD_IDS)
    async def delete(self, ctx: discord.ApplicationContext, name: discord.Option(str, description="解体する国名を入力してください。")):
        apply_c = get_country_info(name)
        delete_c = get_delete_info(name)

        if delete_c:
            await ctx.respond("すでに解体申請済みです。\n申請を取り消す場合は/reportコマンドで運営に報告してください。", ephemeral=True)
        else:
            if apply_c:
                if str(apply_c[1]) == str(ctx.author.id):
                    country = str(name)
                    user_id = str(ctx.author.id)
                    save_delete(country, user_id)

                    embed = discord.Embed(title="解体申請", description="解体申請が届きました。\n/admin delete_applyコマンドで承認できます。", color=0x38c571)
                    embed.add_field(name="国名", value=name, inline=False)
                    embed.add_field(name="国主", value=ctx.author.mention, inline=False)

                    delete_channel = await self.bot.fetch_channel(f"{a_delete_c}")
                    await delete_channel.send(embed=embed)

                    await ctx.respond("国家の解体を申請しました。", ephemeral=True)
                else:
                    await ctx.respond("解体は国主のみ申請可能です。", ephemeral=True)
            else:
                await ctx.respond("国家が存在しません。", ephemeral=True)

    @country.command(name="join", description="入国申請を行います。", guild_ids=GUILD_IDS)
    async def join(self, ctx: discord.ApplicationContext, name: discord.Option(str, description="国名を入力してください。")):
        user_id = str(ctx.author.id)

        user_info = get_join_info(user_id)
        join_c = get_country_info(name)
        country_r = get_country_info(name)
        people = get_people_info(user_id)

        if people:
            await ctx.respond("あなたはすでに国家に所属しています。", ephemeral=True)
        else:
            if join_c:
                if user_info:
                    await ctx.respond(f"あなたはすでに{user_info[1]}に入国申請を行っています。", ephemeral=True)
                else:
                    user_id = str(ctx.author.id)
                    country = str(name)
                    save_join(user_id, country)

                    embed = discord.Embed(title="入国申請", description="入国申請が届きました。")
                    embed.add_field(name="申請者", value=ctx.author.mention, inline=False)
                    embed.set_author(name=f"{country_r[0]}")
                    embed.set_footer(text=f"{ctx.author.id}")

                    await ctx.respond("入国申請を行いました。", ephemeral=True)

                    View = authView(self.bot)
                    join_channel = await self.bot.fetch_channel(f"{p_join_c}")
                    await join_channel.send(f"<@!{country_r[1]}>", embed=embed, view=View)
            else:
                await ctx.respond("指定した国家は存在しません。", ephemeral=True)




class authView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="承認", custom_id="auth-button-yes", style=discord.ButtonStyle.primary)
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        message = interaction.message
        embed = message.embeds[0]
        country_c = str(embed.author.name)
        appli = str(embed.footer.text)

        c_appli = get_join_info(appli)
        c_ruler = get_country_info(country_c)

        author = str(interaction.user.id)
        if author == c_ruler[1]:

            country = str(country_c)
            user_id = str(appli)
            save_people(user_id, country)

            c.execute(f"""DELETE FROM joins WHERE id="{appli}";""")
            conn.commit()

            embed = discord.Embed(title="所属", description="国家への所属が完了しました。")
            embed.add_field(name="加入者", value=f"<@!{appli}>", inline=False)
            embed.add_field(name="加入先国家", value=f"{country_c}", inline=False)

            await interaction.respond("入国を承認しました。", ephemeral=True)
            await message.delete()

            channel = await self.bot.fetch_channel(f"{target_channel_id}")
            await channel.send(embed=embed)

            role = get(interaction.guild.roles, name=country_c)
            user = await interaction.guild.fetch_member(f"{appli}")
            await user.add_roles(role)
        else:
            await interaction.respond("あなたはこの国の国主ではありません。", ephemeral=True)

    @discord.ui.button(label="拒否", custom_id="auth-button-no", style=discord.ButtonStyle.red)
    async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
        message = interaction.message
        embed = message.embeds[0]
        country_c = str(embed.author.name)
        c_ruler = get_country_info(country_c)
        appli = str(embed.footer.text)

        author = str(interaction.user.id)
        if author == c_ruler[1]:

            c.execute(f"""DELETE FROM joins WHERE id="{appli}";""")
            conn.commit()

            await interaction.respond("入国を拒否しました。", ephemeral=True)

            channel = await self.bot.fetch_channel(target_channel_id)
            await channel.send(f"<@!{appli}>\n入国を拒否されました。")
            await message.delete()
        else:
            await interaction.respond("あなたはこの国の国主ではありません。", ephemeral=True)







def setup(bot):
    bot.add_cog(country(bot))