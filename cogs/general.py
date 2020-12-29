from imports import *
from bot import print2


# psutil.Process() is just Task Manager 2.0
TaskManager2 = psutil.Process()

def get_cpu_percent():
    futs = [create_future_ex(child.cpu_percent) for child in TaskManager2.children(True)]
    cpu = TaskManager2.cpu_percent()
    cpu += sum(fut.result() for fut in futs)
    return cpu

def get_memory_percent():
    futs = [create_future_ex(child.memory_percent) for child in TaskManager2.children(True)]
    cpu = TaskManager2.memory_percent()
    cpu += sum(fut.result() for fut in futs)
    return cpu

get_cpu_percent()


class GENERAL(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command()
    async def help(self, ctx):
        page1 = discord.Embed(colour=discord.Colour(15277667), timestamp=ctx.message.created_at)
        page1.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        page1.description = "*I think I need heeelp, I'm drowning in myseeelf* 🎵"
        page1.set_image(url="https://cdn.discordapp.com/attachments/683233571405561876/746281046231875594/image0.png")
        page1.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text="Click the reactions to scroll through the pages!")

        page2 = discord.Embed(colour=discord.Colour(15277667))
        page2.description = """*I think I need heeelp, I'm drowning in myseeelf* 🎵\n
**:crossed_swords: __MODERATION__ :crossed_swords:**\n
***remove_levels***\n**```fix\nAliases: levels_d```**\n*```Prevents level-up embeds from posting in the server.```*\n***enable_levels***\n**```fix\nAliases: levels_e```**\n*```If level-up embeds were disabled, this re-enables them.```*\n***purge***\n*```Clears inputted message count, not counting the command message.```*\n
**:white_heart: __GENERAL__ :white_heart:**\n
***help***\n*```Legends say you've found this command already. 👀```*\n***profile***\n**```fix\nAliases: userinfo, info, stats, userstats```**\n*```Views the profile of a provided user!```*\n***level***\n**```fix\nAliases: pokémon, pokemon```**\n*```Shows the current level and experience of a provided user!```*\n
**:french_bread: __FUN__ :french_bread:**\n
***hello***\n**```fix\nAliases: "hemlo", "hoi"```**\n*```I will greet you back!```*\n***AskDottie***\n**```fix\nAliases: ask, 8ball```**\n*```Ask me anything, I'll give a random answer!```*\n***rate***\n*```Give me anything and I'll give it a rating!```*\n
**:frame_photo: __IMAGE__ :frame_photo:**\n
***photo***\n*```Pulls a random image of me!```*\n***nsfw_photo***\n**```css\n[NSFW CHANNEL ONLY]```**\n*```Pulls a random image of me, but be warned, they are gore.```*\n***art***\n*```Takes the most recent image in a channel and only states the truth!```*\n
**:headphones: __VOICE__ :headphones:**\n
***connect***\n**```fix\nAliases: get_your_butt_in_here, join```**\n*```Connects me to the voice channel you're in!```*\n***disconnect***\n**```fix\nAliases: go_naughty_step, leave```**\n*```Disconnects me from the voice channel I was in!```*\n***despacito***\n**```fix\nAliases: espacito```**\n*```Plays a totally normal version of Despacito!```*\n
**:people_hugging: __MENTAL HEALTH__ :people_hugging:**\n
```json\n"No commands yet of this category!"```\n
 """
        page2.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        page2.set_footer(text="Commands are NOT case sensitive. For a more detailed command list, view the link hidden in the \"🐾 Help List 🌨️\" title! If you find any bugs or have any enquires, be sure to let my creator, smudgedpasta, know!")

        page3 = discord.Embed(colour=discord.Colour(15277667))
        page3.description = f"""*I think I need heeelp, I'm drowning in myseeelf* 🎵\n
**:crossed_swords: __MODERATION__ :crossed_swords:**\n
***ban***\n*```Bans a user the same way as kick.```*\n***unban***\n*```Unbans a user by typing their username and discriminator. (Example: Dottie#7157)```*\n***kick***\n*```Kicks a user from the server, either by mentioning or stating their username.```*\n
**:white_heart: __GENERAL__ :white_heart:**\n
***avatar***\n**```fix\nAliases: icon```**\n*```Sends an image of yours or someone else's Discord avatar!```*\n***random***\n*```Takes all arguments you've provided and chooses one at random!```*\n***loop***\n*```Repeats an inputted command a specified amount of times! Example: {PREFIX}loop 5 {PREFIX}hello```*\n
**:french_bread: __FUN__ :french_bread:**\n
***matchmaking***\n**```fix\nAliases: ship, love```**\n*```Ship two people/characters of your choosing!```*\n***numberguess***\n**```fix\nAliases: quiz```**\n*```A "guess-the-number" guessing game!```*\n***speak***\n**```fix\nAliases: say```**\n*```Make me say something, anything, and I'll repeat! Nobody will know it was you!```*\n
**:frame_photo: __IMAGE__ :frame_photo:**\n
***http_cats***\n**```fix\nAliases: cats, http```**\n*```Pulls a http status code with a funny cat picture and command_related caption!```*\n***marble_fox***\n**```fix\nAliases: marble```**\n*```Sends a random image of a marble fox!```*\n***dog***\n**```fix\nAliases: og, doggo, puppo```**\n*```Sends a random image of a dog!```*\n
**:headphones: __VOICE__ :headphones:**\n
```json\n"Whoops, no further commands yet!"```\n
**:people_hugging: __MENTAL HEALTH__ :people_hugging:**\n
```json\n"No commands yet of this category!"```\n
"""
        page3.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        page3.set_footer(text="Commands are NOT case sensitive. For a more detailed command list, view the link hidden in the \"🐾 Help List 🌨️\" title! If you find any bugs or have any enquires, be sure to let my creator, smudgedpasta, know!")

        page4 = discord.Embed(colour=discord.Colour(15277667))
        page4.description = """*I think I need heeelp, I'm drowning in myseeelf* 🎵\n
**:crossed_swords: __MODERATION__ :crossed_swords:**\n
```json\n"Whoops, no further commands yet!"```\n
**:white_heart: __GENERAL__ :white_heart:**\n
***ping***\n*```Returns some technical information.```*\n
**:french_bread: __FUN__ :french_bread:**\n
***heart***\n*```Use this with two emojis, and I'll make them a heart!```*\n***pyramid***\n*```Tell me to build a pyramid with a height of your choosing!```*\n***ab***\n**```fix\nAliases: dab```**\n*```ab will spell out d.ab with my prefix, so I'll dab!```*\n***faker***\n*```Think you can imitate me? I will call you out!```*\n
**:frame_photo: __IMAGE__ :frame_photo:**\n
***fox***\n*```Sends a random image of any kind of fox!```*\n
**:headphones: __VOICE__ :headphones:**\n
```json\n"Whoops, no further commands yet!"```\n
**:people_hugging: __MENTAL HEALTH__ :people_hugging:**\n
```json\n"No commands yet of this category!"```\n
"""
        page4.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        page4.set_footer(text="Commands are NOT case sensitive. For a more detailed command list, view the link hidden in the \"🐾 Help List 🌨️\" title! If you find any bugs or have any enquires, be sure to let my creator, smudgedpasta, know!")

        pages = [page1, page2, page3, page4]

        message = await ctx.send(embed=page1)

        await message.add_reaction("🔺")
        await message.add_reaction("🔻")

        def user_check(reaction, user):
            if reaction.message.id == message.id:
                if user.id == ctx.author.id or user.id in OWNERS:
                    return True
                if user.id != self.dottie.user.id:
                    guild = reaction.message.guild
                    if guild is not None:
                        member = guild.get_member(user.id)
                        if member is not None:
                            if member.guild_permissions.administrator:
                                return True
    
        async def page_reaction_listener(page, event_type="add"):
            while True:
                react = await self.dottie.wait_for(f"reaction_{event_type}", check=user_check)
                emoji = str(react[0])
                if emoji == "🔺" and page[0] > 0:
                    page[0] -= 1
                    await message.edit(embed=pages[page[0]])
                if emoji == "🔻" and page[0] < len(pages) - 1:
                    page[0] += 1
                    await message.edit(embed=pages[page[0]])
        page = [0]
        create_task(page_reaction_listener(page, "add"))
        create_task(page_reaction_listener(page, "remove"))


    @commands.command()
    async def loop(self, ctx):
        message = ctx.message
        content = message.content
        _, count, command = content.split(None, 2)
        fake_message = copy.copy(message)
        fake_message.content = command
        for i in range(int(count)):
            new_ctx = await self.dottie.get_context(fake_message)
            await self.dottie.invoke(new_ctx)


    @commands.command(aliases=["link", "invite"])
    async def source(self, ctx):
        embed = discord.Embed(colour=discord.Colour(15277667))
        embed.description = """[My GitHub](https://github.com/smudgedpasta/Dottie)\n[My Invite](https://discord.com/api/oauth2/authorize?client_id=737992099449929728&permissions=8&scope=bot)"""
        embed.set_author(name=self.dottie.user.name, icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/751513839169831083/793587710391746590/768px-Python-logo-notext.png")
        await ctx.send(embed=embed)


    @commands.command()
    async def ping(self, ctx):
        cpu = await create_future(get_cpu_percent)
        memory = await create_future(get_memory_percent)
        TechyInfo = {
            "CPU": f"[{cpu / psutil.cpu_count()}%]",
            "Memory": f"[{round(memory, 2)}%]",
            "Ping": f"[{round(self.dottie.latency * 1000)}ms]"
        }
        
        embed = discord.Embed(colour=discord.Colour(15277667))
        embed.set_author(name=self.dottie.user.name, url="https://github.com/smudgedpasta/Dottie", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        embed.description = "*```asciidoc\n[Ping! I pong back all this nice techy info. 🍺]```*"
        embed.add_field(name="CPU Usage", value="```ini\n" + str(TechyInfo["CPU"]) + "```")
        embed.add_field(name="Memory Usage", value="```ini\n" + str(TechyInfo["Memory"]) + "```")
        embed.add_field(name="Ping Latency", value="```ini\n"+ str(TechyInfo["Ping"]) + "```")

        await ctx.send(embed=embed)
    

    @commands.command(aliases=["userinfo", "info", "stats", "userstats"])
    async def profile(self, ctx):
        spl = ctx.message.content.split(None, 1)
        if len(spl) > 1:
            try:
                member = await self.dottie.find_user(spl[-1], guild=ctx.guild)
            except:
                print(traceback.format_exc(), end="")
                return await ctx.send(f"I can't find the user \"{spl[-1]}\"! Please specify a more specific identifier such a username#discriminator, or a user ID.")
        else:
            member = ctx.author
        try:
            Roles = member.roles[1:]
        except AttributeError:
            Roles = None

        embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
        if member.id in OWNERS:
            embed.set_author(name=f"Hey there my owner, {member.name}! Let's see your info! 🤍")
        else:
            embed.set_author(name=f"Snap! Let's see your info, {member.name}! 👀")
        embed.set_thumbnail(url=member.avatar_url_as(format="png", size=4096))
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Command run by {ctx.author.display_name}")

        embed.description = "```ini\n🤍 Here they like to call you [" + member.display_name + "], what a nice nickname! 🤍```"

        embed.add_field(name="Too lazy for developer mode? Here's the ID:", value=str(member.id) + " ✌️")
        embed.add_field(name="You fell into Discord addiction on:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M, %p UTC"))
        if member.bot == True:
            embed.add_field(name="CAPTCHA TEST, are you a robot?", value="True! You failed the test, you robot! 🤖")
        else:
            embed.add_field(name="CAPTCHA TEST, are you a robot?", value="False! I'll let this one slide, mortal. <:squint:760051294668193832>")
        if getattr(member, "joined_at", None):
            embed.add_field(name="You stumbled into this server on:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M, %p UTC"))
        if Roles is not None:
            if len(Roles) == 0:
                embed.add_field(name="Here you have earnt these ranks in 0 roles- wait a minute...", value="\u200b")
                embed.add_field(name="... Your highest rank being nothing, obviously. 😔", value="\u200b")
            else:
                embed.add_field(name=f"Here you have earnt these ranks in {len(Roles)} roles! ⚔️", value=" ".join([role.mention for role in Roles]))
                embed.add_field(name="... With your highest rank being:", value=member.top_role.mention)

        await ctx.send(embed=embed)


    @commands.command(aliases=["icon"])
    async def avatar(self, ctx):
        spl = ctx.message.content.split(None, 1)
        if len(spl) > 1:
            try:
                member = await self.dottie.find_user(spl[-1], guild=ctx.guild)
            except:
                print2(traceback.format_exc(), end="")
                return await ctx.send(f"I can't find the user \"{spl[-1]}\"! Please specify a more specific identifier such a username#discriminator, or a user ID.")
        else:
            member = ctx.author
        embed = discord.Embed(colour=member.colour)
        embed.set_image(url=member.avatar_url_as(format="png", size=4096))
        embed.set_footer(text=f"{member.display_name}'s wonderful icon picture! 👍")
        await ctx.send(embed=embed)


    @commands.command()
    async def random(self, ctx, *args):
        embed = discord.Embed(colour=discord.Colour(15277667), timestamp=ctx.message.created_at)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Randomized by {ctx.author.display_name}")
        embed.description = f"```ini\n🎉 [{random.choice(args)}] 🎉```"
        await ctx.send("🥁 ***Your random selection is...***", embed=embed)
        

def setup(dottie):
    dottie.add_cog(GENERAL(dottie))
