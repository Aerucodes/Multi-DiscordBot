# Discord Bot with Slash Commands

A feature-rich Discord bot with slash commands, moderation tools, fun games, and automated moderation features.

## Features

- Basic Commands (hello, ping, help)
- Moderation Commands (kick, ban, unban, mute, clear)
- Fun Commands (roll, 8ball, coinflip, rps)
- AutoMod Features (banned words, caps limit, mention limit)
- AutoRole System
- Interactive GUI Embeds
- Custom Rich Presence with Uptime

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   ```
4. Run the bot:
   ```bash
   python discord_bot.py
   ```

## Commands

### Basic Commands
- `/hello` - Get a greeting from the bot
- `/ping` - Check the bot's latency
- `/help` - Show available commands

### Moderation Commands
- `/kick` - Kick a member from the server
- `/ban` - Ban a member from the server
- `/unban` - Unban a member from the server
- `/mute` - Mute a member for a specified duration
- `/clear` - Clear a specified number of messages

### Fun Commands
- `/roll` - Roll a dice with specified number of sides
- `/8ball` - Ask the magic 8-ball a question
- `/coinflip` - Flip a coin
- `/rps` - Play Rock, Paper, Scissors with the bot

### AutoMod Commands
- `/automod setup` - Set up AutoMod for the server
- `/automod add_banned_word` - Add a word to the banned words list
- `/automod status` - Check AutoMod configuration

### AutoRole Commands
- `/autorole setup` - Set up auto-role for new members
- `/autorole disable` - Disable auto-role
- `/autorole status` - Check auto-role configuration

## Requirements

- Python 3.8 or higher
- discord.py
- python-dotenv

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Copyright © 2025 Aerucodes. All rights reserved.

## Inviting the Bot

To invite the bot to your server:

1. Go to the OAuth2 > URL Generator section in the [Discord Developer Portal](https://discord.com/developers/applications)
2. Select the "bot" and "applications.commands" scopes
3. Select the permissions your bot needs (at minimum: "Send Messages")
4. Use the generated URL to invite the bot to your server

## Notes

- Slash commands will be registered when the bot starts up
- You need to have the proper permissions to add bots to a server 