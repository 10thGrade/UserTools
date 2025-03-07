import discord
from discord import app_commands
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

# 環境変数取得
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = discord.Object(id=os.getenv("GUILD_ID"))
PERMISSION_ROLE = os.getenv("PERMISSION_ROLE")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")

# Bot 初期設定
class UserTools(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)

intents = discord.Intents.default()
intents.message_content = True
# intents.guilds = True  
# intents.guild_messages = True
# intents.members = True  

client = UserTools(intents=intents)

# Bot 起動時処理
@client.event
async def on_ready():
    log_channel = client.get_channel(LOG_CHANNEL_ID)
    jst = timezone(timedelta(hours=9))
    time = datetime.now(jst).strftime("%H:%M:%S")
    await log_channel.send(f"```[{time}] [INFO]: UserTools が起動しました。```")

# Bot メッセージ取得
@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    if msg.content.startswith("$hello"):
        await msg.channel.send("Hello!")

# Bot testコマンド
@client.tree.command()
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello World!")

# Bot addコマンド
@client.tree.command()
@app_commands.describe(
    first_value="the first value",
    second_value="the second value"
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    await interaction.response.send_message(f"{first_value} + {second_value} = {first_value + second_value}")

# Bot 挨拶アプリ
@client.tree.context_menu(name="挨拶")
async def greeting(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"this is {member.name} !!")

# Bot ピン留めアプリ
@client.tree.context_menu(name="ピン留め")
async def pinning(interaction: discord.Interaction, message: discord.Message):
    user_roles = [role.id for role in interaction.user.roles]
    
    if PERMISSION_ROLE not in user_roles:
        await interaction.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)
        return
    if message.pinned:
        await interaction.response.send_message("このメッセージはすでにピン留めされています。", ephemeral=True)
        return
    await message.pin()
    await interaction.response.send_message("メッセージをピン留めしました。", ephemeral=True)
    log_channel = client.get_channel(LOG_CHANNEL_ID)
    if log_channel is None:
        return  # ログチャンネルが見つからない場合は何もしない

    # JST（日本標準時）での時刻を取得
    jst = timezone(timedelta(hours=9))
    pinned_time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")

    # ログメッセージの作成
    log_message = (
        f"📌 **ピン留めが実行されました** 📌\n"
        f"**実行者**: {interaction.user.mention} (`{interaction.user.id}`)\n"
        f"**チャンネル**: {message.channel.mention}\n"
        f"**ピン留めしたメッセージ**: [ジャンプ]({message.jump_url})\n"
        f"**日時**: `{pinned_time}`"
    )

    # ログチャンネルにメッセージを送信
    await log_channel.send(log_message)

client.run(DISCORD_TOKEN)