# This file serves as a template
# Name the class the file name ⚠️

import discord
from discord.ext import commands

class cogs(commands.Cog):

    def __init__(self, dottie):
        self.dottie = dottie

    @commands.command()
    async def example(self, ctx):
        await ctx.send("```Dev test.```")

def setup (dottie):
    dottie.add_cog(cogs(dottie))
