import discord
from discord.ext import commands
import configparser

from discord.ui.item import Item

config_ini = configparser.ConfigParser()
config_ini.read("config.ini", encoding="utf-8")
GUILD_IDS = config_ini["MAIN"]["GUILD"]



class dm(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author == self.bot.user:
            return

        if isinstance(message.channel, discord.DMChannel):

            owner = await self.bot.fetch_user(827053187919511603)
            embed = discord.Embed(title="ふわ鯖サポート", description="ここではふわ鯖運営に機能などの提案やルール違反の報告などを行うことが可能です。\n以下のボタンを押すことで対応したサポートを開始します。\n \n1:運営への質問・提案\n2:ルール違反などの通報\n3:BOTの機能提案・バグ報告")
            embed.set_author(name="SUPPORTER かちゅーしゃ", icon_url=owner.avatar.url)
            embed.set_footer(text="ふわ鯖サポート")
            View = dm_button(self.bot)
            await message.channel.send(embed=embed, view=View)



class dm_button(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="1", custom_id="dm-1-button", style=discord.ButtonStyle.primary)
    async def dm1(self, button: discord.ui.Button, interaction):

        owner = await self.bot.fetch_user(827053187919511603)
        embed = discord.Embed(title="運営への質問・提案",
                              description="ここでは運営にサーバーに関する質問や提案を行うことができます。\n下のボタンを押すことで出現するフォームに入力して送信可能です。")
        embed.set_author(name="SUPPORTER かちゅーしゃ", icon_url=owner.avatar.url)

        View = dm_button1(self.bot)
        await interaction.response.send_message(embed=embed, view=View)

    @discord.ui.button(label="2", custom_id="dm-2-button", style=discord.ButtonStyle.primary)
    async def dm2(self, button: discord.ui.Button, interaction):

        owner = await self.bot.fetch_user(827053187919511603)
        embed = discord.Embed(title="ルール違反などの通報",
                              description="ここではルール違反などの通報を行うことができます。\n下のボタンを押すことで出現するフォームに入力して送信可能です。")
        embed.set_author(name="SUPPORTER かちゅーしゃ", icon_url=owner.avatar.url)

        View = dm_button2(self.bot)
        await interaction.response.send_message(embed=embed, view=View)

    @discord.ui.button(label="3", custom_id="dm-3-button", style=discord.ButtonStyle.primary)
    async def dm3(self, button: discord.ui.Button, interaction):

        owner = await self.bot.fetch_user(827053187919511603)
        embed = discord.Embed(title="BOTの機能提案・バグ報告",
                              description="ここではBOT管理者にBOTの機能提案やバグの報告を行うことができます。\n下のボタンを押すことで出現するフォームに入力して送信可能です。")
        embed.set_author(name="SUPPORTER かちゅーしゃ", icon_url=owner.avatar.url)
        View = dm_button3(self.bot)
        await interaction.response.send_message(embed=embed, view=View)


class dm_button1(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="入力", custom_id="dm-1-button-form", style=discord.ButtonStyle.green)
    async def dm1(self, button: discord.ui.Button, interaction):

        modal = button1Modal(self.bot, title="運営への質問・提案")
        await interaction.response.send_modal(modal)

class button1Modal(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot= bot

        self.add_item(discord.ui.InputText(label="内容を入力してください。", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):


        channel = await self.bot.fetch_channel("1294104783057190952")

        embed = discord.Embed(title="質問・提案", description=f"{self.children[0].value}")
        await channel.send(embed=embed)

        owner = await self.bot.fetch_user(827053187919511603)
        embed = discord.Embed(title="送信完了", description=f"以下の内容で送信しました。\n{self.children[0].value}", color=0x00ff00)
        embed.set_author(name="SUPPORTER かちゅーしゃ", icon_url=owner.avatar.url)

        await interaction.response.send_message(embed=embed)



class dm_button2(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="入力", custom_id="dm-2-button-form", style=discord.ButtonStyle.green)
    async def dm1(self, button: discord.ui.Button, interaction):

        modal = button2Modal(self.bot, title="ルール違反などの通報")
        await interaction.response.send_modal(modal)

class button2Modal(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot

        self.add_item(discord.ui.InputText(label="内容を入力してください。", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):


        channel = await self.bot.fetch_channel("1294106617461084180")

        embed = discord.Embed(title="ルール違反などの通報", description=f"{self.children[0].value}")
        await channel.send(embed=embed)

        owner = await self.bot.fetch_user(827053187919511603)
        embed = discord.Embed(title="送信完了", description=f"以下の内容で送信しました。\n{self.children[0].value}", color=0x00ff00)
        embed.set_author(name="SUPPORTER かちゅーしゃ", icon_url=owner.avatar.url)

        await interaction.response.send_message(embed=embed)



class dm_button3(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="入力", custom_id="dm-3-button-form", style=discord.ButtonStyle.green)
    async def dm1(self, button: discord.ui.Button, interaction):

        modal = button1Modal(self.bot, title="BOTのバグ報告・機能提案")
        await interaction.response.send_modal(modal)

class button3Modal(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot

        self.add_item(discord.ui.InputText(label="内容を入力してください。", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):


        channel = await self.bot.fetch_channel("1294106535898910791")

        embed = discord.Embed(title="BOTのバグ報告・機能提案", description=f"{self.children[0].value}")
        await channel.send(embed=embed)

        owner = await self.bot.fetch_user(827053187919511603)
        embed = discord.Embed(title="送信完了", description=f"以下の内容で送信しました。\n{self.children[0].value}", color=0x00ff00)
        embed.set_author(name="SUPPORTER かちゅーしゃ", icon_url=owner.avatar.url)

        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(dm(bot))