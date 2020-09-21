import discord
from discord.ext import tasks, commands


class OWNER(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


def setup(dottie):
    dottie.add_cog(OWNER(dottie))
