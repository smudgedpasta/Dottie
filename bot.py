import concurrent.futures
import inspect
import time
import random
import asyncio
import os
import traceback
import discord
from discord.ext import tasks, commands
from discord.ext.commands import Bot, has_permissions, CheckFailure

import json

discord_token = None
with open("./config.json", "r") as f:
    data = json.load(f)
    discord_token = data["token"]


dottie = commands.Bot(command_prefix="d.")

def is_owner(ctx):
  return ctx.message.author.id in [530781444742578188]


dottie.remove_command("help")


def print(*args, sep=" ", end="\n"):
    eloop.create_task(LOG_CHANNEL.send(str(sep).join(str(i) for i in args) + end))


LISTENER = None


def input(*args, **kwargs):
    global LISTENER
    print(*args, **kwargs)
    LISTENER = dottie
    t = time.time()
    while LISTENER is dottie and time.time() - t < 86400:
        time.sleep(0.2)
    return LISTENER


eloop = asyncio.get_event_loop()
def __setloop__(): return asyncio.set_event_loop(eloop)


athreads = concurrent.futures.ThreadPoolExecutor(
    max_workers=16,
    initializer=__setloop__,
)
__setloop__()


def wrap_future(fut, loop=None):
    if loop is None:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = eloop
    new_fut = loop.create_future()

    def on_done(*void):
        try:
            result = fut.result()
        except Exception as ex:
            loop.call_soon_threadsafe(new_fut.set_exception, ex)
        else:
            loop.call_soon_threadsafe(new_fut.set_result, result)

    fut.add_done_callback(on_done)
    return new_fut


create_future = lambda func, * \
    args, loop=None, **kwargs: wrap_future(athreads.submit(func, *args, **kwargs), loop=loop)


def awaitable(obj): return hasattr(obj, "__await__") or issubclass(type(
    obj), asyncio.Future) or issubclass(type(obj), asyncio.Task) or inspect.isawaitable(obj)


async def forceCoro(obj, *args, **kwargs):
    if asyncio.iscoroutinefunction(obj):
        obj = obj(*args, **kwargs)
    elif callable(obj):
        if asyncio.iscoroutinefunction(obj.__call__):
            obj = obj.__call__(*args, **kwargs)
        else:
            obj = await create_future(obj, *args, **kwargs)
    while awaitable(obj):
        obj = await obj
    return obj


TERMINALS = [727087981285998593, 738007255970087014]
OWNERS = [530781444742578188]


GLOBALS = globals()
glob = dict(GLOBALS)


async def procFunc(proc, channel):
    if "\n" not in proc:
        if proc.startswith("await "):
            proc = proc[6:]
    try:
        code = await create_future(compile, proc, "<terminal>", "eval", optimize=2)
    except SyntaxError:
        code = await create_future(compile, proc, "<terminal>", "exec", optimize=2)
    output = await forceCoro(eval, code, glob)
    if output is not None:
        glob["_"] = output
    return output


@dottie.event
async def on_message(message):
    global LISTENER
    await dottie.process_commands(message)
    channel = message.channel
    if channel.id in TERMINALS:
        if message.author.id in OWNERS:
            proc = message.content.strip()
            if proc:
                if proc.startswith("//") or proc.startswith("||") or proc.startswith("\\") or proc.startswith("#"):
                    return
                if proc.startswith("`") and proc.endswith("`"):
                    proc = proc.strip("`")
                if not proc:
                    return
                if LISTENER is dottie:
                    LISTENER = proc
                    return
                if not proc:
                    return
                output = None
                try:
                    output = await procFunc(proc, channel)
                    await channel.send("```\n" + str(output)[:1993] + "```")
                except:
                    await channel.send("```py\n" + traceback.format_exc()[:1991] + "```")


@dottie.event
async def on_ready():
    await dottie.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name="github.com/smudgedpasta/Dottie"))
    globals()["LOG_CHANNEL"] = await dottie.fetch_channel(738320254375165962)
    globals()["eloop"] = asyncio.get_event_loop()
    print("```" + random.choice(["", "ini", "asciidoc", "fix"]) + "\n[Successfully loaded and ready to go!]```")


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


@dottie.command()
@commands.check(is_owner)
async def load(ctx, extension=None):
    if extension is None:
        await ctx.send("```css\n⚠️[Specify the extension.]⚠️```")
    dottie.load_extension(f"cogs.{extension}")
    await ctx.send("```ini\n[Successfully returned access to the extension.]```")


@dottie.command()
@commands.check(is_owner)
async def unload(ctx, extension=None):
    if extension is None:
        await ctx.send("```css\n⚠️[Specify the extension.]⚠️```")
    dottie.unload_extension(f"cogs.{extension}")
    await ctx.send("```css\n[Successfully removed the extension until further notice.]```")


@dottie.command()
@commands.check(is_owner)
async def reload(ctx, extension=None):
    if extension is None:
        await ctx.send("```css\n⚠️[Specify the extension.]⚠️```")
    dottie.unload_extension(f"cogs.{extension}")
    dottie.load_extension(f"cogs.{extension}")
    await ctx.send("```fix\n[Successfully refreshed the extension.]```")


@dottie.event
async def on_member_join(member):
    print("```" + random.choice(["", "ini", "asciidoc", "fix"]) + f"\n[{member} has joined the test server.]```")


@dottie.event
async def on_member_remove(member):
    print("```" + random.choice(["", "ini", "asciidoc", "fix"]) + f"\n[{member} has left the test server.]```")


@dottie.command(aliases=["beta_help"], pass_context=True)
@commands.check(is_owner)
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour(15277667))
    embed.description = """*I think I need heeelp, I'm drowning in myseeelf* 🎵\n
    **:crossed_swords: __MODERATION__ :crossed_swords:**\n
    ***purge***\n*Clears inputted message count, not counting the command message.*\n***kick***\n*Kicks a user from the server, either by mentioning or stating their username.*\n***ban***\n*Bans a user the same way as* ***kick.***\n***unban***\n*Unbans a user by typing their username and discriminator. (Example: Dottie#7157)*\n
    **:white_heart: __GENERAL__ :white_heart:**\n
    ***help***\n*Legends say you've found this command already.* :eyes:\n***ping***\n*Returns my ping latency.*\n***credits***\n*Gives credit to those who contributed to me, as well as a ref of what I look like!*\n
    **:french_bread: __FUN__ :french_bread:**\n
    ***hello***\n**Aliases: Any variant of "hello" or "hi"**\n*I will greet you back!*\n***AskDottie***\n**Aliases: ask, 8ball**\n*Ask me anything, I'll give a random answer!*\n
    If you find any bugs or have any enquires, be sure to let my creator, <@530781444742578188>, know!"""
    embed.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/blob/master/CommandsList", icon_url=dottie.user.avatar_url_as(format="png", size=4096))
    await ctx.send(embed=embed)


@dottie.command(aliases=["hi", "HI", "Hi", "hI"] + ["".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate("hello")) for z in range(1, 32)])
async def hello(ctx):
    await ctx.send("Hello, {0.display_name}! :wave:".format(ctx.author))


@dottie.command()
async def ping(ctx):
    await ctx.send(f"```Ping! I pong back my ping latency was {round(dottie.latency * 1000)}ms.```") 


@dottie.command(aliases=["8ball", "ask"])
async def AskDottie(ctx, *, question):
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
    if amount < 1:
      await ctx.send(f"How am I meant to purge {amount} messages, silly?".format(amount))
      return
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Swept away {amount} messages!")


@dottie.command(pass_context=True)
@has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reasons=None):
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


# for filename in os.listdir("./cogs"):
#     if filename.endswith(".py"):
#         dottie.load_extension(f"cogs.{filename[:-3]}")


dottie.run(discord_token)
