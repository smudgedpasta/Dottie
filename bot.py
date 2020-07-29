import discord
from discord.ext import commands

client = commands.Bot(command_prefix = 'd.')

@client.event
async def on_ready():
    print('I am ready!')

# client.run(The token goes here, I'm keeping it hidden due to publicity)