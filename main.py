import discord
import discord.ui
from discord import option
import os
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
from time import sleep
import configparser
import random
import string
from dotenv import load_dotenv
import sqlite3
from datetime import datetime, timedelta, timezone
import asyncio
from discord.ext.pages import Paginator, Page



intents = discord.Intents.default()
intents.message_content = (True)

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
TOKEN = config_ini["MAIN"]["TOKEN"]

bot = discord.Bot(intents=intents)
bot.webhooks = {}
GUILD_IDS = [1282384396757893172]

global result
result = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

#起動通知
@bot.event
async def on_ready():
    os.environ['PASS'] = result
    print(f"Bot名:{bot.user} On ready!!")
    print(os.environ['PASS'])
    print("------")
    channel = await bot.fetch_channel("1235247794114134037")
    pass_channel = await bot.fetch_channel("1251824100515512432")
    await channel.send(f"{bot.user}BOT起動完了")
    await pass_channel.send(f"{result}")

    bot.add_view(authView())

    while True:
        await bot.change_presence(status=discord.Status.online, activity = discord.Activity(name="ふわ鯖", type=discord.ActivityType.playing))
        await asyncio.sleep(15)
        await bot.change_presence(status=discord.Status.online, activity = discord.Activity(name="mod建国サーバー", type=discord.ActivityType.playing))
        await asyncio.sleep(15)
        await bot.change_presence(status=discord.Status.online, activity = discord.Activity(name="Minecraft", type=discord.ActivityType.playing))
        await asyncio.sleep(15)



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

def get_all_mcid():
    c.execute("SELECT id, mcid FROM register")
    return c.fetchall()



@bot.slash_command(name="register", description="MCIDを登録します。", guild_ids=GUILD_IDS)
async def register(ctx:discord.ApplicationContext, id: discord.Option(str, description="mcidを入力してください。")):

    user_id = str(ctx.author.id)
    mcid = str(id)
    save_mcid(user_id, mcid)

    await ctx.respond(f"{id}を登録しました。", ephemeral=True)



user_dict = {}
owner_dict = {}

@bot.slash_command(name="owner", description="メッセージを埋め込みにして送信します。", guild_ids=GUILD_IDS)
@commands.has_any_role(1282384396791320666)
async def ana_t(ctx):
    user_id = ctx.author.id

    if user_id in owner_dict:
        owner_dict.pop(user_id)
        await ctx.respond("アナウンスモードが終了しました。", ephemeral=True)
    else:
        owner_dict[user_id] = ctx.author.name
        await ctx.respond("アナウンスモードを起動しました。", ephemeral=True)



@bot.slash_command(name="admin", description="メッセージを埋め込みにして送信します。", guild_ids=GUILD_IDS)
@commands.has_any_role(1282384396791320665, 1282384396791320664)
async def ana_t(ctx):
    user_id = ctx.author.id

    if user_id in user_dict:
        user_dict.pop(user_id)
        await ctx.respond("アナウンスモードが終了しました。", ephemeral=True)
    else:
        user_dict[user_id] = ctx.author.name
        await ctx.respond("アナウンスモードを起動しました。", ephemeral=True)



@bot.event
async def on_message(message: discord.Message):
    user_id = message.author.id

    if user_id in owner_dict and not message.author.bot:

        embed = discord.Embed(description=message.content, color=0xe91e62)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)

        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith("image/"):
                    embed.set_image(url=attachment.url)
                    break

        mentions = [mention.mention for mention in message.mentions]
        role_mentions = [role.mention for role in message.role_mentions]
        if message.mention_everyone:
            mentions.append("@everyone")
        mention_text = " ".join(mentions + role_mentions)

        if message.reference:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            if mention_text:
                await replied_message.reply(content=mention_text, embed=embed)
                await message.delete()
            else:
                await replied_message.reply(embed=embed)
                await message.delete()

        else:
            if mention_text:
                await message.channel.send(content=mention_text, embed=embed)
                await message.delete()
            else:
                await message.channel.send(embed=embed)
                await message.delete()
    elif user_id in user_dict and not message.author.bot:

        embed = discord.Embed(description=message.content, color=0x9b59b6)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)

        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith("image/"):
                    embed.set_image(url=attachment.url)
                    break

        mentions = [mention.mention for mention in message.mentions]
        role_mentions = [role.mention for role in message.role_mentions]
        if message.mention_everyone:
            mentions.append("@everyone")
        mention_text = " ".join(mentions + role_mentions)

        if message.reference:
            replied_message = await message.channel.fetch_message(message.reference.message_id)

            if mention_text:
                await replied_message.reply(content=mention_text, embed=embed)
                await message.delete()
            else:
                await replied_message.reply(embed=embed)
                await message.delete()

        else:
            if mention_text:
                await message.channel.send(content=mention_text, embed=embed)
                await message.delete()
            else:
                await message.channel.send(embed=embed)
                await message.delete()



class authModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="MCIDを入力してください。", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):

        role = interaction.guild.get_role(1282384396757893175)

        user_id = str(interaction.user.id)
        mcid = str(self.children[0].value)
        save_mcid(user_id, mcid)

        embed = discord.Embed(title="認証成功", description="認証に成功しました。\nふわ鯖へようこそ", color=0x00ff00)

        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.user.add_roles(role)

class authView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="認証", custom_id="auth-button", style=discord.ButtonStyle.primary)
    async def auth(self, button: discord.ui.Button, interaction):

        modal = authModal(title="mcidを入力してください")
        await interaction.response.send_modal(modal)

@bot.slash_command(name="auth", description="認証用パネルを設置します。", guild_ids=GUILD_IDS)
@commands.has_any_role(1282384396791320664, 1282384396791320665)
async def auth(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="認証パネル", description="下のボタンを押して認証を開始してください。")

    View = authView()
    await ctx.respond("認証用パネルを設置しました。", ephemeral=True)
    await ctx.send(embed=embed, view=View)



@bot.slash_command(name="show", description="mcidを表示します。ユーザーを選択しない場合は一覧表示になります。", guild_ids=GUILD_IDS)
async def s_mcid(ctx: discord.ApplicationContext, user: discord.Member = None):


    if user:
        user_id = str(user.id)
        show_mcid = get_mcid_info(user_id)

        if show_mcid:

            embed = discord.Embed(title="MCID検索", color=0x00ff00)
            embed.add_field(name="", value=f"<@!{user_id}>\nmcid: {show_mcid[1]}")

            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.respond("指定したユーザーはregisterを行っていません。", ephemeral=True)
    else:
        mcidlist = get_all_mcid()

        if not mcidlist:
            await ctx.respond("データベースにデータが存在しません。", ephemeral=True)
            return

        embeds = []
        for i in range(0, len(mcidlist), 5):
            embed = discord.Embed(title="MCIDリスト", color=0x00ff00)
            for user_id, mcid in mcidlist[i:i+5]:
                embed.add_field(name="", value=f"<@!{user_id}>\nmcid: {mcid}", inline=False)
            embeds.append(embed)

        paginator = Paginator(pages=embeds, use_default_buttons=True, timeout=60)
        await paginator.respond(ctx.interaction, ephemeral=True)



#削除メッセージ保存
@bot.event
async def on_message_delete(message: discord.Message):

    JST = timezone(timedelta(hours=9))

    channel = message.channel
    author = message.author
    content = message.content
    deleted_time = datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')

    embed = discord.Embed(title="削除されたメッセージ", description=f"{channel.mention}\n```{content}```", color=0xff0000)
    embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)
    embed.set_footer(text=f"削除時刻:{deleted_time}")

    del_c = await bot.fetch_channel(1283669113587105895)
    await del_c.send(embed=embed)



#stop
def stop_py():
    if (bot.is_closed()):
        print("osを切ります。")
        os.system("kill 1")



#cogs登録
cogs_list = [
    'admin-country',
    'clear',
    'country',
    'mcstatus',
    'ping',
    'serverinfo',
    'stop',
    'tasks',
    'userinfo',
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


bot.run(TOKEN)