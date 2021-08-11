'''
Platform: 3DS
Title: Brain Age: Concentration Training
'''

from discord.ext import commands
from discord import Embed
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from random import randint
from asyncio import sleep
from copy import deepcopy

class ConcentrationTraining(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

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
    @commands.Cog.listener()
    async def on_component(self, ctx):
        await ctx.defer()
        if ctx.custom_id == "dc":
            await ctx.send("Alright, let's go!", hidden=False)
            self.games[ctx.origin_message.guild.id] = {"game": "dc", "current_no1": randint(1, 10), "current_no2": randint(1, 10), "mistakes": 0, "answered": 0}
            to_edit = await ctx.send(f"{self.games[ctx.origin_message.guild.id]['current_no1']}+{self.games[ctx.origin_message.guild.id]['current_no2']}=?")
            self.games[ctx.origin_message.guild.id]["to_edit"] = to_edit
            await sleep(10)
            self.games[ctx.origin_message.guild.id]["last_no1"] = deepcopy(self.games[ctx.origin_message.guild.id]["current_no1"])
            self.games[ctx.origin_message.guild.id]["last_no2"] = deepcopy(self.games[ctx.origin_message.guild.id]["current_no2"])
            self.games[ctx.origin_message.guild.id]['current_no1'] = randint(1, 10)
            self.games[ctx.origin_message.guild.id]['current_no2'] = randint(1, 10)
            await to_edit.edit(content=f"{self.games[ctx.origin_message.guild.id]['current_no1']}+{self.games[ctx.origin_message.guild.id]['current_no2']}=?")
            self.games[ctx.origin_message.guild.id]["ready"] = True
            await sleep(10)
            while True:
                if self.games[ctx.origin_message.guild.id]["ready"]:
                    self.games[ctx.origin_message.guild.id]["last_no1"] = deepcopy(self.games[ctx.origin_message.guild.id]["current_no1"])
                    self.games[ctx.origin_message.guild.id]["last_no2"] = deepcopy(self.games[ctx.origin_message.guild.id]["current_no2"])
                    self.games[ctx.origin_message.guild.id]['current_no1'] = randint(1, 10)
                    self.games[ctx.origin_message.guild.id]['current_no2'] = randint(1, 10)
                    self.games[ctx.origin_message.guild.id]["to_edit"] = await ctx.send(f"{self.games[ctx.origin_message.guild.id]['current_no1']}+{self.games[ctx.origin_message.guild.id]['current_no2']}=?")
                    await sleep(10)
                    try:
                        self.games[ctx.origin_message.guild.id][f"{self.games[ctx.origin_message.guild.id]['to_edit'].id}_was_answered"]
                    except KeyError:
                        await self.games[ctx.origin_message.guild.id]["to_edit"].delete()
                        self.games[ctx.origin_message.guild.id]["to_edit"] = await ctx.send(f":x: {self.games[ctx.origin_message.guild.id]['last_no1']}+{self.games[ctx.origin_message.guild.id]['last_no2']}={self.games[ctx.origin_message.guild.id]['last_no1']+self.games[ctx.origin_message.guild.id]['last_no2']}")
                        self.games[ctx.origin_message.guild.id]["mistakes"] += 1
                        if self.games[ctx.origin_message.guild.id]["mistakes"] == 5:
                            await ctx.send(f"Congratulations! You answered {self.games[ctx.origin_message.guild.id]['answered']} correctly!")
                            break
                        self.games[ctx.origin_message.guild.id]["ready"] = False
                        await sleep(10)
                        await self.games[ctx.origin_message.guild.id]["to_edit"].edit(content=f"{self.games[ctx.origin_message.guild.id]['current_no1']}+{self.games[ctx.origin_message.guild.id]['current_no2']}=?")
                        self.games[ctx.origin_message.guild.id]["ready"] = True
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild.id in list(self.games.keys()):
            if self.games[message.guild.id]["game"] == "dc":
                if message.reference:
                    if message.reference.resolved:
                        if message.reference.resolved.id == self.games[message.guild.id]["to_edit"].id and message.content == str(self.games[message.guild.id]["last_no1"]+self.games[message.guild.id]["last_no2"]):
                            await message.channel.send("Correct", delete_after=5)
                            await self.games[message.guild.id]["to_edit"].delete()
                            self.games[message.guild.id]["answered"] += 1
                            self.games[message.guild.id][f"{self.games[message.guild.id]['to_edit'].id}_was_answered"] = True
                            self.games[message.guild.id]["last_no1"] = self.games[message.guild.id]["current_no1"]
                            self.games[message.guild.id]["last_no2"] = self.games[message.guild.id]["current_no2"]
                            self.games[message.guild.id]['current_no1'] = randint(1, 10)
                            self.games[message.guild.id]['current_no2'] = randint(1, 10)
                            self.games[message.guild.id]["to_edit"] = await message.channel.send(f"{self.games[message.guild.id]['current_no1']}+{self.games[message.guild.id]['current_no2']}=?")
                


def setup(bot):
    bot.add_cog(ConcentrationTraining(bot))