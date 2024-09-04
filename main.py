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


intents = discord.Intents.default()
intents.message_content = (True)

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
TOKEN = config_ini["MAIN"]["TOKEN"]

bot = discord.Bot(intents=intents)
bot.webhooks = {}
GUILD_IDS = [1235247721934360577]

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



blacklist_file = 'blacklist.json'

def load_blacklist_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_blacklist_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)



class editModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="内容を入力してください。", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):

        embed = discord.Embed(description=f"{self.children[0].value}", color=0xf1c40f)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="", value="")

        message = e_message
        await message.edit(embed=embed)
        await interaction.response.send_message("編集しました。", ephemeral=True)

@bot.message_command(name="edit", guild_ids=GUILD_IDS)
@commands.has_permissions(administrator=True)
async def edit(ctx, message: discord.Message):

    if message.embeds:
        embed = message.embeds[0]

        if embed.footer.text == ctx.user.id:

            global e_message
            e_message = message

            modal = editModal(title="editコマンド")
            await ctx.send_modal(modal)
        else:
            await ctx.respond("他人が送信した埋め込みは編集できません。", ephemeral=True)
    else:
        await ctx.respond("埋め込みがありません。", ephemeral=True)

@edit.error
async def editerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("あなたはこのコマンドを使用する権限を持っていません!", ephemeral=True)
    else:
        await ctx.respond("Something went wrong...", ephemeral=True)
        raise error



user_dict = {}

@bot.slash_command(name="announce", description="メッセージを埋め込みにして送信します。", guild_ids=GUILD_IDS)
@commands.has_permissions(administrator=True)
async def ana_t(ctx):
    user_id = ctx.author.id

    if user_id in user_dict:
        user_dict.pop(user_id)
        await ctx.respond(f"{ctx.author.mention}\nアナウンスモードが終了しました。", ephemeral=True)
    else:
        user_dict[user_id] = ctx.author.name
        await ctx.respond(f"{ctx.author.mention}\nアナウンスモードを起動しました", ephemeral=True)

@bot.event
async def on_message(message: discord.Message):
    user_id = message.author.id

    if user_id in user_dict and not message.author.bot:

        embed = discord.Embed(description=message.content, color=0x9b59b6)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
        embed.set_footer(text=message.author.id)

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
    'ping',
    'userinfo',
    'serverinfo',
    'mcstatus',
    'dm',
    'ban',
    'kick',
    'tasks',
    'blacklist',
    'stop'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


bot.run(TOKEN)