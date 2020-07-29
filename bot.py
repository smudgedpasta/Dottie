import discord
from discord.ext import commands

dottie = commands.Bot(command_prefix = 'd.')

@dottie.event
async def on_ready():
    print('I am ready!')

# dottie.run(The token goes here, I'm keeping it hidden due to publicity)
