import discord
from discord.ext import tasks, commands


class GENERAL(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


def setup(dottie):
    dottie.add_cog(GENERAL(dottie))
