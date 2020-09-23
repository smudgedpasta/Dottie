from modules import *


def is_owner(ctx):
    return ctx.message.author.id in [530781444742578188, 201548633244565504]


class OWNER(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie

    
    @commands.command(aliases=["check", "cogs"])
    @commands.check(is_owner)
    async def cogs_check(self, ctx):
        await ctx.send("```json\n\"🎉 COGS ARE OPERATIONAL. 🎉\"```")


    @commands.command()
    @commands.check(is_owner)
    async def shutdown(self, ctx):
        print("```" + random.choice(["css", "ini", "asciidoc", "fix"]) + "\n[Cancelling all scheduled events and logging out...]```")
        await ctx.send("```css\n[❗ Shutting down...]```")
        for vc in self.dottie.voice_clients:
            await vc.disconnect(force=True)
        await asyncio.sleep(0.5)
        await ctx.bot.logout()


def setup(dottie):
    dottie.add_cog(OWNER(dottie))
