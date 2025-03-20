import discord
from discord import app_commands
from discord.ext import commands
from commands.embed_utils import EmbedUtils

class ModerationCommands:
    def __init__(self, tree: app_commands.CommandTree, client: discord.Client):
        self.tree = tree
        self.client = client
        self.setup_commands()

    def setup_commands(self):
        @self.tree.command(name="kick", description="Kick a member from the server")
        @app_commands.checks.has_permissions(kick_members=True)
        async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
            if member.top_role >= interaction.user.top_role:
                await interaction.response.send_message(
                    embed=EmbedUtils.create_error_embed(
                        "Permission Error",
                        "You cannot kick someone with a higher or equal role."
                    ),
                    ephemeral=True
                )
                return

            await member.kick(reason=reason)
            await interaction.response.send_message(
                embed=EmbedUtils.create_moderation_embed(
                    "Member Kicked",
                    f"{member.mention} has been kicked.",
                    interaction.user,
                    member,
                    reason
                )
            )

        @self.tree.command(name="ban", description="Ban a member from the server")
        @app_commands.checks.has_permissions(ban_members=True)
        async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None, delete_messages: int = 0):
            if member.top_role >= interaction.user.top_role:
                await interaction.response.send_message(
                    embed=EmbedUtils.create_error_embed(
                        "Permission Error",
                        "You cannot ban someone with a higher or equal role."
                    ),
                    ephemeral=True
                )
                return

            await member.ban(reason=reason, delete_message_days=delete_messages)
            await interaction.response.send_message(
                embed=EmbedUtils.create_moderation_embed(
                    "Member Banned",
                    f"{member.mention} has been banned.",
                    interaction.user,
                    member,
                    reason
                ).add_field(
                    name="Messages Deleted",
                    value=f"{delete_messages} days",
                    inline=False
                )
            )

        @self.tree.command(name="unban", description="Unban a member from the server")
        @app_commands.checks.has_permissions(ban_members=True)
        async def unban(interaction: discord.Interaction, user_id: str):
            try:
                user_id = int(user_id)
                user = await self.client.fetch_user(user_id)
                await interaction.guild.unban(user)
                await interaction.response.send_message(
                    embed=EmbedUtils.create_success_embed(
                        "Member Unbanned",
                        f"{user.mention} has been unbanned."
                    )
                )
            except ValueError:
                await interaction.response.send_message(
                    embed=EmbedUtils.create_error_embed(
                        "Invalid User ID",
                        "Please provide a valid user ID."
                    ),
                    ephemeral=True
                )

        @self.tree.command(name="mute", description="Mute a member for a specified duration")
        @app_commands.checks.has_permissions(moderate_members=True)
        async def mute(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = None):
            if member.top_role >= interaction.user.top_role:
                await interaction.response.send_message(
                    embed=EmbedUtils.create_error_embed(
                        "Permission Error",
                        "You cannot mute someone with a higher or equal role."
                    ),
                    ephemeral=True
                )
                return

            await member.timeout(duration=duration, reason=reason)
            await interaction.response.send_message(
                embed=EmbedUtils.create_moderation_embed(
                    "Member Muted",
                    f"{member.mention} has been muted.",
                    interaction.user,
                    member,
                    reason
                ).add_field(
                    name="Duration",
                    value=f"{duration} seconds",
                    inline=False
                )
            )

        @self.tree.command(name="clear", description="Clear a specified number of messages")
        @app_commands.checks.has_permissions(manage_messages=True)
        async def clear(interaction: discord.Interaction, amount: int):
            if amount < 1 or amount > 100:
                await interaction.response.send_message(
                    embed=EmbedUtils.create_error_embed(
                        "Invalid Amount",
                        "Please specify a number between 1 and 100."
                    ),
                    ephemeral=True
                )
                return

            await interaction.response.defer()
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(
                embed=EmbedUtils.create_success_embed(
                    "Messages Cleared",
                    f"Successfully deleted {len(deleted)} messages."
                )
            ) 