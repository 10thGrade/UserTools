import discord
from discord import app_commands
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

# 環境変数取得
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = discord.Object(id=os.getenv("GUILD_ID"))
PERMISSION_ROLE = list(map(int, os.getenv("PERMISSION_ROLE", "").split(",")))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

jst = timezone(timedelta(hours=9))

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
    time = datetime.now(jst).strftime("%H:%M:%S")
    log_message = (f"```[{time}] [INFO]: UserTools が起動しました。```")
    await log_channel.send(log_message)

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
    await interaction.response.send_message(f"Hello World!", ephemeral=True)
    log_channel = client.get_channel(LOG_CHANNEL_ID)
    time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
    log_message = (f"```[{time}] [INFO]: {interaction.user.name} issued command: test```\n")
    await log_channel.send(log_message)

# Bot whoisアプリ
@client.tree.context_menu(name="Whois")
async def whois(interaction: discord.Interaction, member: discord.Member):
    
    user_roles = [role.id for role in interaction.user.roles]
    log_channel = client.get_channel(LOG_CHANNEL_ID)
    time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
    log_message = (f"```[{time}] [INFO]: {interaction.user.name} issued app command: Whois```\n")
    await log_channel.send(log_message)
    
    if not any(role_id in user_roles for role_id in PERMISSION_ROLE):
        await interaction.response.send_message(">>> このコマンドを実行する権限がありません。", ephemeral=True)
        time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
        log_message = (f"```[{time}] [ERROR]: {interaction.user.name} does not have permission to use this command.```")
        await log_channel.send(log_message)
        return
    
    whois_message = (
        f"------------| User whois |------------\n"
        f"  User: {member.name}\n"
        f"  Nick: {member.display_name}\n"
        f"  ID: {member.id}\n"
        f"  Status: {member.desktop_status}\n"
        f"  Account: {member.created_at}\n"
        f"  Avatar: {member.avatar}\n"
        f"-------------------------------------"
    )
    await interaction.response.send_message(">>> コマンドを実行しました。", ephemeral=True)
    await log_channel.send(whois_message)

# Bot ピン留めアプリ
@client.tree.context_menu(name="Pinning")
async def pinning(interaction: discord.Interaction, message: discord.Message):
    log_channel = client.get_channel(LOG_CHANNEL_ID)
    time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
    log_message = (f"```[{time}] [INFO]: {interaction.user.name} issued app command: Pinning```\n")
    await log_channel.send(log_message)
    
    if message.pinned:
        await message.unpin()
        await interaction.response.send_message(">>> メッセージのピン留めを解除しました。", ephemeral=True)
        time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
        log_message = (f"```[{time}] [INFO]: {interaction.user.name} unpinned the message.```")
        await log_channel.send(log_message)
        return
    
    await message.pin()
    await interaction.response.send_message(">>> メッセージをピン留めしました。", ephemeral=True)
    time = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S")
    log_message = (f"```[{time}] [INFO]: {interaction.user.name} pinned the message.```")
    await log_channel.send(log_message)

client.run(DISCORD_TOKEN)