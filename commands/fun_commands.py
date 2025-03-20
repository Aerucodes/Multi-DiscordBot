import discord
from discord import app_commands
from discord.ext import commands
import random
from commands.embed_utils import EmbedUtils

class FunCommands:
    def __init__(self, tree: app_commands.CommandTree, client: discord.Client):
        self.tree = tree
        self.client = client
        self.setup_commands()

    def setup_commands(self):
        @self.tree.command(name="roll", description="Roll a dice with specified number of sides")
        async def roll(interaction: discord.Interaction, sides: int = 6):
            result = random.randint(1, sides)
            await interaction.response.send_message(
                embed=EmbedUtils.create_game_embed(
                    "🎲 Dice Roll",
                    f"{interaction.user.mention} rolled a {result}!",
                    f"Rolled a {sides}-sided die"
                )
            )

        @self.tree.command(name="8ball", description="Ask the magic 8-ball a question")
        async def eightball(interaction: discord.Interaction, question: str):
            answers = [
                "It is certain.", "It is decidedly so.", "Without a doubt.",
                "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
                "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
                "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                "Cannot predict now.", "Concentrate and ask again.",
                "Don't count on it.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Very doubtful."
            ]
            answer = random.choice(answers)
            await interaction.response.send_message(
                embed=EmbedUtils.create_game_embed(
                    "🎱 Magic 8-Ball",
                    f"Question: {question}\nAnswer: {answer}",
                    f"Asked by {interaction.user.name}"
                )
            )

        @self.tree.command(name="coinflip", description="Flip a coin")
        async def coinflip(interaction: discord.Interaction):
            result = random.choice(["Heads", "Tails"])
            await interaction.response.send_message(
                embed=EmbedUtils.create_game_embed(
                    "🪙 Coin Flip",
                    f"{interaction.user.mention} flipped a coin and got **{result}**!",
                    "Flipped a coin"
                )
            )

        @self.tree.command(name="rps", description="Play Rock, Paper, Scissors with the bot")
        async def rps(interaction: discord.Interaction, choice: str):
            choices = ["rock", "paper", "scissors"]
            if choice.lower() not in choices:
                await interaction.response.send_message(
                    embed=EmbedUtils.create_error_embed(
                        "Invalid Choice",
                        "Please choose rock, paper, or scissors."
                    ),
                    ephemeral=True
                )
                return

            bot_choice = random.choice(choices)
            user_choice = choice.lower()

            # Determine winner
            if user_choice == bot_choice:
                result = "It's a tie!"
            elif (
                (user_choice == "rock" and bot_choice == "scissors") or
                (user_choice == "paper" and bot_choice == "rock") or
                (user_choice == "scissors" and bot_choice == "paper")
            ):
                result = "You win!"
            else:
                result = "I win!"

            await interaction.response.send_message(
                embed=EmbedUtils.create_game_embed(
                    "🪨 Rock, Paper, Scissors",
                    f"{interaction.user.mention} played {user_choice} and I played {bot_choice}.\n**{result}**",
                    f"Played by {interaction.user.name}"
                )
            ) 