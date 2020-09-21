import discord
from discord.ext import tasks, commands
import psutil


class GENERAL(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    # NEEDS DEBUGGING 🔻
    @commands.command()
    async def help(self, ctx):
        await ctx.send("```fix\n🖐️ Sorry! This command is currently unavailable.```")
    #     page1 = discord.Embed(colour=discord.Colour(15277667), timestamp=ctx.message.created_at)
    #     page1.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/blob/master/CommandsList", icon_url=dottie.user.avatar_url_as(format="png", size=4096))
    #     page1.description = "*I think I need heeelp, I'm drowning in myseeelf* 🎵"
    #     page1.set_image(url="https://cdn.discordapp.com/attachments/683233571405561876/746281046231875594/image0.png")
    #     page1.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text="Click the reactions to scroll through the pages!")

    #     page2 = discord.Embed(colour=discord.Colour(15277667))
    #     page2.description = """*I think I need heeelp, I'm drowning in myseeelf* 🎵\n
    # **:crossed_swords: __MODERATION__ :crossed_swords:**\n
    # ***purge***\n*```Clears inputted message count, not counting the command message.```*\n***kick***\n*```Kicks a user from the server, either by mentioning or stating their username.```*\n***ban***\n*```Bans a user the same way as kick.```*\n***unban***\n*```Unbans a user by typing their username and discriminator. (Example: Dottie#7157)```*\n
    # **:white_heart: __GENERAL__ :white_heart:**\n
    # ***help***\n*```Legends say you've found this command already. 👀```*\n***ping***\n*```Returns my ping latency.```*\n***profile***\n**```fix\nAliases: userinfo, info, stats, userstats```**\n*```Views the profile of a mentioned user!```*\n
    # **:french_bread: __FUN__ :french_bread:**\n
    # ***hello***\n**```fix\nAliases: "hemlo", "henlo", "hoi", or any variant of "hello" or "hi"```**\n*```I will greet you back!```*\n***AskDottie***\n**```fix\nAliases: ask, 8ball```**\n*```Ask me anything, I'll give a random answer!```*\n***ab***\n**```fix\nAliases: dab```**\n*```ab will spell out d.ab with my prefix, so I'll dab!```*\n***faker***\n*```Think you can imitate me? I will call you out!```*\n***photo***\n*```Pulls a random image of me!```*\n***nsfw_photo***\n**```css\n[NSFW CHANNEL ONLY]```**\n*```Pulls a random image of me, but be warned, they are gore.```*\n***numberguess***\n**```fix\nAliases: quiz```**\n*```A "guess-the-number" guessing game!```*\n***speak***\n**```fix\nAliases: say```**\n*```Make me say something, anything, and I'll repeat! Nobody will know it was you!```*\n***pyramid***\n*```Tell me to build a pyramid with a height of your choosing!```*\n
    # **:headphones: __VOICE__ :headphones:**\n
    # ***connect***\n**```fix\nAliases: get_your_butt_in_here, join```**\n*```Connects me to the voice channel you're in!```*\n***disconnect***\n**```fix\nAliases: go_naughty_step, leave```**\n*```Disconnects me from the voice channel I was in!```*\n***despacito***\n**```fix\nAliases: espacito, Despacito```**\n*```Plays a totally normal version of Despacito!```*
    # """
    #     page2.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/blob/master/CommandsList", icon_url=dottie.user.avatar_url_as(format="png", size=4096))
    #     page2.set_footer(text="For a more detailed command list, view the link hidden in the \"🐾 Help List 🌨️\" title! If you find any bugs or have any enquires, be sure to let my creator, smudgedpasta, know!")

    #     page3 = discord.Embed(colour=discord.Colour(15277667))
    #     page3.description = """*I think I need heeelp, I'm drowning in myseeelf* 🎵\n
    # **:crossed_swords: __MODERATION__ :crossed_swords:**\n
    # ``` ```\n
    # **:white_heart: __GENERAL__ :white_heart:**\n
    # ***avatar***\n**```fix\nAliases: icon```**\n*```Sends an image of yours or someone else's Discord avatar!```*\n
    # **:french_bread: __FUN__ :french_bread:**\n
    # ***rate***\n*```Give me anything and I'll give it a rating!```*\n***http_cats***\n**```fix\nAliases: cats, http```**\n*```Pulls a random http status code with a funny cat picture and caption!```*\n
    # **:headphones: __VOICE__ :headphones:**\n
    # ``` ```\n
    # """
    #     page3.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/blob/master/CommandsList", icon_url=dottie.user.avatar_url_as(format="png", size=4096))
    #     page3.set_footer(text="For a more detailed command list, view the link hidden in the \"🐾 Help List 🌨️\" title! If you find any bugs or have any enquires, be sure to let my creator, smudgedpasta, know!")

    #     pages = [page1, page2, page3]

    #     message = await ctx.send(embed=page1)

    #     await message.add_reaction("🔺")
    #     await message.add_reaction("🔻")

    #     def check(reaction, user): return reaction.message.id == message.id and user.id == ctx.author.id

    #     async def page_reaction_listener(page, event_type="add"):
    #         while True:
    #             react = await dottie.wait_for(f"reaction_{event_type}", check=check)
    #             emoji = str(react[0])
    #             if emoji == "🔺" and page[0] > 0:
    #                 page[0] -= 1
    #                 await message.edit(embed=pages[page[0]])
    #             if emoji == "🔻" and page[0] < len(pages) - 1:
    #                 page[0] += 1
    #                 await message.edit(embed=pages[page[0]])
    #     page = [0]
    #     eloop.create_task(page_reaction_listener(page, "add"))
    #     eloop.create_task(page_reaction_listener(page, "remove"))


    @commands.command()
    async def ping(self, ctx):
        TaskManager2 = psutil.Process()
        await ctx.send(f"""*```css\n{{Ping! I pong back all this nice techy info. 🍺}}\n 
    Current CPU usage is: [{TaskManager2.cpu_percent() / psutil.cpu_count()}%]
    Current memory usage is: [{round(TaskManager2.memory_percent(), 2)}%]
    Ping latency is: [{round(dottie.latency * 1000)}ms]
    ```*""")


def setup(dottie):
    dottie.add_cog(GENERAL(dottie))
