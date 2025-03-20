import discord
from discord import app_commands
from discord.ext import commands
from commands.embed_utils import EmbedUtils

class AutoModCommands:
    def __init__(self, tree: app_commands.CommandTree, client: discord.Client, server_configs: dict):
        self.tree = tree
        self.client = client
        self.server_configs = server_configs
        self.setup_commands()

    def setup_commands(self):
        @self.tree.command(name="automod", description="AutoMod configuration commands")
        @app_commands.checks.has_permissions(manage_guild=True)
        async def automod(interaction: discord.Interaction, action: str, value: str = None):
            guild_id = interaction.guild_id
            
            if action == "setup":
                if guild_id not in self.server_configs:
                    self.server_configs[guild_id] = {}
                
                self.server_configs[guild_id]["automod"] = {
                    "enabled": True,
                    "banned_words": False,
                    "banned_words_list": [],
                    "caps_limit": 70,
                    "mention_limit": 5
                }
                
                await interaction.response.send_message(
                    embed=EmbedUtils.create_config_embed(
                        "🛡️ AutoMod Configuration",
                        "AutoMod has been set up with default settings.",
                        {
                            "Banned Words": "Disabled",
                            "Caps Limit": "70%",
                            "Mention Limit": "5 mentions"
                        }
                    )
                )
            
            elif action == "add_banned_word":
                if guild_id not in self.server_configs or "automod" not in self.server_configs[guild_id]:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_error_embed(
                            "AutoMod Not Set Up",
                            "Please set up AutoMod first using `/automod setup`"
                        ),
                        ephemeral=True
                    )
                    return
                
                if not value:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_error_embed(
                            "Missing Word",
                            "Please provide a word to ban."
                        ),
                        ephemeral=True
                    )
                    return
                
                if value.lower() in self.server_configs[guild_id]["automod"]["banned_words_list"]:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_error_embed(
                            "Word Already Banned",
                            f"The word '{value}' is already in the banned words list."
                        ),
                        ephemeral=True
                    )
                    return
                
                self.server_configs[guild_id]["automod"]["banned_words_list"].append(value.lower())
                self.server_configs[guild_id]["automod"]["banned_words"] = True
                
                await interaction.response.send_message(
                    embed=EmbedUtils.create_success_embed(
                        "Word Added",
                        f"The word '{value}' has been added to the banned words list."
                    )
                )
            
            elif action == "status":
                if guild_id not in self.server_configs or "automod" not in self.server_configs[guild_id]:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_error_embed(
                            "AutoMod Not Set Up",
                            "AutoMod is not configured for this server."
                        ),
                        ephemeral=True
                    )
                    return
                
                automod_config = self.server_configs[guild_id]["automod"]
                banned_words_count = len(automod_config.get("banned_words_list", []))
                
                await interaction.response.send_message(
                    embed=EmbedUtils.create_config_embed(
                        "🛡️ AutoMod Status",
                        "Current AutoMod configuration:",
                        {
                            "Status": "Enabled" if automod_config.get("enabled", False) else "Disabled",
                            "Banned Words": f"{banned_words_count} words" if banned_words_count > 0 else "None",
                            "Caps Limit": f"{automod_config.get('caps_limit', 70)}%",
                            "Mention Limit": f"{automod_config.get('mention_limit', 5)} mentions"
                        }
                    )
                )
            
            else:
                await interaction.response.send_message(
                    embed=EmbedUtils.create_error_embed(
                        "Invalid Action",
                        "Please use 'setup', 'add_banned_word', or 'status' as the action."
                    ),
                    ephemeral=True
                ) 