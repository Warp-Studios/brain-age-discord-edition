from discord.ext import commands
from discord import Embed
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow

class Menu(commands.Cog):
    """
    The main menu
    """
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def play(self, ctx):
        """
        Opens the menu
        """
        embed=Embed(title="Welcome!", description="Hi, I'm Dr. Ryuta Kawashima, and I study the brain at a top university in Japan. Select an option below to get training!", color=0x80ff00)
        embed.set_author(name="Dr. Ryuta Kawashima", url="https://en.wikipedia.org/wiki/Ryuta_Kawashima", icon_url="https://www.giantbomb.com/a/uploads/scale_medium/0/4362/190766-dr_kawashima.jpg")
        embed.set_footer(text="Brain Age Discord Edition designed by JG#3205")
        buttons = [create_actionrow(*[
            create_button(style=ButtonStyle.blurple, label="Devilish Calculations", custom_id="dc"),
        ])]
        await ctx.send(embed=embed, components=buttons)