from imports import *


class OWNER(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie

    
    # This was just a debug command, its fairly useless now
    @commands.command(aliases=["check", "cogs"])
    @commands.check(is_owner)
    async def cogs_check(self, ctx):
        await ctx.send("```json\n\"🎉 COGS ARE OPERATIONAL. 🎉\"```")


    @commands.command()
    @commands.check(is_owner)
    async def big_pyramid(self, ctx):
        await ctx.send(":muscle: Y'know what I'm in the mood for? Building a **big** pyramid! How tall should it be, my trusted owner?")
        message = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        size = (int(message.content))
        if size >= 11:
            # Even bot owners can be a bit ambitious 🙃
            await ctx.send(f"OK, I trust you {ctx.author.display_name}, but that's a bit *too* much! :sweat_drops:")
        elif size <= -1:
            await ctx.send(f"C'mon {ctx.author.display_name}, even you know Discord has no shovels. :upside_down:")
        elif size == 0:
            if message.author.id == 530781444742578188:
                await ctx.send("Haha very funny, I would be sad if you weren't the one to code this monstrosity. <:smudgedead:712902348984549437>")
            if message.author.id == 201548633244565504:
                await ctx.send("Haha very funny, I would be sad if you weren't the one to code this monstrosity. <:txindead:712902347512217610>")
            # Simply checks if its either Smudge or Txin running the command and uses the appropriate emoji
        else:
            for i in range(size):
                await ctx.send(("<:empty" + ":760062353063936000>") * (size-i-1) + ":orange_square:" + (":blue_square::orange_square:") * i)
                # Sends a bigger variant of the pyramid in an alternating pattern


    @commands.command()
    async def big_heart(self, ctx, arg1, arg2):
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
                "0": "<:_" + ":760062353063936000>",
                "1": f"{arg1}",
                "2": f"{arg2}"
                }

        trans = "".maketrans(emoji)
        for line in heart:
            await ctx.send(line.translate(trans)) 


    @commands.command()
    @commands.check(is_owner)
    async def restart(self, ctx):
        await ctx.send("```css\n[❗ Restarting...]```")
        for vc in self.dottie.voice_clients:
            await vc.disconnect(force=True)
            # Forces Dottie to leave VC if they're currently in one
        os.system("start cmd /c python bot.py")
        psutil.Process().kill()
        # Mimics the .bat, opens the program again and closes the current one


    @commands.command()
    @commands.check(is_owner)
    async def shutdown(self, ctx):
        print("```" + random.choice(["css", "ini", "asciidoc", "fix"]) + "\n[Cancelling all scheduled events and logging out...]```")
        await ctx.send("```css\n[❗ Shutting down...]```")
        for vc in self.dottie.voice_clients:
            await vc.disconnect(force=True)
        await asyncio.sleep(0.5)
        # Has the shutdown process sleep briefly so there's time for the message to send and log to the log channel
        await ctx.bot.logout()

    
    # Just some code for my Discord Server's rules 🙃
    @commands.command()
    @commands.check(is_owner)
    async def rules(self, ctx):
        embed = discord.Embed(colour=discord.Colour(15277667))
        embed.set_author(name=self.dottie.get_user(530781444742578188).name, url="https://github.com/smudgedpasta/Dottie", icon_url=self.dottie.get_user(530781444742578188).avatar_url_as(format="png", size=4096))
        embed.description = """***```ini\n🗒️ [SERVER RULES!] 🗒️```***
*```fix\n🔸 RULE ONE```*
*What the <@&677928041183182890>'s say, goes.*

The server admins may not have their roles displayed at the side, but there will always be indicators of who they are. The server admins currently are <@530781444742578188> and <@201548633244565504>, who are marked by the roles <@&668062248907964417> and <@&723119556301815818>. 
If you are asked to stop behaving a certain way, you are expected to listen.

*```fix\n🔸 RULE TWO```*
*Do not hate on other people's interests.*

This can range from music taste to opinions on "ships" regarding a fandom. You can have friendly debates on why you disagree, this server is not built to silence your opinion. But when it gets into the territory of discriminating against users/insulting them of their interests, the line is drawn.
People should be allowed to feel safe to express their opinion, and I don't want anyone feeling like they're walking on eggshells. 

*```fix\n🔸 RULE THREE```*
*Absolutely no discrimination towards sexuality, religion and culture/background.*

Similarly to rule two, users should be free to express themselves, only this is taken more seriously. If you have  negative opinions on certain sexualities, cultures, countries, backgrounds, and more of the like, kindly keep it to yourself. Discrimination or insults to others based on these factors will absolutely not be tolerated, `it does not define them.`
"""
        embed2 = discord.Embed(colour=discord.Colour(15277667))
        embed2.description = """*```fix\n🔸 RULE FOUR```*
*No ||pornographic/heavily suggestive|| imagery, artwork or music.*

The odd occasional sexual reference is fine, but full blown conversation, imagery or other forms of media regarding sex/nudity/porn is strictly forbidden. Not only is it inconsiderate to the minor members of the server, `it is against Discord TOS.`
There is no NSFW channel as I myself am currently a minor and wouldn't be able to view it.

*```fix\n🔸 RULE FIVE```*
*Do not critique other users unless they ask for it.*

If users have not requested or discussed critique (especially in <#668071671063773204>, <#734115770488848414>, <#668072914284707880>, <#668072832525271050> and <#668072372833878026>) then do not give them critique, as sometimes it is not appreciated or could play with a users insecurities.
<#668097481468280832> plays as the channel for asking critique on any creative subject. If you critique a user, make sure you're constructive and offer real helpful criticism, and aren't just being blunt and unkind.

```In a nutshell, the rules can be defined as being respectful to other users. I may come across as strict, but the server is open to everyone, so don't feel like you can't be yourself.```
"""
        
        embed2.set_footer(text="Concerned or confused about anything? @ in #questions-and-feedback or DM a Server Admin")

        await self.dottie.get_channel(668061258007969802).send("https://cdn.discordapp.com/attachments/668061258007969802/723157201903943730/Untitled163.png")
        await self.dottie.get_channel(668061258007969802).send(embed=embed)
        await self.dottie.get_channel(668061258007969802).send(embed=embed2)

        await ctx.send("Rules successfully added!")
    

def setup(dottie):
    dottie.add_cog(OWNER(dottie))
