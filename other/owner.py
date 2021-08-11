from discord.ext import commands
from helpers import is_owner
from traceback import format_exc

class Owner(commands.Cog):
    def __init__(self, bot):
        global owner_id
        self.bot = bot
        owner_id = self.bot.owner_id
    @commands.command()
    @is_owner()
    async def reload(self, ctx, *, cog: str):
        """Reloads a cog"""
        try:
            self.bot.reload_extension(f"{cog}")
            await ctx.send(f"Successfully reloaded {cog}")
        except Exception as e:
            await ctx.send(f"Error reloading {cog}: ```py\n{format_exc()}```")
    @commands.command()
    @is_owner()
    async def load(self, ctx, *, cog: str):
        """Loads a cog"""
        try:
            self.bot.load_extension(f"{cog}")
            await ctx.send(f"Successfully reloaded {cog}")
        except Exception as e:
            await ctx.send(f"Error loading {cog}: ```py\n{format_exc()}```")
    @commands.command()
    @is_owner()
    async def unload(self, ctx, *, cog: str):
        """Unloads a cog"""
        try:
            self.bot.unload_extension(f"{cog}")
            await ctx.send(f"Successfully unloaded {cog}")
        except Exception as e:
            await ctx.send(f"Error unloading {cog}: ```py\n{format_exc()}```")

def setup(bot):
    bot.add_cog(Owner(bot))