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



TOML_FILE = 'country.toml'

async def load_country_data():
    if not os.path.exists(TOML_FILE):
        return {}
    async with aiofiles.open(TOML_FILE, 'r', encoding='utf-8') as file:
        contents = await file.read()
        return toml.loads(contents).get('countrys', {})

async def save_country_data(data):
    async with aiofiles.open(TOML_FILE, 'w', encoding='utf-8') as file:
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



#sqlite3
conn = sqlite3.connect('fuwasaba.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (country TEXT PRIMARY KEY, id INTEGER )''')

conn.commit()



def save_user(country, user_id):
    with conn:
        c.execute("INSERT OR IGNORE INTO users (country, id) VALUES (?, ?)", (country, user_id))
        c.execute("UPDATE users SET id = ? WHERE country = ?", (user_id, country))

def get_user_info(country):
    c.execute("SELECT country, id FROM users WHERE country = ?", (country,))
    return c.fetchone()



class permissionView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="承認", custom_id="permission-button", style=discord.ButtonStyle.green)
    async def permission(self, button: discord.ui.Button, interaction: discord.Interaction):

        await save_country_access(country_id, ruler.id, [])
        country = str(country_id)
        user_id = int(ruler.id)
        save_user(country, user_id)

        role = await interaction.guild.create_role(name=country, mentionable=True)
        await ruler.add_roles(role)

        await interaction.response.send_message("建国が承認されました。")

        embed = discord.Embed(title="建国されました", color=0x4169e1)
        embed.add_field(name="国名", value=country_id)
        embed.add_field(name="国主", value=ruler.mention, inline=False)
        embed.set_image(url=flag_url)

        approval_c = await self.bot.fetch_channel("1282384397563068505")
        await approval_c.send(embed=embed)

    @discord.ui.button(label="却下", custom_id="rejection-button", style=discord.ButtonStyle.red)
    async def rejection(self, button: discord.ui.Button, interaction: discord.Interaction):

        await interaction.response.send_message("建国を却下しました。")

        ruler_dm = await self.bot.fetch_user(f"{ruler.id}")
        await ruler_dm.send("建国が却下されました。")



class joinView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="承認", custom_id="join-button", style=discord.ButtonStyle.green)
    async def permission(self, button: discord.ui.Button, interaction: discord.Interaction):

        country_name = get_user_info(join_c)
        if str(country_name[1]) == str(interaction.user.id):
            country_id = str(join_c)
            employee_id = str(join_u.id)

            await add_employee(country_id, employee_id)

            role = get(interaction.guild.roles, name=join_c)
            await join_u.add_roles(role)

            await interaction.response.send_message(f"{join_u.display_name}の国家への加入を承認しました。")

            embed = discord.Embed(title="国家加入", description="以下の内容で国家への加入が行われました。", color=0x4169e1)
            embed.add_field(name="加入者", value=join_u.mention, inline=False)
            embed.add_field(name="加入先", value=join_c, inline=False)

            approval_c = await self.bot.fetch_channel("1282384397563068506")
            await approval_c.send(embed=embed)
        else:
            await interaction.response.send_message("あなたは国主ではありません。", ephemeral=True)

    @discord.ui.button(label="却下", custom_id="kick-button", style=discord.ButtonStyle.red)
    async def rejection(self, button: discord.ui.Button, interaction: discord.Interaction):

        country_name = get_user_info(join_c)
        if str(country_name[1]) == str(interaction.user.id):

            await interaction.response.send_message("加入を却下しました。")

            applicant_dm = await self.bot.fetch_user(f"{join_u.id}")
            await applicant_dm.send("加入が却下されました。")
        else:
            await interaction.response.send_message("あなたは国主ではありません。", ephemeral=True)



class deleteView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="承認", custom_id="d-permission-button", style=discord.ButtonStyle.green)
    async def permission(self, button: discord.ui.Button, interaction: discord.Interaction):

        country_info2 = get_user_info(country_info)

        country_id2 = str(country_info)
        if country_info2:
            c.execute(f"""DELETE FROM users WHERE id="{country_info}";""")
            conn.commit()

            countrys = await load_country_data()
            if country_id2 in countrys:
                del countrys[country_id2]
                await save_country_data(countrys)

        await interaction.response.send_message("解体が承認されました。")

        embed = discord.Embed(title="解体されました", color=0x4169e1)
        embed.add_field(name="国名", value=country_id2)
        embed.add_field(name="国主", value=country_r.mention, inline=False)

        approval_c = await self.bot.fetch_channel("1282384397563068505")
        await approval_c.send(embed=embed)

    @discord.ui.button(label="却下", custom_id="d-rejection-button", style=discord.ButtonStyle.red)
    async def rejection(self, button: discord.ui.Button, interaction: discord.Interaction):

        await interaction.response.send_message("解体を却下しました。")

        ruler_dm = await self.bot.fetch_user(f"{ruler.id}")
        await ruler_dm.send("解体が却下されました。")



class country(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    country = SlashCommandGroup("country", "countryグループ")

    @country.command(name='create', description="建国を行います。", guild_ids=GUILD_IDS)
    async def all(self, interaction: discord.ApplicationContext, name: discord.Option(str, description="国名を入力してください。"), flag: discord.Attachment):

        country_name = get_user_info(name)
        if country_name:
            await interaction.response.send_message("その国名を持つ国がすでに存在しています。", ephemeral=True)
        else:
            embed = discord.Embed(title="建国申請", color=0x4169e1)
            embed.add_field(name="国名", value=name, inline=False)
            embed.add_field(name="国主", value=interaction.author.mention, inline=False)
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
            await ctx.respond("No countrys found.", ephemeral=True)
            return

        country_pages = []
        embed = discord.Embed(title="国家リスト", color=0x00ff00)
        count = 0

        for country_id, details in countrys.items():
            embed.add_field(name=country_id, value=f"国主: <@{details['Ruler']}>", inline=False)
            count += 1

            if count % 5 == 0 or count == len(countrys):
                country_pages.append(Page(embeds=[embed]))
                embed = discord.Embed(title="国家リスト", color=0x00ff00)

        paginator = Paginator(pages=country_pages)
        await paginator.respond(ctx.interaction, ephemeral=True)



    @country.command(name="request", description="指定した国家に加入申請を行います。", guild_ids=GUILD_IDS)
    async def request(self, ctx: discord.ApplicationContext, name: discord.Option(str, description="加入したい国家の名称を入力してください。")):

        global join_c, join_u, ruler_id
        join_c = name
        join_u = ctx.author

        ruler_id = get_user_info(name)

        embed = discord.Embed(title="国家加入申請", description="以下の内容で入国申請が届きました。")
        embed.add_field(name="入国希望者", value=ctx.author.mention, inline=False)
        embed.add_field(name="国主", value=f"<@!{ruler_id[1]}>")
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        View = joinView(self.bot)
        ruler_dm = await self.bot.fetch_channel(1282384397563068506)
        await ruler_dm.send(embed=embed, view=View)

        await ctx.respond(f"{name}への加入申請を行いました。\n国主が承認するまでお待ちください。\n \nなお、承認及び不承認の際にはBOTからのDMが届きます。\n必ずBOTからメッセージを受信できるようにしてください。")



    @country.command(name='delete', description="国家の解体を行います。", guild_ids=GUILD_IDS)
    async def all(self, interaction: discord.ApplicationContext, name: discord.Option(str, description="国名を入力してください。")):

        global country_info, country_r

        country_info = str(name)

        country_r = interaction.author

        c_name = get_user_info(name)

        if str(c_name[1]) == str(country_r.id):

            embed = discord.Embed(title="解体申請", description="以下の内容で国家の解体申請を受け付けました。", color=0x4169e1)
            embed.add_field(name="国名", value=name, inline=False)
            embed.add_field(name="国主", value=interaction.author.mention, inline=False)

            ruler = interaction.author

            await interaction.respond(embed=embed, ephemeral=True)

            View = deleteView(self.bot)
            request_c = await self.bot.fetch_channel("1283638915453947985")
            await request_c.send(embed=embed, view=View)
        else:
            await interaction.response.send_message("あなたは国主ではありません。", ephemeral=True)


def setup(bot):
    bot.add_cog(country(bot))