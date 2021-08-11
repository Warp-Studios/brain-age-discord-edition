from dotenv import load_dotenv
from os import environ
from discord.ext.commands import check 
from discord.ext.commands.errors import NotOwner

load_dotenv()

def is_owner():
    async def predicate(ctx):
        if not ctx.author.id == ctx.bot.owner_id and not ctx.author.id == int(environ.get('OWNER_ID')):
            raise NotOwner("You do not own this bot.")
        else:
            return True
    return check(predicate)