import discord
from discord.ext import commands

import json

discord_token = None
with open("./config.json", "r") as f:
    data = json.load(f)
    discord_token = data["token"]

import random


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

@dottie.command(aliases = ["Hi", "Hello", "hi", "HI", "HELLO", "hElLo", "HeLlO", "hI"])
async def hello(ctx):
    await ctx.send("Hello! 👋")

@dottie.command()
async def ping(ctx):
    await ctx.send(f"Ping! I pong back your ping latency was {round(dottie.latency * 1000)}ms.")

@dottie.command(aliases = ["8ball", "AskDottie", "ask"])
async def _8ball(ctx, *, question):
    responses = ["Heck yeah!",
                 "Hmm, maybe?",
                 "Probably not...",
                 "Try it and find out!",
                 "Heheh, I'd like to see you try.",
                 "I didn't quite catch that...",
                 "Ay, ask me later, I'm busy with my 10 hour tunez!"]
    await ctx.send(f"So you asked... {question}? {random.choice(responses)}")
    
dottie.run(discord_token)
