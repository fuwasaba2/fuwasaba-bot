import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import psutil
import datetime

Debug_guild = [1235247721934360577]

class tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    tasks = SlashCommandGroup("task", "タスクグループ")

    @tasks.command(name='all', description="サーバーの使用状況を確認します。")
    async def all(self, interaction: discord.ApplicationContext):

        time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

        embed = discord.Embed(title="サーバー状況", description="サーバーの状態を表示しています。", color=0x4169e1)
        embed.add_field(name="CPU使用率", value=f"{psutil.cpu_percent(interval=1)}％", inline=False)
        embed.add_field(name="メモリ使用率", value=f"{psutil.virtual_memory().percent}％", inline=False)
        embed.add_field(name="ストレージ使用率", value=f"{psutil.disk_usage('/').percent}％", inline=False)
        embed.add_field(name="サーバー起動時刻", value=f"{time}", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tasks.command(name="cpu", description="CPUの使用状況を確認します。")
    async def cpu(self, interaction: discord.ApplicationContext):

        time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

        embed = discord.Embed(title="CPU使用状況", description="CPUの使用状況を表示します。", color=0x4169e1)
        embed.add_field(name="CPU使用率", value=f"{psutil.cpu_percent(interval=1)}％", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


    @tasks.command(name="ram", description="メモリの使用状況を確認します。")
    async def ram(self, interaction: discord.ApplicationContext):

        time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

        embed = discord.Embed(title="メモリ使用状況", description="メモリの使用状況を表示しています。", color=0x4169e1)
        embed.add_field(name="メモリ使用率", value=f"{psutil.virtual_memory().percent}％", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tasks.command(name="rom", description="ストレージの使用状況を確認します。")
    async def rom(self, interaction: discord.ApplicationContext):

        time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

        embed = discord.Embed(title="ストレージ使用状況", description="ストレージの使用状況を表示しています。", color=0x4169e1)
        embed.add_field(name="ストレージ使用率", value=f"{psutil.disk_usage('/').percent}％", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tasks.command(name="time", description="サーバーの起動時刻を確認します。")
    async def time(self, interaction: discord.ApplicationContext):

        time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

        embed = discord.Embed(title="サーバー起動時刻", description="サーバーの起動時刻を表示しています。", color=0x4169e1)
        embed.add_field(name="サーバー起動時刻", value=f"{time}", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(tasks(bot))