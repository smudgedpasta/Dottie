import discord
from discord.ext import commands

import json

discord_token = None
with open("./config.json", "r") as f:
    data = json.load(f)
    discord_token = data["token"]

import asyncio
import random


dottie = commands.Bot(command_prefix="d.")


def print(*args, sep=" ", end="\n"):
    asyncio.create_task(LOG_CHANNEL.send(str(sep).join(str(i) for i in args) + end))
    # asyncio.create_task(LOG_CHANNEL_2.send(str(sep).join(str(i) for i in args) + end))


@dottie.event
async def on_ready():
    globals()["LOG_CHANNEL"] = await dottie.fetch_channel(738320254375165962)
    # globals()["LOG_CHANNEL_2"] = await dottie.fetch_channel(738003426218213389)
    print("```Successfully loaded and ready to go!```")


@dottie.event
async def on_member_join(member):
    print(f"```{member} has joined the test server.```")

@dottie.event
async def on_member_remove(member):
    print(f"```{member} has left the test server.```")


@dottie.command(aliases=["Hi", "Hello", "hi", "HI", "HELLO", "hElLo", "HeLlO", "hI", "hElLO"])
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

@dottie.command()
async def credits(ctx):
    embed = discord.Embed(colour=discord.Colour(15277667))
    embed.description = """Hi! I'm Dottie, a test project by <@530781444742578188>.\n
    Special thanks to <@201548633244565504> and <@245890903133257730> for help with code here and there!\n
    Another special thanks to <@550429134401044490> for designing me, giving me my name and making my icon! :white_heart:"""
    embed.set_author(name=dottie.user.name, url="https://github.com/smudgedpasta/Dottie",
                 icon_url=dottie.user.avatar_url_as(format="png", size=4096))
    embed.set_image(
    url="https://cdn.discordapp.com/attachments/738007255970087014/738345655012950036/dottie_ref.png")
    await ctx.send(embed=embed)


dottie.run(discord_token)
