import discord
from discord import app_commands
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio

# Import command modules
from commands.basic_commands import BasicCommands
from commands.moderation_commands import ModerationCommands
from commands.fun_commands import FunCommands
from commands.automod_commands import AutoModCommands
from commands.autorole_commands import AutoRoleCommands

# Load environment variables
load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create client
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Store server configurations
server_configs = {}

# Initialize command groups
basic_commands = BasicCommands(tree, client)
moderation_commands = ModerationCommands(tree, client)
fun_commands = FunCommands(tree, client)
automod_commands = AutoModCommands(tree, client, server_configs)
autorole_commands = AutoRoleCommands(tree, client, server_configs)

# Uptime tracking
start_time = None

def format_uptime():
    if not start_time:
        return "0s"
    
    uptime = datetime.utcnow() - start_time
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    seconds = uptime.seconds % 60
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

async def update_presence():
    while True:
        uptime = format_uptime()
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"uptime: {uptime} | /help"
        )
        await client.change_presence(activity=activity)
        await asyncio.sleep(60)  # Update every minute

# Event Handlers
@client.event
async def on_ready():
    global start_time
    start_time = datetime.utcnow()
    
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")
    # Sync slash commands to the Discord server
    await tree.sync()
    print("Slash commands synced")
    
    # Start the presence update task
    client.loop.create_task(update_presence())

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    
    # Check if automod is enabled for this server
    guild_id = message.guild.id if message.guild else None
    if not guild_id or guild_id not in server_configs or "automod" not in server_configs[guild_id]:
        return
    
    automod = server_configs[guild_id]["automod"]
    content = message.content.lower()
    
    # Banned words filter
    if automod.get("banned_words", False) and any(word in content for word in automod.get("banned_words_list", [])):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, your message was removed for containing banned words.")
        return
    
    # Excessive caps check
    if automod.get("caps_limit", 0) > 0:
        caps_count = sum(1 for c in message.content if c.isupper())
        if len(message.content) > 10 and caps_count / len(message.content) * 100 > automod["caps_limit"]:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, your message was removed for excessive caps.")
            return
    
    # Mention limit
    if automod.get("mention_limit", 0) > 0:
        if len(message.mentions) > automod["mention_limit"]:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, your message was removed for too many mentions.")
            return

@client.event
async def on_member_join(member):
    guild_id = member.guild.id
    
    # Check if autorole is enabled
    if guild_id in server_configs and "autorole" in server_configs[guild_id]:
        autorole = server_configs[guild_id]["autorole"]
        if autorole.get("enabled", False):
            try:
                role = member.guild.get_role(autorole["role_id"])
                if role:
                    await member.add_roles(role)
                    print(f"Added role {role.name} to {member.name}")
            except Exception as e:
                print(f"Error adding role to {member.name}: {e}")

# Error handler for app commands
@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
        raise error

# Run the bot with your token
client.run(os.getenv("DISCORD_TOKEN")) 