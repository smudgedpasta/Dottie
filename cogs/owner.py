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
        os.system("start cmd /k python bot.py")
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


def setup(dottie):
    dottie.add_cog(OWNER(dottie))
