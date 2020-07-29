import discord
from discord.ext import commands

dottie = commands.Bot(command_prefix = "d.")

@dottie.event
async def on_ready():
    print("I am ready!")
    
@dottie.event
async def on_member_join(member):
    print(f"{member} has joined the test server.")

@dottie.event
async def on_member_remove(member):
    print(f"{member} has left the test server.")

# dottie.run("The token goes here, I'm keeping it hidden due to publicity")
