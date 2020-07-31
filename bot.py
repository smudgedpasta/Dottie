import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure

import json

discord_token = None
with open("./config.json", "r") as f:
    data = json.load(f)
    discord_token = data["token"]

import traceback
import os
import asyncio
import random


dottie = commands.Bot(command_prefix="d.")


def print(*args, sep=" ", end="\n"):
    asyncio.create_task(LOG_CHANNEL.send(str(sep).join(str(i) for i in args) + end))


@dottie.event
async def on_ready():
    globals()["LOG_CHANNEL"] = await dottie.fetch_channel(738320254375165962)
    print("```" + random.choice(["", "ini", "asciidoc", "fix"]) + "\n[Successfully loaded and ready to go!]```")


@dottie.command()
async def load(ctx, extension=None):
    if extension is None:
        await ctx.send("```css\n⚠️[Specify the extension.]⚠️```")
    dottie.load_extension(f"cogs.{extension}")
    await ctx.send("```ini\n[Successfully returned access to the extension.]```")

@dottie.command()
async def unload(ctx, extension=None):
    if extension is None:
        await ctx.send("```css\n⚠️[Specify the extension.]⚠️```")
    dottie.unload_extension(f"cogs.{extension}")
    await ctx.send("```css\n[Successfully removed the extension until further notice.]```")

@dottie.command()
async def reload(ctx, extension=None):
    if extension is None:
        await ctx.send("```css\n⚠️[Specify the extension.]⚠️```")
    dottie.unload_extension(f"cogs.{extension}")
    dottie.load_extension(f"cogs.{extension}")
    await ctx.send("```fix\n[Successfully refreshed the extension.]```")


@dottie.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You don't have permissions to use that command, you lil' delinquent!")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Uh, that doesn't exist! Use `d.help` if you're confused!")
    try:
        raise error
    except:
        print("```py\n" + traceback.format_exc() + "```")


@dottie.event
async def on_member_join(member):
    print("```" + random.choice(["", "ini", "asciidoc", "fix"]) + f"\n[{member} has joined the test server.]```")

@dottie.event
async def on_member_remove(member):
    print("```" + random.choice(["", "ini", "asciidoc", "fix"]) + f"\n[{member} has left the test server.]```")


@dottie.command(aliases=["hi", "HI", "Hi", "hI"] + ["".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate("hello")) for z in range(1, 32)])
async def hello(ctx):
         await ctx.send("Hello, {0.display_name}! :wave:".format(ctx.author))
        

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
   

@dottie.command()
@has_permissions(administrator=True)
async def purge(ctx, amount=1):
    await ctx.channel.purge(limit=amount+1)
    if amount == 0:
        await ctx.send("How am I meant to purge 0 messages, silly?")


@dottie.command(pass_context=True)
@has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reasons=None):
    await member.kick(reason=reasons)
    await ctx.send(f"{member.name}#{member.discriminator} has been *yeet* right out the server! :lock:")
        

@dottie.command()
@has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reasons=None):
    await member.ban(reason=reasons)
    await ctx.send(f"Good riddance, {member.name}#{member.discriminator}! :closed_lock_with_key:")
   

@dottie.command()
@has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Granted access back to the server for {user.name}#{user.discriminator}. :unlock:")
            return


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        dottie.load_extension(f"cogs.{filename[:-3]}")

dottie.run(discord_token)
