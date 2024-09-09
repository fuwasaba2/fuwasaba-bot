import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.ext.commands import MissingAnyRole
import json
import toml
import sqlite3
import configparser
import aiofiles
import os
from discord.ext.pages import Paginator, Page



config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]



TOML_FILE = 'country.toml'

async def load_country_data():
    if not os.path.exists(TOML_FILE):
        return {}
    async with aiofiles.open(TOML_FILE, 'r') as file:
        contents = await file.read()
        return toml.loads(contents).get('countrys', {})

async def save_country_data(data):
    async with aiofiles.open(TOML_FILE, 'w') as file:
        await file.write(toml.dumps({'countrys': data}))

async def save_country_access(country_id, Ruler, employees):
    countrys = await load_country_data()
    countrys[country_id] = {'Ruler': Ruler, 'employees': employees}
    await save_country_data(countrys)

async def get_country_access(country_id):
    countrys = await load_country_data()
    return countrys.get(country_id)

async def add_employee(country_id, employee_id):
    countrys = await load_country_data()
    if country_id in countrys:
        if 'employees' not in countrys[country_id]:
            countrys[country_id]['employees'] = []
        countrys[country_id]['employees'].append(employee_id)
        await save_country_data(countrys)
        return True
    return False

async def is_authorized_user(user_id, country_id):
    country_access = await get_country_access(country_id)
    if country_access:
        return user_id == country_access['Ruler'] or user_id in country_access['employees']
    return False



class permissionView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="承認", custom_id="permission-button", style=discord.ButtonStyle.green)
    async def permission(self, button: discord.ui.Button, interaction: discord.Interaction):

        await save_country_access(country_id, ruler.id, [])

        await interaction.response.send_message("建国が承認されました。")

        embed = discord.Embed(title="建国されました", color=0x4169e1)
        embed.add_field(name="国主", value=ruler.mention, inline=False)
        embed.set_image(url=flag_url)

        approval_c = await self.bot.fetch_channel("1282384397563068505")
        await approval_c.send(embed=embed)

    @discord.ui.button(label="却下", custom_id="rejection-button", style=discord.ButtonStyle.red)
    async def rejection(self, button: discord.ui.Button, interaction: discord.Interaction):

        await interaction.response.send_message("建国を却下しました。")

        ruler_dm = await self.bot.fetch_user(f"{ruler.id}")
        await ruler_dm.send("建国が却下されました。")



class country(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    country = SlashCommandGroup("country", "countryグループ")

    @country.command(name='create', description="建国を行います。", guild_ids=GUILD_IDS)
    async def all(self, interaction: discord.ApplicationContext, name: discord.Option(str, description="国名を入力してください。"), flag: discord.Attachment):

        embed = discord.Embed(title="建国申請", color=0x4169e1)
        embed.add_field(name="国名", value=name, inline=False)
        embed.set_image(url=flag.url)

        global ruler, country_id, flag_url
        ruler = interaction.author
        country_id = str(name)
        flag_url = flag.url

        await interaction.respond(embed=embed, ephemeral=True)

        View = permissionView(self.bot)
        request_c = await self.bot.fetch_channel("1282716891378356225")
        await request_c.send(embed=embed, view=View)



    @country.command(name="list", description="国家を一覧表示します。", guild_ids=GUILD_IDS)
    async def list(self, ctx: discord.ApplicationContext):
        countrys = await load_country_data()
        if not countrys:
            await ctx.send("No countrys found.")
            return

        country_pages = []
        embed = discord.Embed(title="国家リスト", color=0x00ff00)
        count = 0

        for country_id, details in countrys.items():
            embed.add_field(name=country_id, value=f"国主: <@{details['Ruler']}>", inline=False)
            count += 1

            # 5社ごとにページを作成
            if count % 5 == 0 or count == len(countrys):
                country_pages.append(Page(embeds=[embed]))
                embed = discord.Embed(title="国家リスト", color=0x00ff00)  # 新しい埋め込みを作成

        paginator = Paginator(pages=country_pages)
        await paginator.respond(ctx.interaction, ephemeral=True)



def setup(bot):
    bot.add_cog(country(bot))