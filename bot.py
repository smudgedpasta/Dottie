#!/usr/bin/python3


# Imports all required modules... As a module 🙃
from modules import *


# Hides the Discord Token behind an unseen json file
discord_token = None
with open("config.json", "r") as f:
    data = json.load(f)
    discord_token = data["token"]


# Sets the default command prefix to either "d." or @'ing the bot
dottie = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX))

# Removes the default help command from discord.ext
dottie.remove_command("help")


# Defaults message count to always start at 0
messages = 0


LISTENER = None


def input(*args, **kwargs):
    global LISTENER
    print(*args, **kwargs)
    LISTENER = dottie
    t = time.time()
    while LISTENER is dottie and time.time() - t < 86400:
        time.sleep(0.2)
    return LISTENER

# Overwrites the python print mechanic to send terminal logs to a log channel
_print = print
def print(*args, sep=" ", end="\n"):
    create_task(LOG_CHANNEL.send(str(sep).join(str(i) for i in args) + end))
    create_task(LOG_CHANNEL_2.send(str(sep).join(str(i) for i in args) + end))
    _print(*args)


dottie.eloop = eloop


# Assigning a list of channels to act as a python terminal within Discord
TERMINALS = [727087981285998593, 751518107922858075]


# Copy of the global variables for use by the terminal
GLOBALS = globals()
glob = dict(GLOBALS)
# The custom message cache which is fed to by dottie._connection._messages
MESSAGES = {}


# Processes a function as python code, using a copy of the global variables, and able to run coroutines
async def procFunc(proc):
    # Updates all of the entries in the custom cache
    MESSAGES.update({m.id: m for m in dottie._connection._messages})
    while len(MESSAGES) > 1048576:
        MESSAGES.pop(next(iter(MESSAGES)))
    glob["messages"] = MESSAGES
    glob["guilds"] = dottie._connection._guilds
    glob["users"] = dottie._connection._users
    glob["emojis"] = dottie._connection._emojis
    glob["channels"] = {c.id: c for g in dottie.guilds for c in g.channels}
    glob["roles"] = {r.id: r for g in dottie.guilds for r in g.roles}
    # Just get rid of "await " if the code is only one line long, leave it to later
    if "\n" not in proc:
        if proc.startswith("await "):
            proc = proc[6:]
    # Try the basic `eval` function, as that's what the basic python terminal tries to do first
    code = None
    try:
        code = await create_future(compile, proc, "<terminal>", "eval", optimize=2)
    except SyntaxError:
        pass
    # If `eval` wasn't successful, try to use `exec`, which can run multiple lines of python code as well as assign variables, but cannot return a value
    if code is None:
        try:
            code = await create_future(compile, proc, "<terminal>", "exec", optimize=2)
        except SyntaxError:
            pass
    # If both were unsuccessful, simulate the code as an `async def` function, possibly returning a variable
    if code is None:
        # This is a very hacky mess but it works 🙃
        _ = glob.get("_")
        func = "async def _():\n\tlocals().update(globals())\n"
        func += "\n".join("\t" + line for line in proc.split("\n"))
        func += "\n\tglobals().update(locals())"
        code2 = await create_future(compile, func, "<terminal>", "exec", optimize=2)
        await create_future(eval, code2, glob)
        output = await glob["_"]()
        glob["_"] = _
    # Runs the code if it's not `None`
    if code is not None:
        output = await create_future(eval, code, glob)
    # If the code returned a value that wasn't `None`, set the variable "_" to that value (similar to basic python terminals)
    if output is not None:
        glob["_"] = output
    # Also return the value to be displayed in the terminal channel
    return output


LAST_COMMAND_TIMESTAMP = inf


async def status_update_loop():
    global LAST_COMMAND_TIMESTAMP
    while LAST_COMMAND_TIMESTAMP > -inf:
        if time.time() - LAST_COMMAND_TIMESTAMP > 20:
            await dottie.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="over " + str(len(dottie.guilds)) + " servers! 🐾"))
            LAST_COMMAND_TIMESTAMP = inf
        await asyncio.sleep(0.5)


@dottie.event
async def on_message(message):
    ctx = await dottie.get_context(message)
    # Checks the message for mentions, and if Dottie is mentioned, respond
    if dottie.user in message.mentions:
        await ctx.send(f"Hi, {message.author.display_name}! My prefix is " + PREFIX + " so if you're looking for my commands, use `" + PREFIX + "help`!")

    # Gets each message sent that Dottie can see and adds on 1 each time.
    global messages
    messages += 1
    ctx = await dottie.get_context(message)
    # Invokes command to a dispatch method (determining what method should be invoked)
    await dottie.invoke(ctx)

    # Just a fun feature calling Smudge (the bot's creator) out for a common typo 🙃
    Smudge = [530781444742578188, 668064931345596439]
    if message.author.id in Smudge and message.content.endswith("#"):
        await ctx.send("Smudge Keyboard Moment <a:moment" + ":750685242553139321>")

    # Makes sure this part only runs if the message was a command
    if ctx.command is not None:
        user = message.author.name
        cmd = message.content
        # Logs the usage of a command.
        if getattr(message.author, "guild", None) is None:
            cmd = cmd.replace("`", "")
            print(f"```" + random.choice(["css", "ini"]) + f"\n[{user}] has run the following command: [{cmd}] in [Direct Messages]```")
        else:
            cmd = cmd.replace("`", "")
            print(f"```" + random.choice(["css", "ini"]) + f"\n[{user}] has run the following command: [{cmd}] in [{message.author.guild}]```")

        # Causes a temporary status change to indicate that a command has been used
        global LISTENER
        global LAST_COMMAND_TIMESTAMP
        if LAST_COMMAND_TIMESTAMP > time.time():
            await dottie.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="whoever summoned me! 👀"))
            LAST_COMMAND_TIMESTAMP = time.time()

    # Creates a DM relay to send all incoming DM's to the same channel(s) where the terminal is active
    elif getattr(message.channel, "guild", None) is None and message.author != dottie.user:
        if ctx.command is None:
            user_dm = message.author
            embed = discord.Embed(colour=discord.Colour(197379), timestamp=ctx.message.created_at)
            embed.set_author(name=f"Incoming DM from {user_dm}!", icon_url="https://cdn.discordapp.com/attachments/751513839169831083/757326045450862754/DM_Thumbnail.png")
            embed.set_thumbnail(url=ctx.author.avatar_url_as(format="png", size=4096))
            embed.description = f"{message.content}"
            embed.set_footer(text=f"User ID: {ctx.author.id}")
            await dottie.get_channel(727087981285998593).send(embed=embed)
            await dottie.get_channel(751518107922858075).send(embed=embed)
            
    # Creates the in-Discord python terminal
    else:
        channel = message.channel
        if channel.id in TERMINALS:
            if message.author.id in OWNERS:
                proc = message.content.strip()
                if proc:
                    # Treats messages beginning with "//", "||", "\\" or "#" as comments, to prevent them returning None
                    if proc.startswith("//") or proc.startswith("||") or proc.startswith("\\") or proc.startswith("#"):
                        return
                    # If the message contains codeblock characters, remove them
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
                        output = await procFunc(proc)
                        await channel.send("```\n" + str(output)[:1993] + "```")
                    except:
                        await channel.send("```py\n" + traceback.format_exc()[:1991] + "```")
      
eloop.create_task(status_update_loop())


@dottie.event
async def on_ready():
    await dottie.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="over " + str(len(dottie.guilds)) + " servers! 🐾"))
    # Assigns the channels acting as a log channel
    globals()["LOG_CHANNEL"] = dottie.get_channel(738320254375165962)
    globals()["LOG_CHANNEL_2"] = dottie.get_channel(751517870009352192)
    globals()["eloop"] = asyncio.get_event_loop()
    # Sends a message to the log channel signifying that Dottie has logged in successfully
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]) + f"\n[Logged in as user {dottie.user} (ID = {dottie.user.id})]```")
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]) + "\n[Successfully loaded and ready to go!]```")
    # The random markdown allows the log to send messages in multicolours


async def serverstats_update():
    await dottie.wait_until_ready()
    global messages
    while not dottie.is_closed():
        # ~~This was just where it used to go to a file whoops~~
        try:
            # Simply counts all the messages sent within the hour and logs it to the log channel
            globals()["LOG_CHANNEL"] = dottie.get_channel(738320254375165962)
            globals()["LOG_CHANNEL_2"] = dottie.get_channel(751517870009352192)
            globals()["eloop"] = asyncio.get_event_loop()
            print(f"```" + random.choice(["css", "ini"]) + f"\nTime at log interval: [{datetime.datetime.utcnow().strftime('%a, %#d %B %Y, %I:%M %p')}, GMT] | Messages sent within 60m interval: [{messages}]```".format())
            # Defaults the message count back down to 0
            messages = 0
        except Exception as e:
            print(e)
        await asyncio.sleep(3600)

dottie.loop.create_task(serverstats_update())


# Checks if a particular error has occured and sends a message if its necessary
@dottie.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You don't have permissions to use that command, you lil' delinquent!")
    if isinstance(error, commands.CommandNotFound):
        # ~~Aka me making fun of my friend's typos~~
        if str(error).split("\"")[1] in ["hepl", "hepk", "hlep", "hekp", "pleh"]:
            await ctx.send("Did you mean \"help\"?")
        elif str(error).split("\"")[1] in ["cars", "cat"]:
            await ctx.send("Did you mean \"cats\"?")
        elif str(error).split("\"")[1] in ["pign"]:
            await ctx.send("Did you mean \"ping\"? ~~I hate to break it to you but I'm not a Minecraft Piglin...~~")
        else:
            await ctx.send("Uh, that doesn't exist! Use `" + PREFIX + "help` if you're confused!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Hm? Is there something you'd like to say, or am I meant to interpret space? Speak up, I don't bite!")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("```fix\n⚠️ Unexpected error! Either use this command with a required argument, or report this as a bug to smudgedpasta.```")
    try:
        raise error
    except:
        print("```py\n" + traceback.format_exc() + "```")


# When a user joins or leaves a server Dottie is in, it logs to the log channel
@dottie.event
async def on_member_join(member):
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]) + f"\n[{member}] has joined [{member.guild}]```")

@dottie.event
async def on_member_remove(member):
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]) + f"\n[{member}] has left [{member.guild}]```")


@dottie.event
async def on_guild_join(guild):
    target_channel = None

    embed = discord.Embed(colour=discord.Colour(15277667))
    embed.description = """Hi! I'm Dottie, a test project by <@530781444742578188>- with the help of <@201548633244565504> and <@245890903133257730> of course! :white_heart:\n
For a list of my commands, use the classic command of `""" + PREFIX + """help`. For a more detailed list of what I can do, visit https://github.com/smudgedpasta/Dottie/blob/master/CommandsList. You can find my source code over there too if you're interested!\n
Thanks for inviting me! 😊"""
    embed.set_author(name=dottie.user.name, url="https://github.com/smudgedpasta/Dottie", icon_url=dottie.user.avatar_url_as(format="png", size=4096))
    embed.set_image(url="https://cdn.discordapp.com/attachments/703579929840844891/740522679697932349/Dottie.gif")

    # Checks for channels by a specific name to send an introductory embed when Dottie joins a server
    for channel in ["bots", "dottie", "general", "text", "convo", "chat"]:
        target_channel = discord.utils.get(guild.text_channels, name=channel)
        if target_channel and target_channel.permissions_for(guild.me).send_messages:
            break

    # If there are no targetted channels, send the embed to the first text channel with send_message permissions
    if not target_channel:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                target_channel = channel
                break
    if target_channel:
        await target_channel.send(embed=embed)


# If a cog(s) is disabled, this re-enables it
@dottie.command()
@commands.check(is_owner)
async def load(ctx, extension=None):
    if extension is None:
        dottie.load_extension("cogs.moderation")
        dottie.load_extension("cogs.general")
        dottie.load_extension("cogs.fun")
        dottie.load_extension("cogs.voice")
        dottie.load_extension("cogs.owner")
        await ctx.send("```fix\n[Successfully returned acces to all extensions.]```")
        return
    dottie.load_extension(f"cogs.{extension}")
    await ctx.send(f"```ini\n[Successfully returned access to category \"{extension.upper()}\".]```")


# If a cog(s) is already enabled, this disables it
@dottie.command()
@commands.check(is_owner)
async def unload(ctx, extension=None):
    if extension is None:
        dottie.unload_extension("cogs.moderation")
        dottie.unload_extension("cogs.general")
        dottie.unload_extension("cogs.fun")
        dottie.unload_extension("cogs.voice")
        dottie.unload_extension("cogs.owner")
        await ctx.send("```fix\n[Successfully removed all extensions until further notice.]```")
        return
    dottie.unload_extension(f"cogs.{extension}")
    await ctx.send(f"```asciidoc\n[Successfully removed category \"{extension.upper()}\" until further notice.]```")


# Refreshes a cog(s) so changes can be made and applied to the code without having to re-run anything
@dottie.command()
@commands.check(is_owner)
async def reload(ctx, extension=None):
    if extension is None:
        dottie.unload_extension("cogs.moderation")
        dottie.load_extension("cogs.moderation")
        dottie.unload_extension("cogs.general")
        dottie.load_extension("cogs.general")
        dottie.unload_extension("cogs.fun")
        dottie.load_extension("cogs.fun")
        dottie.unload_extension("cogs.voice")
        dottie.load_extension("cogs.voice")
        dottie.unload_extension("cogs.owner")
        dottie.load_extension("cogs.owner")
        await ctx.send("```fix\n[Successfully refreshed all extensions.]```")
        return
    dottie.unload_extension(f"cogs.{extension}")
    dottie.load_extension(f"cogs.{extension}")
    await ctx.send(f"```fix\n[Successfully refreshed category \"{extension.upper()}\".]```")


# Loads all cogs into this file
for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # Removes ".py" as a part of the extension name
            dottie.load_extension(f"cogs.{filename[:-3]}")


dottie.run(discord_token)
