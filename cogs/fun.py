from modules import *


class FUN(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command(aliases=["hi", "HI", "Hi", "hI", "hemlo", "henlo", "hoi"] + ["".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate("hello")) for z in range(1, 32)])
    # Finds every possible case variation in "hello"
    async def hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.display_name}! :wave:")


    @commands.command(aliases=["8ball", "ask"], question=None)
    async def AskDottie(self, ctx, *, question):
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
            "Ay, ask me later, I'm busy with my 10 hour tunez! :headphones:"
        ]

        # Replaces words of personal address to sound like a legitimate response, and replaces "?" with an empty string
        question = question.replace("?", "")
        question = question.replace("yourself", "myself")
        question = question.replace("your", "my")
        question = question.replace("you", "I")
        question = question.replace("are", "am")

        # ~~YandereDev moment~~ I mean, copies the authors text formatting | this would actually be a fun challenge to optimize XD
        if question.startswith("~~") or question.endswith("~~"):
            await ctx.send(f"~~So you asked... {question[2:-2]}? {random.choice(responses)}~~")
        elif question.startswith("***") or question.endswith("***"):
            await ctx.send(f"***So you asked... {question[3:-3]}? {random.choice(responses)}***")
        elif question.startswith("**") or question.endswith("**"):
            await ctx.send(f"**So you asked... {question[2:-2]}? {random.choice(responses)}**")
        elif question.startswith("*") or question.endswith("*"):
            await ctx.send(f"*So you asked... {question[1:-1]}? {random.choice(responses)}*")
        elif question.startswith("||") or question.endswith("||"):
            await ctx.send(f"||So you asked... {question[2:-2]}? {random.choice(responses)}||")
        elif question.startswith("__") or question.endswith("__"):
            await ctx.send(f"__So you asked... {question[2:-2]}? {random.choice(responses)}__")
        elif question.startswith("```") or question.endswith("```"):
            await ctx.send(f"```So you asked... {question[3:-3]}? {random.choice(responses)}```")
        elif question.startswith("`") or question.endswith("`"):
            await ctx.send(f"`So you asked... {question[1:-1]}? {random.choice(responses)}`")
        else:
            await ctx.send(f"So you asked... {question}? {random.choice(responses)}")


    @commands.command(aliases=["dab"])
    async def ab(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/688253918890688521/739424083556696104/unknown.gif")


    @commands.command()
    async def faker(self, ctx):
        member = ctx.author
        for role in member.roles:
            # "dottie" is 6 characters long, so since you have upper/lower case, there are 2 possibilities for each, making 2^6 total outcomes (64)
            if role.name in ["".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate("dottie")) for z in range(64)]:
                await ctx.send("What, you think I wouldn't notice you have a **role** of my name? *There can only be one!* :crossed_swords:")
                break
            if member.nick in ["".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate("dottie")) for z in range(64)]:
                await ctx.send("What, you think I wouldn't notice you have a **nickname** of my name? *There can only be one!* :crossed_swords:")
                break
            elif member.name in ["".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate("dottie")) for z in range(64)]: 
                await ctx.send("What, you think I wouldn't notice you have a **username** of my name? *There can only be one!* :crossed_swords:")
                break
        else:
            await ctx.send("Hmm, you don't seem to be mimicking me... For now. I have my eye on you. :eye:")


    @commands.command()
    async def photo(self, ctx):
        Image_Pool = None
        with open("bot/Image_Pool.json", "r") as f:
            Image_Pool = json.load(f)
            # Chooses a random segment of the image pool json
            random_image = random.choice(Image_Pool)
            embed = discord.Embed(colour=discord.Colour(15277667))
            embed.description = random_image["desc"]
            embed.set_image(url=random_image["img"])
            embed.set_footer(text=random_image["artist"])
            await ctx.send(embed=embed)


    @commands.command()
    async def nsfw_photo(self, ctx):
        NSFW_Image_Pool = None
        with open("bot/NSFW_Image_Pool.json", "r") as f:
            NSFW_Image_Pool = json.load(f)
            random_image = random.choice(NSFW_Image_Pool)
            embed = discord.Embed(colour=discord.Colour(15277667))
            embed.description = random_image["desc"]
            embed.set_image(url=random_image["img"])
            embed.set_footer(text=random_image["artist"])
            if ctx.channel.is_nsfw():
                await ctx.send(embed=embed)
            else:
                await ctx.send("Woah, be careful, this command pulls graphic imagery! Try again in an **nsfw channel**!")
                # Obviously wouldn't want this command being run outside of an NSFW marked channel 🙃


    @commands.command(aliases=["quiz"])
    async def numberguess(self, ctx):
        await ctx.send("I am thinking of a number between 1 and 100... Can you guess what it is?")
        answer = random.randint(1, 100)
        attempts = 10
        # Assigns 10 chances
        for i in range(attempts):
            response = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            # Waits for the next message sent by the author of the command, and repeats until they get it correct
            number = int(response.content)
            if number == answer:
                await ctx.send(f"Bingo! This took you {i + 1} attempts! You now get a cheesecake. 🧀🍰")
                return
            elif i >= attempts - 1:
                await ctx.send("🛑 Sorry, you ran out of chances! Try again any time!")
                return
            elif number > answer:
                await ctx.send("Your guess was **too high**! Try again!")
            elif number < answer:
                await ctx.send("Your guess was **too low**! Try again!")


    @commands.command(aliases=["say"], speach=None)
    async def speak(self, ctx, *, speach):
        await ctx.message.delete()
        if "@everyone" in ctx.message.content:
            if "`" not in ctx.message.content:
                speach = speach.replace("@everyone", "@- `Oh no you don't!`")
            else:
                speach = speach.replace("@everyone", "@- Oh no you don't!")
        # As Dottie generally requires admin perms, this eliminates users from being able to use @everyone or @here
        if "@here" in ctx.message.content:
            if "`" not in ctx.message.content:
                 speach = speach.replace("@here", "@- `Nope!`")
            else:
                speach = speach.replace("@here", "@- Nope!")
        await ctx.send(f"{speach}")


    @commands.command()
    async def pyramid(self, ctx):
        await ctx.send(":desert: Y'know what I'm in the mood for? Building a pyramid! How tall should it be?")
        message = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        size = (int(message.content))
        if size >= 26:
            # This checks if the argument is greater than or equal to 26, setting the highest limit as 25
            await ctx.send("Yeah no, let's not go *too* spammy! :sweat_drops:")
        elif size <= -1:
            await ctx.send("Oi, quit try'na break the universe, I can't exactly dig underground on Discord! :upside_down:")
        elif size == 0:
            await ctx.send("Uh, okay, guess I'll go build elsewhere... :pensive:")
        else:
            for i in range(size):
                await ctx.send("\u200b" + ("<:empty" + ":760062353063936000>") * (size-i-1) + ("<:empty" + ":760062353063936000>" + ":orange_square:") * (i+1))
                # Sends a repeated amount of messages, adding on one "🟧" until the specified argument has been reached, including empty emojis to allow for a a triangular formation


    @commands.command(input=None)
    async def rate(self, ctx, *, input):
        random.seed(input)
        rate = random.randint(0, 10)
        embed = discord.Embed(colour=discord.Colour(15277667), timestamp=ctx.message.created_at)
        embed.description = f"**{input}**, hmm? I rate that a **{rate}/10**! " + random.choice(["✨", "🤍", "😏", "😊"])
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)


    # Note to self: allow a lookup for certain http codes
    @commands.command(aliases=["cats", "http"])
    async def http_cats(self, ctx):
        http_cats = None
        with open("bot/http_cats.json", "r", encoding="utf-8") as f:
            # Encoding UTF-8 allows for unicode emojis to be parsed in json.load()
            http_cats = json.load(f)
            cat_response = random.choice(http_cats)
            embed_colours = random.choice([1146986, 2067276, 2123412, 7419530, 11342935, 12745742, 11027200, 10038562, 9936031, 5533306])
            embed = discord.Embed(colour=discord.Colour(embed_colours))
            embed.set_footer(text="Images are from https://http.cat/")
            embed.description = cat_response["description"]
            embed.set_image(url=cat_response["image"])
            await ctx.send(embed=embed)


    @commands.command(aliases=["og", "doggo", "puppo"])
    async def dog(self, ctx):
        r = requests.get("https://dog.ceo/api/breeds/image/random")
        # Gets the raw HTTP response
        data = r.json()
        embed_colours = random.choice([1146986, 2067276, 2123412, 7419530, 11342935, 12745742, 11027200, 10038562, 9936031, 5533306])
        embed = discord.Embed(colour=discord.Colour(embed_colours))
        embed.set_image(url=data["message"])
        # If the HTTP request has succeeded, the JSON would create two parametres, the one in which we need is "message"
        embed.description = random.choice(["Bärk!", "Börk!", "🐶", "🐕"])
        await ctx.send(embed=embed)


def setup(dottie):
    dottie.add_cog(FUN(dottie))
