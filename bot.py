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
from math import *
import json

discord_token = None
with open("./config.json", "r") as f:
    data = json.load(f)
    discord_token = data["token"]


dottie = commands.Bot(command_prefix="d.")


def is_owner(ctx):
  return ctx.message.author.id in [530781444742578188, 201548633244565504]


def print(*args, sep=" ", end="\n"):
    eloop.create_task(LOG_CHANNEL.send(str(sep).join(str(i)
                                                     for i in args) + end))
    eloop.create_task(LOG_CHANNEL_2.send(str(sep).join(str(i)
                                                       for i in args) + end))


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


TERMINALS = [727087981285998593, 738007255970087014, 740134310044237884]
OWNERS = [530781444742578188, 201548633244565504]


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


LAST_COMMAND_TIMESTAMP = inf


async def infinite_loop():
    global LAST_COMMAND_TIMESTAMP
    while LAST_COMMAND_TIMESTAMP > -inf:
        if time.time() - LAST_COMMAND_TIMESTAMP > 10:
            await dottie.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="github.com/smudgedpasta/Dottie"))
            LAST_COMMAND_TIMESTAMP = inf
        await asyncio.sleep(0.5)


@dottie.event
async def on_message(message):
    global LISTENER
    ctx = await dottie.get_context(message)
    await dottie.invoke(ctx)
    if ctx.command is not None:
        global LAST_COMMAND_TIMESTAMP
        if LAST_COMMAND_TIMESTAMP > time.time():
            await dottie.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="github.com/smudgedpasta/Dottie"))
            LAST_COMMAND_TIMESTAMP = time.time()
    else:
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


eloop.create_task(infinite_loop())


@dottie.event
async def on_ready():
    await dottie.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="github.com/smudgedpasta/Dottie"))
    globals()["LOG_CHANNEL"] = await dottie.fetch_channel(738320254375165962)
    globals()["LOG_CHANNEL_2"] = await dottie.fetch_channel(739982586054705194)
    globals()["eloop"] = asyncio.get_event_loop()
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]
                                ) + "\n[Successfully loaded and ready to go!]```")


@dottie.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You don't have permissions to use that command, you lil' delinquent!")
    if isinstance(error, commands.CommandNotFound):
        if "hepl" in str(error):
            await ctx.send("Did you mean \"help\"?")
        else:
            await ctx.send("Uh, that doesn't exist! Use `d.help` if you're confused!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Hm? Is there something you'd like to say, or am I meant to interpret space? Speak up, I don't bite!")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Hey, I can't find you! You need to be in a voice channel first!")
    try:
        raise error
    except:
        print("```py\n" + traceback.format_exc() + "```")


@dottie.event
async def on_member_join(member):
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]
                                ) + f"\n[{member} has joined the test server.]```")


@dottie.event
async def on_member_remove(member):
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]
                                ) + f"\n[{member} has left the test server.]```")


dottie.remove_command("help")


@dottie.command()
@has_permissions(administrator=True)
async def purge(ctx, amount=1):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Swept away {amount} messages!")
    # if amount < 1:
    if amount == 0:
        await ctx.send(f"How am I meant to purge {amount} messages, silly?".format(amount))


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


@dottie.command()
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour(15277667))
    embed.description = """*I think I need heeelp, I'm drowning in myseeelf* 🎵\n
    **:crossed_swords: __MODERATION__ :crossed_swords:**\n
    ***purge***\n*Clears inputted message count, not counting the command message.*\n***kick***\n*Kicks a user from the server, either by mentioning or stating their username.*\n***ban***\n*Bans a user the same way as* ***kick.***\n***unban***\n*Unbans a user by typing their username and discriminator. (Example: Dottie#7157)*\n
    **:white_heart: __GENERAL__ :white_heart:**\n
    ***help***\n*Legends say you've found this command already.* :eyes:\n***ping***\n*Returns my ping latency.*\n***credits***\n*Gives credit to those who contributed to me, as well as a ref of what I look like!*\n
    **:french_bread: __FUN__ :french_bread:**\n
    ***hello***\n**Aliases: Any variant of "hello" or "hi"**\n*I will greet you back!*\n***AskDottie***\n**Aliases: ask, 8ball**\n*Ask me anything, I'll give a random answer!*\n***ab***\n**Aliases: dab**\n*ab will spell out d.ab with my prefix, so I'll dab!*\n***faker***\n*If someone uses this with a role of my name, I will call you out!*\n
    **:headphones: __VOICE__ :headphones:**\n
    ***connect***\n**Aliases: get_your_butt_in_here, join**\n*Connects me to the voice channel you're in!*\n***disconnect***\n**Aliases: go_naughty_step, leave**\n*Disconnects me from the voice channel I was in!*\n***despacito***\n**Aliases: espacito, Despacito**\n*Plays a totally normal version of Despacito!*\n
    FOR A MORE DETAILED COMMAND LIST, VIEW THE LINK HIDDEN IN THE "**HELP LIST**" TITLE! If you find any bugs or have any enquires, be sure to let my creator, <@530781444742578188>, know!"""
    embed.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/blob/master/CommandsList",
                     icon_url=dottie.user.avatar_url_as(format="png", size=4096))
    await ctx.send(embed=embed)


@dottie.command()
async def ping(ctx):
    await ctx.send(f"```Ping! I pong back my ping latency was {round(dottie.latency * 1000)}ms.```")


@dottie.command()
async def credits(ctx):
    embed = discord.Embed(colour=discord.Colour(15277667))
    embed.description = """Hi! I'm Dottie, a test project by <@530781444742578188>.\n
    Special thanks to <@201548633244565504> and <@245890903133257730> for help with code here and there!\n
    Another special thanks to <@550429134401044490> for designing me and giving me my name! :white_heart:"""
    embed.set_author(name=dottie.user.name, url="https://github.com/smudgedpasta/Dottie",
                     icon_url=dottie.user.avatar_url_as(format="png", size=4096))
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/738007255970087014/738345655012950036/dottie_ref.png")
    await ctx.send(embed=embed)


@dottie.command(aliases=["hi", "HI", "Hi", "hI"] + ["".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate("hello")) for z in range(1, 32)])
async def hello(ctx):
    await ctx.send("Hello, {0.display_name}! :wave:".format(ctx.author))


@dottie.command(aliases=["8ball", "ask"], question=None)
async def AskDottie(ctx, *, question):
    responses = [
        "Heck yeah!",
        "Of course!",
        "I think so!",
        "Meh, sounds alright.",
        "I suppose so...",
        "Hmm, maybe?",
        "Eh?",
        "Probably not...",
        "Try it and find out!",
        "Heheh, I'd like to see you try.",
        "I didn't quite catch that...",
        "Ay, ask me later, I'm busy with my 10 hour tunez!\n\nhttps://cdn.discordapp.com/attachments/739023774405492836/739433348157538344/TUNEZ.gif",
        "Today's AskDottie is sponsored by **Raid Shadow Legends**, one of the BIGGEST mobile role-playing games of 2019 and it's totally free!\n\n*Currently almost 10 million users have joined Raid over the last six months, and it's one of the most impressive games in its class with detailed models, environments and smooth 60 frames per second animations! All the champions in the game can be customized with unique gear that changes your strategic buffs and abilities! The dungeon bosses have some ridiculous skills of their own and figuring out the perfect party and strategy to overtake them's a lot of fun! Currently with over 300,000 reviews, Raid has almost a perfect score on the Play Store! The community is growing fast and the highly anticipated new faction wars feature is now live, you might even find my squad out there in the arena! It's easier to start now than ever with rates program for new players you get a new daily login reward for the first 90 days that you play in the game! So what are you waiting for? Go to the non-existent description, click on the special links and you'll get 50,000 silver and a free epic champion as part of the new player program to start your journey!*\n\nGood luck and I'll see you there!",
        "Side note but did you know that according to all known laws of aviation, there is no way that a bee should be able to fly...?\nIts wings are too small to get its fat little body off the ground...\nThe bee, of course, flies anyway... Because bees don't care what humans think are impossible.\n\nThat's more interesting then what you was going to ask, right?"
    ]
    await ctx.send(f"So you asked... {question}? {random.choice(responses)}")


@dottie.command(aliases=["dab"])
async def ab(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/688253918890688521/739424083556696104/unknown.gif")


@dottie.command(pass_context=True)
@commands.has_any_role("Dottie", "dottie")
async def faker(ctx):
    await ctx.send("What, you think I wouldn't notice you have a role of my name? *There can only be one!* :crossed_swords:")
# async def on_member_update(before, after):
#     n = nick
#     if n:
#         if n.upper().count("Dottie"):
#             user = dottie.get_user()
#             await user.send("I see you there with a nickname of me... *There can only be one!* :crossed_swords:")
#         if n.lower().count("dottie")
#             await user.send("I see you there with a nickname of me... *There can only be one!* :crossed_swords:")


@dottie.command(aliases=["get_your_butt_in_here", "join"], pass_context=True)
async def connect(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()
    await ctx.send("ini\n[Successfully joined the Voice Channel! What a cozy place you got here! 😊]")


@dottie.command(aliases=["go_naughty_step", "leave"], pass_context=True)
async def disconnect(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()
    await ctx.send("ini\n[Successfully disconnected from the Voice Channel... Sad that it is time to go... 😔]")


@dottie.command(aliases=["espacito", "Despacito"])
async def despacito(ctx):
  for vc in dottie.voice_clients:
    if vc.guild == ctx.guild:
        vc.play(discord.FFmpegOpusAudio("music/Normal_Despacito.ogg"))
        return
  await ctx.send("How are you meant to hear my *100% normal Despacito* from outside of a Voice Channel? Hop in one and use `d.connect` first!")


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


@dottie.command()
@commands.check(is_owner)
async def shutdown(ctx):
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]
                                ) + "\n[Cancelling all scheduled events and logging out...]```")
    await ctx.send("```css\n[❗ Shutting down...]```")
    for vc in dottie.voice_clients:
        await vc.disconnect(force=True)
    await asyncio.sleep(0.5)
    await ctx.bot.logout()


@dottie.command()
@commands.check(is_owner)
async def nsfw_test(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send("Test.")
    else:
        await ctx.send("Try using this command in an **nsfw channel**.")


@dottie.command()
@commands.check(is_owner)
async def photo_beta(ctx):
    embed = discord.Embed(colour=discord.Colour(8259923))
    embed.description = ":warning: **GORE WARNING!**\n\nCan't get it up if a girl's breathing."
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/739023774405492836/739509257992667206/SPOILER_Dottie_1.png")
    embed.set_footer(text="Art by Just Jay")
    await ctx.send(embed=embed)


# @dottie.event
# # @commands.guild_only()
# async def on_member_update(before, after):
#     n = after.nick
#     if n:
#         if n.lower().count("Dottie") > 0:
#             prev = before.nick
#             if prev:
#                 await Bot.get_user.send("I see you there with a nickname of me... *There can only be one!* :crossed_swords:")
#             else:
#                 await after.edit(nick="NOT Dottie! ⚔️")


@dottie.command()
@commands.check(is_owner)
async def input_test(ctx):
    await ctx.send("Test. Type 4.")
    response = await dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    if response.content.lower() == "4":
        print("```Success.```")
        await ctx.send("That's right.")
    if response.content.lower() != "4":
        print("```Unsuccess.```")
        await ctx.send("That's not right.")


# for filename in os.listdir("./cogs"):
#     if filename.endswith(".py"):
#         dottie.load_extension(f"cogs.{filename[:-3]}")


dottie.run(discord_token)
