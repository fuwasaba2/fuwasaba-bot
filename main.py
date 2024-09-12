import discord
import discord.ui
from discord import option
import os
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from time import sleep
import json
import configparser
import random
import string
from dotenv import load_dotenv
import sqlite3


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
                owner_dict.pop(user_id)
            else:
                await replied_message.reply(embed=embed)
                await message.delete()
                owner_dict.pop(user_id)

        else:
            if mention_text:
                await message.channel.send(content=mention_text, embed=embed)
                await message.delete()
                owner_dict.pop(user_id)
            else:
                await message.channel.send(embed=embed)
                await message.delete()
                owner_dict.pop(user_id)
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
                user_dict.pop(user_id)
            else:
                await replied_message.reply(embed=embed)
                await message.delete()
                user_dict.pop(user_id)

        else:
            if mention_text:
                await message.channel.send(content=mention_text, embed=embed)
                await message.delete()
                user_dict.pop(user_id)
            else:
                await message.channel.send(embed=embed)
                await message.delete()
                user_dict.pop(user_id)



#stop
def stop_py():
    if (bot.is_closed()):
        print("osを切ります。")
        os.system("kill 1")



#cogs登録
cogs_list = [
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