import discord
from typing import List, Dict, Any
from datetime import datetime

class EmbedUtils:
    @staticmethod
    def create_command_embed(title: str, description: str, color: discord.Color) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Discord Bot")
        return embed

    @staticmethod
    def create_error_embed(title: str, description: str) -> discord.Embed:
        return EmbedUtils.create_command_embed(title, description, discord.Color.red())

    @staticmethod
    def create_success_embed(title: str, description: str) -> discord.Embed:
        return EmbedUtils.create_command_embed(title, description, discord.Color.green())

    @staticmethod
    def create_help_embed() -> discord.Embed:
        embed = discord.Embed(
            title="📚 Help Menu",
            description="Here are all available commands:",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Use /help <command> for more details")
        return embed

    @staticmethod
    def create_command_help_embed(command: Any) -> discord.Embed:
        embed = discord.Embed(
            title=f"📚 Command Help: /{command.name}",
            description=command.description,
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        if command.parameters:
            embed.add_field(
                name="Parameters",
                value="\n".join(f"• `{param.name}`: {param.description}" for param in command.parameters),
                inline=False
            )
        
        embed.set_footer(text="Discord Bot")
        return embed

    @staticmethod
    def create_game_embed(title: str, description: str, footer: str) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=footer)
        return embed

    @staticmethod
    def create_moderation_embed(title: str, description: str, moderator: discord.User, target: discord.User, reason: str = None) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="Moderator", value=moderator.mention, inline=True)
        embed.add_field(name="Target", value=target.mention, inline=True)
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        
        embed.set_footer(text="Discord Bot")
        return embed

    @staticmethod
    def create_config_embed(title: str, description: str, config: Dict[str, str]) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        for key, value in config.items():
            embed.add_field(name=key, value=value, inline=True)
        
        embed.set_footer(text="Discord Bot")
        return embed 