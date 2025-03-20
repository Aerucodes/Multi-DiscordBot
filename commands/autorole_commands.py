import discord
from discord import app_commands
from discord.ext import commands
from commands.embed_utils import EmbedUtils

class AutoRoleCommands:
    def __init__(self, tree: app_commands.CommandTree, client: discord.Client, server_configs: dict):
        self.tree = tree
        self.client = client
        self.server_configs = server_configs
        self.setup_commands()

    def setup_commands(self):
        @self.tree.command(name="autorole", description="AutoRole configuration commands")
        @app_commands.checks.has_permissions(manage_guild=True)
        async def autorole(interaction: discord.Interaction, action: str, role: discord.Role = None):
            guild_id = interaction.guild_id
            
            if action == "setup":
                if not role:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_error_embed(
                            "Missing Role",
                            "Please specify a role to assign to new members."
                        ),
                        ephemeral=True
                    )
                    return
                
                if guild_id not in self.server_configs:
                    self.server_configs[guild_id] = {}
                
                self.server_configs[guild_id]["autorole"] = {
                    "enabled": True,
                    "role_id": role.id
                }
                
                await interaction.response.send_message(
                    embed=EmbedUtils.create_config_embed(
                        "👥 AutoRole Configuration",
                        "AutoRole has been set up successfully.",
                        {
                            "Role": role.name,
                            "Status": "Enabled"
                        }
                    )
                )
            
            elif action == "disable":
                if guild_id not in self.server_configs or "autorole" not in self.server_configs[guild_id]:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_error_embed(
                            "AutoRole Not Set Up",
                            "AutoRole is not configured for this server."
                        ),
                        ephemeral=True
                    )
                    return
                
                self.server_configs[guild_id]["autorole"]["enabled"] = False
                
                await interaction.response.send_message(
                    embed=EmbedUtils.create_success_embed(
                        "AutoRole Disabled",
                        "AutoRole has been disabled. New members will no longer receive the role automatically."
                    )
                )
            
            elif action == "status":
                if guild_id not in self.server_configs or "autorole" not in self.server_configs[guild_id]:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_error_embed(
                            "AutoRole Not Set Up",
                            "AutoRole is not configured for this server."
                        ),
                        ephemeral=True
                    )
                    return
                
                autorole_config = self.server_configs[guild_id]["autorole"]
                role = interaction.guild.get_role(autorole_config["role_id"])
                
                if not role:
                    await interaction.response.send_message(
                        embed=EmbedUtils.create_error_embed(
                            "Role Not Found",
                            "The configured role no longer exists."
                        ),
                        ephemeral=True
                    )
                    return
                
                await interaction.response.send_message(
                    embed=EmbedUtils.create_config_embed(
                        "👥 AutoRole Status",
                        "Current AutoRole configuration:",
                        {
                            "Role": role.name,
                            "Status": "Enabled" if autorole_config.get("enabled", False) else "Disabled"
                        }
                    )
                )
            
            else:
                await interaction.response.send_message(
                    embed=EmbedUtils.create_error_embed(
                        "Invalid Action",
                        "Please use 'setup', 'disable', or 'status' as the action."
                    ),
                    ephemeral=True
                ) 