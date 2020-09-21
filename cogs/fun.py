import discord
from discord.ext import tasks, commands


class FUN(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command()
    async def test(self, ctx):
        await ctx.send("```COGS ARE OPPERATIONAL.```")


    @commands.command(aliases=["hi", "HI", "Hi", "hI", "hemlo", "henlo", "hoi"] + ["".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate("hello")) for z in range(1, 32)])
    async def hello(self, ctx):
        await ctx.send("Hello, {0.display_name}! :wave:".format(ctx.author))


def setup(dottie):
    dottie.add_cog(FUN(dottie))
