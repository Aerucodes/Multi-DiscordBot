import discord
from discord import app_commands
from discord.ext import commands
from commands.embed_utils import EmbedUtils

class BasicCommands:
    def __init__(self, tree: app_commands.CommandTree, client: discord.Client):
        self.tree = tree
        self.client = client
        self.setup_commands()

    def setup_commands(self):
        @self.tree.command(name="hello", description="Get a greeting from the bot")
        async def hello(interaction: discord.Interaction):
            await interaction.response.send_message(
                embed=EmbedUtils.create_command_embed(
                    "Greeting",
                    f"Hello {interaction.user.mention}! 👋",
                    discord.Color.blue()
                )
            )

        @self.tree.command(name="ping", description="Check the bot's latency")
        async def ping(interaction: discord.Interaction):
            latency = round(self.client.latency * 1000)
            await interaction.response.send_message(
                embed=EmbedUtils.create_command_embed(
                    "Ping",
                    f"Pong! 🏓",
                    discord.Color.green()
                ).add_field(
                    name="Latency",
                    value=f"{latency}ms",
                    inline=False
                )
            )

        @self.tree.command(name="help", description="Show available commands")
        async def help(interaction: discord.Interaction, command: str = None):
            if command:
                # Show detailed help for specific command
                command_obj = self.tree.get_command(command)
                if command_obj:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_command_help_embed(command_obj)
                    )
                else:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_error_embed(
                            "Command not found",
                            f"The command '{command}' does not exist."
                        ),
                        ephemeral=True
                    )
            else:
                # Show all commands grouped by category
                commands_by_category = {}
                for cmd in self.tree.get_commands():
                    category = cmd.module.split('.')[-1].replace('_commands', '').title()
                    if category not in commands_by_category:
                        commands_by_category[category] = []
                    commands_by_category[category].append(cmd)

                embed = EmbedUtils.create_help_embed()
                for category, cmds in commands_by_category.items():
                    embed.add_field(
                        name=f"{category} Commands",
                        value="\n".join(f"`/{cmd.name}` - {cmd.description}" for cmd in cmds),
                        inline=False
                    )

                await interaction.response.send_message(embed=embed) 