import discord
from discord.ext import commands
import json

Debug_guild = [1235247721934360577]

blacklist_file = 'blacklist.json'

def load_data():
    with open(blacklist_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(blacklist_file, 'w') as file:
        json.dump(data, file, indent=4)

class serverinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="serverinfo", description="サーバーの情報を表示します。")
    async def serverinfo(self, interaction: discord.ApplicationContext):
        user_id = str(interaction.author.id)

        data = load_data()

        if user_id not in data:
            embed = discord.Embed(title="サーバー情報", color=0x4169e1)
            embed.set_author(name=f"{interaction.guild.name}")
            embed.add_field(name="所有者", value=f"{interaction.guild.owner.mention}", inline=False)
            embed.add_field(name="id", value=f"{interaction.guild.id}", inline=False)
            embed.add_field(name="メンバー数", value=f"{interaction.guild.member_count}", inline=False)
            embed.add_field(name="サーバー作成日", value=f"{interaction.guild.created_at}", inline=False)
            embed.add_field(name="オンライン数", value=f"{interaction.guild.approximate_member_count}", inline=False)
            embed.set_thumbnail(url=interaction.guild.icon.replace(static_format='png'))
            embed.set_footer(text=f"{interaction.user.display_name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("あなたはブラックリストに登録されています。", ephemeral=True)

def setup(bot):
    bot.add_cog(serverinfo(bot))