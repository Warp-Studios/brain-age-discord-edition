from discord.ext.commands import Bot
from os import environ
from dotenv import load_dotenv
from discord_slash.client import SlashCommand

load_dotenv()

bot = Bot(command_prefix="Hey Dr. Ryuta ")
slash = SlashCommand(bot)

bot.load_extension("3ds.concentration_training")

bot.run(environ.get("TOKEN"))