from modules import *

# psutil.Process() is just Task Manager 2.0
TaskManager2 = psutil.Process()

# whoops this is a mess XD
def get_cpu_percent():
    # Creates a list of concurrent.futures Future objects waiting on the cpu usage percentage of all child subprocesses
    futs = [create_future_ex(child.cpu_percent) for child in TaskManager2.children(True)]
    # Gets cpu percentage of the main process
    cpu = TaskManager2.cpu_percent()
    # Adds all the cpu usage percentages together
    cpu += sum(fut.result() for fut in futs)
    return cpu

def get_memory_percent():
    # Works similarly to get_cpu_percent()
    futs = [create_future_ex(child.memory_percent) for child in TaskManager2.children(True)]
    cpu = TaskManager2.memory_percent()
    cpu += sum(fut.result() for fut in futs)
    return cpu

# cpu_percent() of the psutil.Process object needs to be run once before it actually starts working
get_cpu_percent()


class GENERAL(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command()
    async def help(self, ctx):
        page1 = discord.Embed(colour=discord.Colour(15277667), timestamp=ctx.message.created_at)
        page1.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/blob/master/CommandsList", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        page1.description = "*I think I need heeelp, I'm drowning in myseeelf* 🎵"
        page1.set_image(url="https://cdn.discordapp.com/attachments/683233571405561876/746281046231875594/image0.png")
        page1.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text="Click the reactions to scroll through the pages!")

        page2 = discord.Embed(colour=discord.Colour(15277667))
        page2.description = """*I think I need heeelp, I'm drowning in myseeelf* 🎵\n
**:crossed_swords: __MODERATION__ :crossed_swords:**\n
***purge***\n*```Clears inputted message count, not counting the command message.```*\n***kick***\n*```Kicks a user from the server, either by mentioning or stating their username.```*\n***ban***\n*```Bans a user the same way as kick.```*\n***unban***\n*```Unbans a user by typing their username and discriminator. (Example: Dottie#7157)```*\n
**:white_heart: __GENERAL__ :white_heart:**\n
***help***\n*```Legends say you've found this command already. 👀```*\n***ping***\n*```Returns my ping latency.```*\n***profile***\n**```fix\nAliases: userinfo, info, stats, userstats```**\n*```Views the profile of a mentioned user!```*\n
**:french_bread: __FUN__ :french_bread:**\n
***hello***\n**```fix\nAliases: "hemlo", "henlo", "hoi", or any variant of "hello" or "hi"```**\n*```I will greet you back!```*\n***AskDottie***\n**```fix\nAliases: ask, 8ball```**\n*```Ask me anything, I'll give a random answer!```*\n***ab***\n**```fix\nAliases: dab```**\n*```ab will spell out d.ab with my prefix, so I'll dab!```*\n***faker***\n*```Think you can imitate me? I will call you out!```*\n***photo***\n*```Pulls a random image of me!```*\n***nsfw_photo***\n**```css\n[NSFW CHANNEL ONLY]```**\n*```Pulls a random image of me, but be warned, they are gore.```*\n***numberguess***\n**```fix\nAliases: quiz```**\n*```A "guess-the-number" guessing game!```*\n***speak***\n**```fix\nAliases: say```**\n*```Make me say something, anything, and I'll repeat! Nobody will know it was you!```*\n***pyramid***\n*```Tell me to build a pyramid with a height of your choosing!```*\n
**:headphones: __VOICE__ :headphones:**\n
***connect***\n**```fix\nAliases: get_your_butt_in_here, join```**\n*```Connects me to the voice channel you're in!```*\n***disconnect***\n**```fix\nAliases: go_naughty_step, leave```**\n*```Disconnects me from the voice channel I was in!```*\n***despacito***\n**```fix\nAliases: espacito, Despacito```**\n*```Plays a totally normal version of Despacito!```*
 """
        page2.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/blob/master/CommandsList", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        page2.set_footer(text="For a more detailed command list, view the link hidden in the \"🐾 Help List 🌨️\" title! If you find any bugs or have any enquires, be sure to let my creator, smudgedpasta, know!")

        page3 = discord.Embed(colour=discord.Colour(15277667))
        page3.description = """*I think I need heeelp, I'm drowning in myseeelf* 🎵\n
**:crossed_swords: __MODERATION__ :crossed_swords:**\n
``` ```\n
**:white_heart: __GENERAL__ :white_heart:**\n
***avatar***\n**```fix\nAliases: icon```**\n*```Sends an image of yours or someone else's Discord avatar!```*\n
**:french_bread: __FUN__ :french_bread:**\n
***rate***\n*```Give me anything and I'll give it a rating!```*\n***http_cats***\n**```fix\nAliases: cats, http```**\n*```Pulls a random http status code with a funny cat picture and caption!```*\n***dog***\n**```fix\nAliases: og, doggo, puppo```**\n*```Sends a random image of a dog!```*\n
**:headphones: __VOICE__ :headphones:**\n
``` ```\n
"""
        page3.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/blob/master/CommandsList", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        page3.set_footer(text="For a more detailed command list, view the link hidden in the \"🐾 Help List 🌨️\" title! If you find any bugs or have any enquires, be sure to let my creator, smudgedpasta, know!")

        # Creates a list of all pages of the help command
        pages = [page1, page2, page3]

        # Sends the first page when the command is run
        message = await ctx.send(embed=page1)

        # Adds reactions to the message
        await message.add_reaction("🔺")
        await message.add_reaction("🔻")

        # If the author of the command or a bot owner was the one to hit a reaction, it returns True
        def user_check(reaction, user):
            if reaction.message.id == message.id:
                if user.id == ctx.author.id or user.id in OWNERS:
                    return True
                # If the reaction was hit by a server administrator, it also returns True
                guild = reaction.message.guild
                if guild is not None:
                    member = guild.get_member(user.id)
                    if member is not None:
                        if member.guild_permissions.administrator:
                            return True
    
        # Function for editing the message to cycle between the help pages
        async def page_reaction_listener(page, event_type="add"):
            while True:
                react = await self.dottie.wait_for(f"reaction_{event_type}", check=user_check)
                emoji = str(react[0])
                # Depending which reaction was hit, the pages will go next or backwards in the list
                if emoji == "🔺" and page[0] > 0:
                    page[0] -= 1
                    await message.edit(embed=pages[page[0]])
                if emoji == "🔻" and page[0] < len(pages) - 1:
                    page[0] += 1
                    await message.edit(embed=pages[page[0]])
        page = [0]
        # Places two tasks on the asyncio event loop queue, one to check reaction adds, and one to check removals
        create_task(page_reaction_listener(page, "add"))
        create_task(page_reaction_listener(page, "remove"))


    @commands.command()
    async def ping(self, ctx):
        cpu = await create_future(get_cpu_percent)
        memory = await create_future(get_memory_percent)
        # A dictionary of technical statistics
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
    async def profile(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        Roles = member.roles[1:]
        # Strips the first role in a members roles, which is "@@everyone"

        embed = discord.Embed(colour=discord.Colour(15277667), timestamp=ctx.message.created_at)
        if member.id in OWNERS:
            # Creates a special embed author if the member is a bot owner
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
        embed.add_field(name="You stumbled into this server on:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M, %p UTC"))
        if len(Roles) == 0:
            # If the member has no roles, this replaces the values with an empty space
            embed.add_field(name="Here you have earnt these ranks in 0 roles- wait a minute...", value="\u200b")
            embed.add_field(name="... Your highest rank being nothing, obviously. 😔", value="\u200b")
        else:
            embed.add_field(name=f"Here you have earnt these ranks in {len(Roles)} roles! ⚔️", value=" ".join([role.mention for role in Roles]))
            # Top role is the role with the highest level permissions
            embed.add_field(name="... With your highest rank being:", value=member.top_role.mention)

        await ctx.send(embed=embed)


    @commands.command(aliases=["icon"])
    async def avatar(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        # If no member is specified it sends the authors
        embed = discord.Embed(colour=discord.Colour(15277667))
        embed.set_image(url=member.avatar_url_as(format="png", size=4096))
        embed.set_footer(text=f"{member.display_name}'s wonderful icon picture! 👍")
        await ctx.send(embed=embed)


def setup(dottie):
    dottie.add_cog(GENERAL(dottie))
