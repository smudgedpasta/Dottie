from imports import *


class FUN(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


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

        answer = [
            "So you asked...",
            "You'd like to know...",
            "Hi there, you asked me...",
            "Hm...",
            ""
        ]

        question = question.replace("?", "")
        question = question.replace("yourself", "myself")
        question = question.replace("your", "my")
        question = question.replace("you", "I")
        question = question.replace("are", "am")

        for i in ("~~", "***", "**", "*", "||", "__", "```", "'"):
            if question.startswith(i) and question.endswith(i):
                await ctx.send(f"{i}{random.choice(answer)} {question[len(i):-len(i)]}? {random.choice(responses)}{i}")
                return

        await ctx.send(f"{random.choice(answer)} {question}? {random.choice(responses)}")


    @commands.command()
    async def faker(self, ctx):
        member = ctx.author
        for role in member.roles:
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


    @commands.command(aliases=["quiz"])
    async def numberguess(self, ctx):
        await ctx.send("I am thinking of a number between 1 and 100... Can you guess what it is?")
        answer = random.randint(1, 100)
        attempts = 10
        try:
            for i in range(attempts):
                response = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                number = int(response.content)
                if number == answer:
                    await ctx.send(f"Bingo! This took you **{i + 1} attempts**! You now get a cheesecake. 🧀🍰")
                    return
                elif i >= attempts - 1:
                    await ctx.send("🛑 Sorry, you ran out of chances! Try again any time!")
                    return
                elif number > answer:
                    await ctx.send("Your guess was **too high**! Try again!")
                elif number < answer:
                    await ctx.send("Your guess was **too low**! Try again!")
        except:
            await ctx.send("Yo, I ain't that smart! Please use **integers** written in **numbers**!")


    @commands.command(aliases=["chachaslide", "ccs"])
    async def cha_cha_slide(self, ctx):
        lyrics = """We're going to get funky...
To the left!
Take it back now y'all
One hop this time!
Right foot let's stomp
Left foot let's stomp
Cha cha real smooth
Yeah, yeah, do that stuff, do it!
Ah yeah, I'm outta here y'all.
Peace!
""".splitlines()

        await ctx.send(lyrics[0])
        time.sleep(1)
        error_message = "Boo, that's not how the lyrics go!"

        await ctx.send(f"Sing it with me now. {lyrics[1]}")
        next1 = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        next1.content = next1.content.capitalize().replace("!", "").replace("?", "").replace(".", "")
        if next1.content.replace("yall", "y'all").replace("ya'll", "y'all") == lyrics[2]:
            await ctx.send(lyrics[3])
        else:
            await ctx.send(error_message)
            return
        next2 = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        next2.content = next2.content.capitalize().replace("!", "").replace("?", "").replace(".", "")
        if next2.content.replace("lets", "let's") == lyrics[4]:
            await ctx.send(lyrics[5])
        else:
            await ctx.send(error_message)
            return
        next3 = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        if next3.content.capitalize().replace("!", "").replace("?", "").replace(".", "") == lyrics[6]:
            await ctx.send(lyrics[7])
            time.sleep(1)
            await ctx.send(lyrics[8])
            time.sleep(1)
            await ctx.send(lyrics[9])
        else:
            await ctx.send("C'mon, we were so close!")
         

    @commands.command(Aliases=["rockpaperscissors", "rock_paper_scissors"])
    async def rps(self, ctx):
        try:
            await ctx.send("Lets play Rock, Paper, Scissors! Post your choice!")
            response = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

            matches = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
            decision = random.choice(list(matches.keys()))
            await ctx.send(f"I'll go with {decision}!")

            if response.content.lower() not in matches.keys():
                await ctx.send("We- Hold on a minute, you didn't even respond with an answer! <:colondead:751543407494823956>")
            if matches[decision] == response.content.lower():
                await ctx.send("I win! Mwahaha! :grin:")
            if matches[response.content.lower()] == decision:
                await ctx.send("Aw, I lost... Wanna' rematch? :pensive:")
                response2 = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                if "no" in response2.content.lower() or "nope" in response2.content.lower() or "nah" in response2.content.lower():
                    await ctx.send(":cry:")
                    return
            if response.content.lower() == decision:
                await ctx.send("Wow, we tied! Great minds thing alike. :smirk:")
        except:
            return


    @commands.command(aliases=["say"], speach=None)
    async def speak(self, ctx, *, speach):
        try:
            await ctx.message.delete()
        except:
            pass
        if "@everyone" in ctx.message.content:
            if "`" not in ctx.message.content:
                speach = speach.replace("@everyone", "@- `Oh no you don't!`")
            else:
                speach = speach.replace("@everyone", "@- Oh no you don't!")
        if "@here" in ctx.message.content:
            if "`" not in ctx.message.content:
                speach = speach.replace("@here", "@- `Nope!`")
            else:
                speach = speach.replace("@here", "@- Nope!")

        speach = speach.replace("<@&", "<@&\u200b")

        if ctx.author.id in OWNERS:
            await ctx.send(f"{speach}")
        else:
            await ctx.send(f"\u200b {speach}")


    @commands.command()
    async def pyramid(self, ctx):
        await ctx.send(":desert: Y'know what I'm in the mood for? Building a pyramid! How tall should it be?")
        try:
            message = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            size = (int(message.content))
            if size >= 26:
                await ctx.send("Yeah no, let's not go *too* spammy! :sweat_drops:")
            elif size <= -1:
                await ctx.send("Oi, quit try'na break the universe, I can't exactly dig underground on Discord! :upside_down:")
            elif size == 0:
                await ctx.send("Uh, okay, guess I'll go build elsewhere... :pensive:")
            else:
                for i in range(size):
                    await ctx.send("\u200b" + ("<:empty" + ":760062353063936000>") * (size-i-1) + ("<:empty" + ":760062353063936000>" + ":orange_square:") * (i+1))
        except:
            await ctx.send("Yo, I ain't that smart! Please use **integers** written in **numbers**!")


    @commands.command(input=None)
    async def rate(self, ctx, *, input):
        random.seed(input)
        rate = random.randint(0, 10)
        embed = discord.Embed(colour=discord.Colour(pink_embed), timestamp=ctx.message.created_at)
        embed.description = f"**{input.capitalize()}**, hmm? I rate that a **{rate}/10**! " + random.choice(["✨", "🤍", "😏", "😊"])
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)


    @commands.command()
    async def heart(self, ctx, arg1, arg2):
        heart = [
            "00111011100",
            "01222122210",
            "12222222221",
            "12222222221",
            "12222222221",
            "01222222210",
            "00122222100",
            "00012221000",
            "00001210000",
            "00000100000"
        ]

        emoji = {
            "0": "<:_:760062353063936000>",
            "1": arg1,
            "2": arg2
        }

        trans = "".maketrans(emoji)
        for line in heart:
            await ctx.send("\u200b" + line.translate(trans))     


    @commands.command(aliases=["ship", "love"])
    async def matchmaking(self, ctx, arg, arg2):
        heart_list = ["❤️", "🧡", "💛", "💚", "💙", "💜", "💗", "💞", "🤍", "🖤", "🤎", "❣️", "💕", "💖"]

        if arg.startswith("<@" or "<@!"):
            numbers = []
            for i in split(arg):
                if i.isdigit():
                    numbers.append(int(i))
                    arg = dottie.get_user("".join(map(str, numbers)).name)

        if arg2.startswith("<@" or "<@!"):
            numbers2 = []
            for i in split(arg2):
                if i.isdigit():
                    numbers2.append(int(i))
                    arg2 = dottie.get_user("".join(map(str, numbers2)).name)

        arg = arg.capitalize().replace("'", "").replace("`", "")
        arg2 = arg2.capitalize().replace("'", "").replace("`", "")
        arg, arg2 = sorted((arg, arg2))

        random.seed((arg, arg2))
        percentage = random.randint(0, 100)

        start = len(arg) / 2
        end = len(arg2) / 2
        ship_beg = arg[:-int(start)]
        ship_beg2 = arg2[:-int(end)]
        ship_tail = arg[-int(start):]
        ship_tail2 = arg2[-int(end):]
        ship_start = random.choice([ship_beg, ship_tail])
        ship_end = random.choice([ship_beg2, ship_tail2])
        random.seed((ship_start, ship_end))
        shipname = ship_start + ship_end

        random.seed(time.time())
        heart = random.choice(heart_list)

        bar = create_progress_bar(21, percentage / 100)

        embed = discord.Embed(colour=discord.Colour(pink_embed), timestamp=ctx.message.created_at)
        suspicious_function = lambda x: x / ((x ** 2 * 6254793562032913) // (7632048114126314 * 10 ** 24) - (x * 5638138161912547) // 2939758 + 1000000155240420236976462021787648)
        suspicious_function_2 = lambda x: int.from_bytes(bytes.fromhex(x.encode("utf-8").hex()), "little")
        if round(suspicious_function(suspicious_function_2(arg + arg2))) in (13264547, 47787122) and suspicious_function(suspicious_function_2(arg2 + arg)) in (5.869437322867208e-09, 1.0000614609767725e-08):
            inwards_heart = [
                "00111011100",
                "01122122110",
                "01223232210",
                "01234543210",
                "00123432100",
                "00012321000",
                "00001210000",
                "00000100000",
            ]
            emoji = {
                "0": "▪",
                "1": "<a:_" + ":797359273914138625>",
                "2": "<a:_" + ":797359354314620939>",
                "3": "<a:_" + ":797359351509549056>",
                "4": "<a:_" + ":797359341157482496>",
                "5": "<:_" + ":722354192995450912>"
            }
            e_calc = lambda x: (x * 15062629995394936) // 7155909327645687 - (x ** 2 * 3014475045596449) // (2062550437214859 * 10 ** 18) - 53
            e2 = self.dottie.get_emoji(e_calc(ctx.guild.id))
            if e2:
                emoji["5"] = f"<:_:{e2.id}>"

            trans = "".maketrans(emoji)
            rainbow_heart = "\n".join(inwards_heart).translate(trans)
            embed.description = f"```" + random.choice(["css", "ini"]) + f"\n[{arg}] ♡ [{arg2}] ({shipname.capitalize()})❔ 𝓣𝓱𝓮𝔂 𝓼𝓬𝓸𝓻𝓮 𝓪𝓷 [𝓲𝓷𝓯𝓲𝓷𝓲𝓽𝓮%]❕ 💜```" + rainbow_heart
        else:
            if arg == arg2:
                embed.description = f"```" + random.choice(["css", "ini"]) + f"\n[{arg}] ♡ [{arg2}]❔ 𝒯𝒽𝑒𝓎 [{percentage}%] 𝓁𝑜𝓋𝑒 𝓉𝒽𝑒𝓂𝓈𝑒𝓁𝓋𝑒𝓈❕ " + random.choice(["🙃", "🤍", "🥺", "🍿"]) + "```" + bar
            else:
                embed.description = f"```" + random.choice(["css", "ini"]) + f"\n[{arg}] ♡ [{arg2}] ({shipname.capitalize()})❔ 𝓣𝓱𝓮𝔂 𝓼𝓬𝓸𝓻𝓮 𝓪 [{percentage}%]❕ " + random.choice(["✨", "🤍", "😏", "😊"]) + "```" + bar
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Shipped by {ctx.author.display_name} 🤍")
        await ctx.send(f"{heart}" + " ***MATCHMAKING*** " + f"{heart}", embed=embed)


def setup(dottie):
    dottie.add_cog(FUN(dottie))
