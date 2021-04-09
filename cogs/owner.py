from imports import *


class OWNER(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command()
    @commands.check(is_owner)
    async def big_pyramid(self, ctx):
        await ctx.send(":muscle: Y'know what I'm in the mood for? Building a **big** pyramid! How tall should it be, my trusted owner?")
        message = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        size = (int(message.content))
        if size >= 11:
            await ctx.send(f"OK, I trust you {ctx.author.display_name}, but that's a bit *too* much! :sweat_drops:")
        elif size <= -1:
            await ctx.send(f"C'mon {ctx.author.display_name}, even you know Discord has no shovels. :upside_down:")
        elif size == 0:
            if message.author.id == 530781444742578188:
                await ctx.send("Haha very funny, I would be sad if you weren't the one to code this monstrosity. <:smudgedead:712902348984549437>")
            if message.author.id == 201548633244565504:
                await ctx.send("Haha very funny, I would be sad if you weren't the one to code this monstrosity. <:txindead:712902347512217610>")
        else:
            for i in range(size):
                await ctx.send(("<:empty" + ":760062353063936000>") * (size-i-1) + ":orange_square:" + (":blue_square::orange_square:") * i)


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


    @commands.command(aliases=["exec_e"])
    @commands.check(is_owner)
    async def exec_add(self, ctx):
        if ctx.message.channel.id not in TERMINALS:
            TERMINALS.add(ctx.message.channel.id)
            with open("database/terminal_channels.txt", "a") as f:
                f.write("\n" + str(ctx.message.channel.id))
        await ctx.send(f"`Added #{ctx.message.channel} to the list of terminals!`")


    @commands.command(aliases=["exec_d"])
    @commands.check(is_owner)
    async def exec_remove(self, ctx):
        TERMINALS.discard(ctx.message.channel.id)
        with open("database/terminal_channels.txt", "w") as f:
            f.write("\n".join(str(i) for i in TERMINALS))
        await ctx.send(f"`Removed #{ctx.message.channel} from the list of terminals!`")


    @commands.command(aliases=["dm_e"])
    @commands.check(is_owner)
    async def dm_add(self, ctx):
        if ctx.message.channel.id not in DM_CHANNEL:
            DM_CHANNEL.add(ctx.message.channel.id)
            with open("database/DM_channels.txt", "a") as f:
                f.write("\n" + str(ctx.message.channel.id))
        await ctx.send(f"`#{ctx.message.channel} will now log DM's!`")


    @commands.command(aliases=["dm_d"])
    @commands.check(is_owner)
    async def dm_remove(self, ctx):
        DM_CHANNEL.discard(ctx.message.channel.id)
        with open("database/DM_channels.txt", "w") as f:
            f.write("\n".join(str(i) for i in DM_CHANNEL))
        await ctx.send(f"`#{ctx.message.channel} will no longer log DM's!`")


    @commands.command(aliases=["log_e"])
    @commands.check(is_owner)
    async def log_add(self, ctx):
        if ctx.message.channel.id not in LOG_CHANNELS:
            LOG_CHANNELS.add(ctx.message.channel.id)
            with open("database/log_channels.txt", "a") as f:
                f.write("\n" + str(ctx.message.channel.id))
        await ctx.send(f"`#{ctx.message.channel} will now recieve developer logs!`")


    @commands.command(aliases=["log_d"])
    @commands.check(is_owner)
    async def log_remove(self, ctx):
        LOG_CHANNELS.discard(ctx.message.channel.id)
        with open("database/log_channels.txt", "w") as f:
            f.write("\n".join(str(i) for i in LOG_CHANNELS))
        await ctx.send(f"`#{ctx.message.channel} will no longer recieve developer logs!`")


    @commands.command()
    @commands.check(is_owner)
    async def restart(self, ctx):
        await ctx.send("❗ `Restarting...`")
        await self.dottie.change_presence(status=discord.Status.invisible)
        for vc in self.dottie.voice_clients:
            await vc.disconnect(force=True)
        os.system("start cmd /c python bot.py")
        try:
            stop_miza()
        except:
            return
        psutil.Process().kill()


    @commands.command()
    @commands.check(is_owner)
    async def shutdown(self, ctx):
        with open("log", "w") as f:
            f.write("Refreshed log...\n\n")
        await ctx.send("❗ `Shutting down...`")
        await self.dottie.change_presence(status=discord.Status.invisible)
        for vc in self.dottie.voice_clients:
            await vc.disconnect(force=True)
        await asyncio.sleep(5)
        try:
            stop_miza()
        except:
            return
        psutil.Process().kill()
    

def setup(dottie):
    dottie.add_cog(OWNER(dottie))
