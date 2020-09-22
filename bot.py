from modules import *


discord_token = None
with open("config.json", "r") as f:
    data = json.load(f)
    discord_token = data["token"]


dottie = commands.Bot(command_prefix=commands.when_mentioned_or("d."))


OWNERS = [530781444742578188, 201548633244565504]

def is_owner(ctx):
  return ctx.message.author.id in OWNERS


messages = 0

players = {}

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

def print(*args, sep=" ", end="\n"):
    eloop.create_task(LOG_CHANNEL.send(str(sep).join(str(i) for i in args) + end))
    eloop.create_task(LOG_CHANNEL_2.send(str(sep).join(str(i) for i in args) + end))

dottie.eloop = eloop


athreads = concurrent.futures.ThreadPoolExecutor(
    max_workers=16,
    initializer=__setloop__,)
__setloop__()


def get_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return eloop

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


def awaitable(obj): return hasattr(obj, "__await__") or issubclass(type(obj), asyncio.Future) or issubclass(type(obj), asyncio.Task) or inspect.isawaitable(obj)


def create_future_ex(func, *args, timeout=None, **kwargs):
    fut = athreads.submit(func, *args, **kwargs)
    if timeout is not None:
        fut = athreads.submit(fut.result, timeout=timeout)
    return fut


async def _create_future(obj, *args, loop, timeout, **kwargs):
    if asyncio.iscoroutinefunction(obj):
        obj = obj(*args, **kwargs)
    elif callable(obj):
        if asyncio.iscoroutinefunction(obj.__call__) or not is_main_thread():
            obj = obj.__call__(*args, **kwargs)
        else:
            obj = await wrap_future(create_future_ex(obj, *args, timeout=timeout, **kwargs), loop=loop)
    while awaitable(obj):
        if timeout is not None:
            obj = await asyncio.wait_for(obj, timeout=timeout)
        else:
            obj = await obj
    return obj


def create_future(obj, *args, loop=None, timeout=None, **kwargs):
    if loop is None:
        loop = get_event_loop()
    fut = _create_future(obj, *args, loop=loop, timeout=timeout, **kwargs)
    return create_task(fut, loop=loop)


def create_task(fut, *args, loop=None, **kwargs):
    if loop is None:
        loop = get_event_loop()
    return asyncio.ensure_future(fut, *args, loop=loop, **kwargs)

is_main_thread = lambda: threading.current_thread() is threading.main_thread()


TERMINALS = [757848291181461574]


GLOBALS = globals()
glob = dict(GLOBALS)
MESSAGES = {}


async def procFunc(proc, channel):
    MESSAGES.update({m.id: m for m in dottie._connection._messages})
    while len(MESSAGES) > 1048576:
        MESSAGES.pop(next(iter(MESSAGES)))
    glob["messages"] = MESSAGES
    glob["guilds"] = dottie._connection._guilds
    glob["users"] = dottie._connection._users
    glob["emojis"] = dottie._connection._emojis
    glob["channels"] = {c.id: c for g in dottie.guilds for c in g.channels}
    glob["roles"] = {r.id: r for g in dottie.guilds for r in g.roles}
    if "\n" not in proc:
        if proc.startswith("await "):
            proc = proc[6:]
    code = None
    try:
        code = await create_future(compile, proc, "<terminal>", "eval", optimize=2)
    except SyntaxError:
        pass
    if code is None:
        try:
            code = await create_future(compile, proc, "<terminal>", "exec", optimize=2)
        except SyntaxError:
            pass
    if code is None:
        _ = glob.get("_")
        func = "async def _():\n\tlocals().update(globals())\n"
        func += "\n".join("\t" + line for line in proc.split("\n"))
        func += "\n\tglobals().update(locals())"
        code2 = await create_future(compile, func, "<terminal>", "exec", optimize=2)
        await create_future(eval, code2, glob)
        output = await glob["_"]()
        glob["_"] = _
    if code is not None:
        output = await create_future(eval, code, glob)
    if output is not None:
        glob["_"] = output
    return output


LAST_COMMAND_TIMESTAMP = inf


async def infinite_loop():
    global LAST_COMMAND_TIMESTAMP
    while LAST_COMMAND_TIMESTAMP > -inf:
        if time.time() - LAST_COMMAND_TIMESTAMP > 20:
            await dottie.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="over " + str(len(dottie.guilds)) + " servers! 🐾"))
            LAST_COMMAND_TIMESTAMP = inf
        await asyncio.sleep(0.5)


@dottie.event
async def on_message(message):
    global messages
    messages += 1
    ctx = await dottie.get_context(message)
    await dottie.invoke(ctx)

    if ctx.command is not None:
        user = message.author.name
        cmd = message.content
        if getattr(message.author, "guild", None) is None:
            cmd = cmd.replace("`", "")
            print(f"```" + random.choice(["css", "ini"]) + f"\n[{user}] has run the following command: [{cmd}] in [Direct Messages]```")
        else:
            cmd = cmd.replace("`", "")
            print(f"```" + random.choice(["css", "ini"]) + f"\n[{user}] has run the following command: [{cmd}] in [{message.author.guild}]```")

    if getattr(message.channel, "guild", None) is None and message.author != dottie.user:
        if ctx.command is None:
            user_dm = message.author
            embed = discord.Embed(colour=discord.Colour(197379), timestamp=ctx.message.created_at)
            embed.set_author(name=f"Incoming DM from {user_dm}!", icon_url="https://cdn.discordapp.com/attachments/751513839169831083/757326045450862754/DM_Thumbnail.png")
            embed.set_thumbnail(url=ctx.author.avatar_url_as(format="png", size=4096))
            embed.description = f"{message.content}"
            embed.set_footer(text=f"User ID: {ctx.author.id}")
            await dottie.get_channel(727087981285998593).send(embed=embed)
            await dottie.get_channel(751518107922858075).send(embed=embed)

        global LISTENER
        global LAST_COMMAND_TIMESTAMP
        if LAST_COMMAND_TIMESTAMP > time.time():
            await dottie.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="whoever summoned me! 👀"))
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
    await dottie.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="over " + str(len(dottie.guilds)) + " servers! 🐾"))
    globals()["LOG_CHANNEL"] = dottie.get_channel(738320254375165962)
    globals()["LOG_CHANNEL_2"] = dottie.get_channel(751517870009352192)
    globals()["eloop"] = asyncio.get_event_loop()
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]) + "\n[Logged in as user {0} (ID = {0.id})]```".format(dottie.user))
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]) + "\n[Successfully loaded and ready to go!]```")


async def serverstats_update():
    await dottie.wait_until_ready()
    global messages
    while not dottie.is_closed():
        try:
            globals()["LOG_CHANNEL"] = dottie.get_channel(738320254375165962)
            globals()["LOG_CHANNEL_2"] = dottie.get_channel(751517870009352192)
            globals()["eloop"] = asyncio.get_event_loop()
            print(f"```" + random.choice(["css", "ini"]) + f"\nTime at log interval: [{datetime.datetime.utcnow().strftime('%a, %#d %B %Y, %I:%M %p')}, GMT] | Messages sent within 60m interval: [{messages}]```".format())
            messages = 0
        except Exception as e:
            print(e)
        await asyncio.sleep(3600)

dottie.loop.create_task(serverstats_update())


# async def leveldata_update(member, guild):
#     with open("bot/leveldata.json", "w") as f:
#         f.write(str(leveldata))

#     with open("bot/leveldata.json", "r") as f:
#         data = eval(f.read())


@dottie.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You don't have permissions to use that command, you lil' delinquent!")
    if isinstance(error, commands.CommandNotFound):
        if str(error).split("\"")[1] in ["hepl", "hepk", "hlep", "hekp", "pleh"]:
            await ctx.send("Did you mean \"help\"?")
        elif str(error).split("\"")[1] in ["cars"]:
            await ctx.send("Did you mean \"cats\"?")
        else:
            await ctx.send("Uh, that doesn't exist! Use `d.help` if you're confused!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Hm? Is there something you'd like to say, or am I meant to interpret space? Speak up, I don't bite!")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("```fix\n⚠️ Unexpected error! Either use this command with a required argument, or report this as a bug to smudgedpasta.```")
    try:
        raise error
    except:
        print("```py\n" + traceback.format_exc() + "```")


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
For a list of my commands, use the classic command of `d.help`. For a more detailed list of what I can do, visit https://github.com/smudgedpasta/Dottie/blob/master/CommandsList. You can find my source code over there too if you're interested!\n
Thanks for inviting me! 😊"""
    embed.set_author(name=dottie.user.name, url="https://github.com/smudgedpasta/Dottie", icon_url=dottie.user.avatar_url_as(format="png", size=4096))
    embed.set_image(url="https://cdn.discordapp.com/attachments/703579929840844891/740522679697932349/Dottie.gif")

    for channel in ["bots", "dottie", "general", "text", "convo", "chat"]:
        target_channel = discord.utils.get(guild.text_channels, name=channel)
        if target_channel and target_channel.permissions_for(guild.me).send_messages:
            break

    if not target_channel:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                target_channel = channel
                break

    if target_channel:
        await target_channel.send(embed=embed)


dottie.remove_command("help")


def ignore_case(s):
    out = set()
    for z in range(1 << len(s)):
        new = "".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate(s))
        out.add(new)
    return out


@dottie.command()
@has_permissions(administrator=True)
async def purge(ctx, amount=1):
    if amount == 1:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f":broom: swept away **1** message!")
    elif amount > 0:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f":broom: Swept away **{amount}** messages!")
    elif amount < 1:
        await ctx.send(f"How am I meant to purge **{amount}** messages, silly?".format(amount))


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


@dottie.command(aliases=["get_your_butt_in_here", "join"], pass_context=True)
async def connect(ctx):
    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("```ini\n[Successfully joined the Voice Channel! What a cozy place you got here! 😊]```")
    except:
        await ctx.send("Hey, I can't find you! You need to be in a voice channel first!")


@dottie.command(aliases=["go_naughty_step", "leave"], pass_context=True)
async def disconnect(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()
    await ctx.send("```ini\n[Successfully disconnected from the Voice Channel... Sad that it is time to go... 😔]```")


@dottie.command(aliases=["espacito", "Despacito"])
async def despacito(ctx):
  for vc in dottie.voice_clients:
    if vc.guild == ctx.guild:
        vc.play(discord.FFmpegOpusAudio("assets/music/Normal_Despacito.ogg"))
        await ctx.send("***```css\n🥁 Embrace my [DESPACITO!]```***")
        return
  await ctx.send("How are you meant to hear my *100% normal Despacito* from outside of a Voice Channel? Hop in one and use `d.connect` first!")


@dottie.command()
@commands.check(is_owner)
async def load(ctx, extension=None):
    if extension is None:
        await ctx.send("```css\n⚠️[Specify the extension.]⚠️```")
        return
    dottie.load_extension(f"cogs.{extension}")
    await ctx.send("```ini\n[Successfully returned access to the extension.]```")


@dottie.command()
@commands.check(is_owner)
async def unload(ctx, extension=None):
    if extension is None:
        await ctx.send("```css\n⚠️[Specify the extension.]⚠️```")
        return
    dottie.unload_extension(f"cogs.{extension}")
    await ctx.send("```css\n[Successfully removed the extension until further notice.]```")


@dottie.command()
@commands.check(is_owner)
async def reload(ctx, extension=None):
    if extension is None:
        await ctx.send("```css\n⚠️[Specify the extension.]⚠️```")
        return
    dottie.unload_extension(f"cogs.{extension}")
    dottie.load_extension(f"cogs.{extension}")
    await ctx.send("```fix\n[Successfully refreshed the extension.]```")


@dottie.command()
@commands.check(is_owner)
async def shutdown(ctx):
    print("```" + random.choice(["css", "ini", "asciidoc", "fix"]) + "\n[Cancelling all scheduled events and logging out...]```")
    await ctx.send("```css\n[❗ Shutting down...]```")
    for vc in dottie.voice_clients:
        await vc.disconnect(force=True)
    await asyncio.sleep(0.5)
    await ctx.bot.logout()


# 🔻 UNFINISHED COMMANDS/EVENTS 🔻


for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            dottie.load_extension(f"cogs.{filename[:-3]}")


# @dottie.command()
# async def test(ctx, pass_context=True):
#     await ctx.send("<:plus:688316007093370910>")


dottie.run(discord_token)
