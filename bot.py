#!/usr/bin/python3


from imports import *


discord_token = None
with open("config.json", "r") as f:
    data = json.load(f)
    discord_token = data["token"]


intents = discord.Intents.default()
intents.members = True

dottie = commands.Bot(
    command_prefix=PREFIX,
    case_insensitive=True,
    intents=intents
)


miza_commands = requests.get("http://27.33.133.250:9801/static/help.json").json()
miza_voice = []
for name, command in miza_commands["VOICE"].items():
    miza_voice.extend((name.lower(),) + tuple(alias.lower() for alias in command["aliases"]))


LISTENER = None


def input(*args, **kwargs):
    global LISTENER
    print(*args, **kwargs)
    LISTENER = dottie
    t = time.time()
    while LISTENER is dottie and time.time() - t < 86400:
        time.sleep(0.2)
    return LISTENER


_print = print
def print(*args, sep=" ", end="\n"):
    with open("log", "a", encoding="utf-8") as f:
        f.write(str(sep).join(str(i) for i in args) + end)

    embed = discord.Embed(colour=discord.Colour(15277667))
    embed.description = "```" + random.choice(["css", "ini"]) + "\n" + str(sep).join(str(i) for i in args) + end + "```"

    for c_id in LOG_CHANNELS:
        create_task(dottie.get_channel(c_id).send(embed=embed))

    return _print(*args)


def print2(*args, sep=" ", end="\n"):
    embed = discord.Embed(colour=discord.Colour(15277667))
    embed.description = "```py\n" + str(sep).join(str(i) for i in args) + end + "```"

    for c_id in LOG_CHANNELS:
        create_task(dottie.get_channel(c_id).send(embed=embed))

    return _print(*args)


dottie.eloop = eloop


MESSAGES = {}


async def procFunc(proc):
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


async def status_update_loop():
    global LAST_COMMAND_TIMESTAMP
    while LAST_COMMAND_TIMESTAMP > -inf:
        if time.time() - LAST_COMMAND_TIMESTAMP > 20:
            await dottie.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="over " + str(len(dottie.guilds)) + " servers! 🐾"))
            LAST_COMMAND_TIMESTAMP = inf
        await asyncio.sleep(0.5)


messages = 0


@dottie.event
async def on_message(message):
    if message.author.id == 244652405944221699:
        return
    LEVELS = getattr(dottie, "LEVELS", None)
    if LEVELS:
        try:
            await LEVELS.on_message(message)
        except:
            print2(traceback.format_exc(), end="")
    ctx = await dottie.get_context(message)

    if dottie.user in message.mentions:
        responses = [
            f"Hi, {message.author.display_name}! My prefix is `" + PREFIX[0] + "` so if you're looking for my commands, use `" + PREFIX[0] + "help`!",
            f"What's up, {message.author.display_name}, aka... \"{message.author.name}\"? :smirk: If you need help, use `" + PREFIX[0] + "help`!",
            f"Aaah I've been pinged! How could you do this to me, {message.author.mention}?!",
            f"Hello, {message.author.display_name}! I appreciate you wanting to speak to me! Use `" + PREFIX[0] + "help` if you're interested!",
            f"Here, decode this, {message.author.display_name}... `64 51 77 34 77 39 57 67 58 63 51` :smirk:",
            f"WOAH YES HI I'M UP, need me for something, {message.author.display_name}? :eyes:",
            f"{message.author.display_name}, you are a wonderful person, and I hope you are having a good day. :blush:",
            f"You are loved and worth it, {message.author.display_name}... Never forget that. :white_heart:",
            f"Hiya, {message.author.display_name}! Need me for something? My prefix is `" + PREFIX[0] + "` so to see my commands, use `" + PREFIX[0] + "help`!",
            f"Heheh, I can do that too! {message.author.mention} :smiling_imp:",
            f"My creator is questioning why she is spending time writing this feature... UH, I MEAN, I HAVE MY OWN INTELLIGENCE, WHAT'S UP {message.author.display_name.upper()}?!",
            f"Hey, {message.author.display_name}, you should talk to my best friend <@668999031359537205>, she's great! :blush:",
            "Hi there! I'm an experimental Discord bot created by ||~~the cuddly bugs~~|| <@530781444742578188> and <@201548633244565504>! My mission is to be something positive. :white_heart:"
        ]

        await ctx.send(random.choice(responses))
        try:
            print(f"[{message.author.name}] mentioned me in [{message.guild}]")
        except:
            print(f"[{message.author.name}] mentioned me in [DM's]")

    global messages
    messages += 1
    ctx = await dottie.get_context(message)

    await dottie.invoke(ctx)

    Smudge = [530781444742578188, 668064931345596439]
    if message.author.id in Smudge and message.content.endswith("#"):
        if set(message.content) == {"#"}:
            return
        else:
            await ctx.send("Smudge Keyboard Moment <a:moment:750685242553139321>")

    if ctx.command is not None:
        if getattr(message.author, "guild", None) is None:
            print(f"[{message.author.name}] has run the following command: [{message.content}] in [Direct Messages]")
        else:
            print(f"[{message.author.name}] has run the following command: [{message.content}] in [{message.guild}]")

        global LISTENER
        global LAST_COMMAND_TIMESTAMP
        if LAST_COMMAND_TIMESTAMP > time.time():
            await dottie.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="whoever summoned me! 👀"))
            LAST_COMMAND_TIMESTAMP = time.time()

    elif getattr(message.channel, "guild", None) is None and message.author != dottie.user:
        channel = message.channel
        if ctx.command is None:
            embed = discord.Embed(colour=discord.Colour(197379), timestamp=ctx.message.created_at)
            embed.set_author(name=f"Incoming DM from {message.author}!", icon_url="https://cdn.discordapp.com/attachments/751513839169831083/757326045450862754/DM_Thumbnail.png")
            embed.set_thumbnail(url=ctx.author.avatar_url_as(format="png", size=4096))
            embed.description = f"{message.content}"
            embed.set_footer(text=f"User ID: {ctx.author.id}")
            for ID in DM_CHANNEL:
                create_task(dottie.get_channel(ID).send(embed=embed))
            
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
                        output = await procFunc(proc)
                        await channel.send("```\n" + str(output)[:1993] + "```")
                    except:
                        error = await channel.send("```py\n" + traceback.format_exc()[:1991] + "```")
                        await error.add_reaction("❎")
      
eloop.create_task(status_update_loop())


@dottie.event
async def on_ready():
    await dottie.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="over " + str(len(dottie.guilds)) + " servers! 🐾"))
    GLOBALS["eloop"] = asyncio.get_event_loop()
    print(f"Logged in as user [{dottie.user}] [(ID = {dottie.user.id})]")
    print("[Successfully loaded and ready to go!]\n")


async def log_update():
    await dottie.wait_until_ready()
    global messages
    start_time = time.time()
    interval_time = time.time()
    current_day = str(datetime.datetime.utcnow().date())
    while not dottie.is_closed():
        try:
            GLOBALS["eloop"] = asyncio.get_event_loop()
            uptime = datetime.timedelta(seconds=time.time() - start_time)
            interval = time.time() - interval_time
            new_day = str(datetime.datetime.utcnow().date())
            if new_day != current_day:
                current_day = new_day
                print(f"🔸 Time at log interval: [{datetime.datetime.utcnow().strftime('%a, %#d %B, %I:%M %p')}]\n🔹 Current uptime: [{str(uptime).rsplit('.', 1)[0]}]\n🔸 Messages sent within [{interval // 3600}] hour interval: [{messages}]".format())
                messages = 0
                interval_time = time.time()
        except Exception as e:
            print(e)
        await asyncio.sleep(1)

dottie.loop.create_task(log_update())


@dottie.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("You don't have permissions to use that command, you lil' delinquent!")
    if isinstance(error, commands.CommandNotFound):
        if str(error).split("\"", 2)[1].lower() in list(miza_voice) + ["np"]:
            global LAST_COMMAND_TIMESTAMP
            command = PREFIX[0] + str(error).split("\"", 2)[1].lower()
            print(f"[{ctx.author.name}] has run the following command: [{command}] in [{ctx.guild}]")
            await dottie.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="whoever summoned me! 👀"))
            LAST_COMMAND_TIMESTAMP = time.time()
            return
        if str(error).split("\"")[1] in ["hepl", "hepk", "hlep", "hekp", "pleh"]:
            await ctx.send("Did you mean \"help\"?")
        elif str(error).split("\"")[1] in ["cars", "cat"]:
            await ctx.send("Did you mean \"cats\"?")
        elif str(error).split("\"")[1] in ["levels"]:
            await ctx.send("Did you mean \"level\"?")
        elif str(error).split("\"")[1] in ["pign"]:
            await ctx.send("Did you mean \"ping\"? ~~I hate to break it to you but I'm not a Minecraft Piglin...~~")
        else:
            await ctx.send("Uh, that doesn't exist! Use `" + PREFIX[0] + "help` if you're confused!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Hm? Is there something you'd like to say, or am I meant to interpret space? Speak up, I don't bite!")
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(colour=discord.Colour(16776960))
        embed.description = "```fix\n⚠️ Unexpected error! Either use this command with a required argument, or report this as a bug to smudgedpasta. ⚠️```"
        await ctx.send(embed=embed)
    try:
        raise error
    except:
        print2(traceback.format_exc(), end="")


@dottie.event
async def on_member_join(member):
    print(f"[{member}] has joined [{member.guild}]")

@dottie.event
async def on_member_remove(member):
    print(f"[{member}] has left [{member.guild}]")


@dottie.event
async def on_guild_join(guild):
    target_channel = None

    embed = discord.Embed(colour=discord.Colour(15277667))
    embed.description = f"""Hi! I'm {dottie.user.name}, a test project by <@530781444742578188>- with the help of <@201548633244565504> and <@245890903133257730> of course! :white_heart:\n
For a list of my commands, use the classic command of `""" + PREFIX[0] + """help`. For a more detailed list of what I can do, visit https://github.com/smudgedpasta/Dottie/wiki. You can find my source code over there too if you're interested!\n
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


@dottie.command(aliases=["exec_e"])
@commands.check(is_owner)
async def exec_add(ctx):
    if ctx.message.channel.id not in TERMINALS:
        TERMINALS.add(ctx.message.channel.id)
        with open("database/terminal_channels", "a") as f:
            f.write("\n" + str(ctx.message.channel.id))
    embed = discord.Embed(colour=discord.Colour(65280))
    embed.description = f"```css\nAdded [#{ctx.message.channel}] to the list of terminals!```"
    await ctx.send(embed=embed)


@dottie.command(aliases=["exec_d"])
@commands.check(is_owner)
async def exec_remove(ctx):
    TERMINALS.discard(ctx.message.channel.id)
    with open("database/terminal_channels", "w") as f:
        f.write("\n".join(str(i) for i in TERMINALS))
    embed = discord.Embed(colour=discord.Colour(65280))
    embed.description = f"```css\nRemoved [#{ctx.message.channel}] from the list of terminals!```"
    await ctx.send(embed=embed)


@dottie.command(aliases=["dm_e"])
@commands.check(is_owner)
async def dm_add(ctx):
    if ctx.message.channel.id not in DM_CHANNEL:
        DM_CHANNEL.add(ctx.message.channel.id)
        with open("database/DM_channels", "a") as f:
            f.write("\n" + str(ctx.message.channel.id))
    embed = discord.Embed(colour=discord.Colour(65280))
    embed.description = f"```css\n[#{ctx.message.channel}] will now log DM's!```"
    await ctx.send(embed=embed)


@dottie.command(aliases=["dm_d"])
@commands.check(is_owner)
async def dm_remove(ctx):
    DM_CHANNEL.discard(ctx.message.channel.id)
    with open("database/DM_channels", "w") as f:
        f.write("\n".join(str(i) for i in DM_CHANNEL))
    embed = discord.Embed(colour=discord.Colour(65280))
    embed.description = f"```css\n[#{ctx.message.channel}] will no longer log DM's!```"
    await ctx.send(embed=embed)


@dottie.command(aliases=["log_e"])
@commands.check(is_owner)
async def log_add(ctx):
    if ctx.message.channel.id not in LOG_CHANNELS:
        LOG_CHANNELS.add(ctx.message.channel.id)
        with open("database/log_channels", "a") as f:
            f.write("\n" + str(ctx.message.channel.id))
    embed = discord.Embed(colour=discord.Colour(65280))
    embed.description = f"```css\n[#{ctx.message.channel}] will now recieve developer logs!```"
    await ctx.send(embed=embed)


@dottie.command(aliases=["log_d"])
@commands.check(is_owner)
async def log_remove(ctx):
    LOG_CHANNELS.discard(ctx.message.channel.id)
    with open("database/log_channels", "w") as f:
        f.write("\n".join(str(i) for i in LOG_CHANNELS))
    embed = discord.Embed(colour=discord.Colour(65280))
    embed.description = f"```css\n[#{ctx.message.channel}] will no longer recieve developer logs!```"
    await ctx.send(embed=embed)


@dottie.command()
@commands.check(is_owner)
async def load(ctx, extension=None):
    if extension is None:

        start_miza()
        for cog in ["moderation", "general", "fun", "levels", "image", "voice", "owner", "CTE"]:
            dottie.load_extension(f"cogs.{cog}")
        embed = discord.Embed(colour=discord.Colour(255))
        embed.description = "```fix\n[Successfully returned acces to all extensions.]```"
        await ctx.send(embed=embed)
        return

    dottie.load_extension(f"cogs.{extension}")
    if extension == "voice":
        start_miza()
    embed = discord.Embed(colour=discord.Colour(255))
    embed.description = f"```ini\n[Successfully returned access to category \"{extension.upper()}\".]```"
    await ctx.send(embed=embed)


@dottie.command()
@commands.check(is_owner)
async def unload(ctx, extension=None):
    if extension is None:

        stop_miza()
        for cog in ["moderation", "general", "fun", "levels", "image", "voice", "owner", "CTE"]:
            dottie.unload_extension(f"cogs.{cog}")
        embed = discord.Embed(colour=discord.Colour(16711680))
        embed.description = "```asciidoc\n[Successfully removed all extensions until further notice.]```"
        await ctx.send(embed=embed)
        return

    dottie.unload_extension(f"cogs.{extension}")
    if extension == "voice":
        stop_miza()
    embed = discord.Embed(colour=discord.Colour(16711680))
    embed.description = f"```asciidoc\n[Successfully removed category \"{extension.upper()}\" until further notice.]```"
    await ctx.send(embed=embed)


@dottie.command()
@commands.check(is_owner)
async def reload(ctx, extension=None):
    if extension is None:
        
        stop_miza()
        start_miza()
        for cog in ["moderation", "general", "fun", "levels", "image", "voice", "owner", "CTE"]:
            dottie.unload_extension(f"cogs.{cog}")
            dottie.load_extension(f"cogs.{cog}")
        embed = discord.Embed(colour=discord.Colour(16776960))
        embed.description = "```fix\n[Successfully refreshed all extensions.]```"
        await ctx.send(embed=embed)
        return

    dottie.unload_extension(f"cogs.{extension}")
    dottie.load_extension(f"cogs.{extension}")
    if extension == "voice":
        stop_miza()
        start_miza()
    embed = discord.Embed(colour=discord.Colour(16776960))
    embed.description = f"```fix\n[Successfully refreshed category \"{extension.upper()}\".]```"
    await ctx.send(embed=embed)


async def find_user(query, guild=None):
    if query.startswith("<@") and query.endswith(">"):
        q = query[2:-1].lstrip("!")
        if q.isnumeric():
            query = q
    if query.isnumeric():
        u_id = int(query)
        if guild:
            user = guild.get_member(u_id)
            if user is not None:
                return user
        user = dottie.get_user(u_id)
        if user is not None:
            return user
        try:
            user = await dottie.fetch_user(u_id)
        except (discord.NotFound, discord.Forbidden):
            pass
        else:
            dottie._connection._users[user.id] = user
            return user
    if "#" in query and query.rsplit("#", 1)[-1].isnumeric():
        for user in dottie._connection._users.values():
            if str(user) == query:
                if guild:
                    member = guild.get_member(user.id)
                    if member is not None:
                        return member
                return user
    if guild:
        for user in guild.members:
            if user.name == query or user.nick == query:
                return user
    if guild:
        if len(guild.members) < 2:
            member = await guild.query_members(query, limit=1)
            return member[0]
        lower_query = query.casefold()
        found = set()
        for user in guild.members:
            if user.name.casefold().startswith(lower_query):
                found.add((len(user.name), user))
            if user.nick and user.nick.casefold().startswith(lower_query):
                found.add((len(user.nick), user))
        if found:
            return sorted(found, key=lambda t: t[0])[0][1]
    raise LookupError(f"No results for {query}.")


dottie.find_user = find_user

glob = dict(GLOBALS)
glob.update(globals())


if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            dottie.load_extension(f"cogs.{filename[:-3]}")
    start_miza()
    dottie.run(discord_token)
