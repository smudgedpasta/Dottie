from imports import *
from bot import print2, on_message


try:
    with open("database/level_disables.txt", "r") as f:
        s = f.read()
except FileNotFoundError:
    s = ""
DISABLED = {int(i) for i in s.splitlines() if i}


class LEVELS(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie
        dottie.LEVELS = self
        dottie.loop.create_task(self.update_userbase())
        if not os.path.exists("database/levelsdata.json"):
            self.users = {}
        else:
            with open("database/levelsdata.json", "r") as f:
                self.users = json.load(f)

    async def update_userbase(self):
        await self.dottie.wait_until_ready()
        while not self.dottie.is_closed():
            with open("database/levelsdata.json", "w") as f:
                json.dump(self.users, f, indent=4)
            await asyncio.sleep(10)


    def give_exp(self, author_id, exp=1):
        data = self.users.setdefault(author_id, dict(lvl=1, exp=0))
        data["exp"] += 1
        return data["exp"]


    def lvl_up(self, author_id):
        if author_id not in self.users:
            self.users[author_id] = dict(lvl=1, exp=0)
        exp_amount = self.users[author_id]["exp"]
        lvl_amount = self.users[author_id]["lvl"]

        requirement = lvl_amount * (lvl_amount + 1) / 2 * 100
        if exp_amount >= requirement:
            self.users[author_id]["lvl"] = int(((2 * exp_amount + 25) ** 0.5 - 5) / 10) + 1
            return True
        else:
            return False


    @commands.command(aliases=["levels_d"])
    @has_permissions(administrator=True)
    async def remove_levels(self, ctx):
        if ctx.guild.id not in DISABLED:
            DISABLED.add(ctx.guild.id)
        with open("database/level_disables.txt", "a") as f:
            f.write(str(ctx.guild.id) + "\n")
            embed = discord.Embed(colour=discord.Colour(65280))
            embed.description = f"```css\nDisabled [{ctx.guild}] from recieving level-up embeds!```"
            await ctx.send(embed=embed)


    @commands.command(aliases=["levels_e"])
    @has_permissions(administrator=True)
    async def enable_levels(self, ctx):
        DISABLED.discard(ctx.guild.id)
        with open("database/level_disables.txt", "w") as f:
            f.write("\n".join(str(i) for i in DISABLED))
            embed = discord.Embed(colour=discord.Colour(65280))
            embed.description = f"```css\nRe-enabled [{ctx.guild}] into recieving level-up embeds!```"
            await ctx.send(embed=embed)

    
    async def on_message(self, message):
        author_id = str(message.author.id)
        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]["lvl"] = 1
            self.users[author_id]["exp"] = 0

        self.give_exp(author_id, 1)

        if self.lvl_up(author_id) and not message.author.bot:
            if message.guild.id not in DISABLED:
                embed = discord.Embed(colour=message.author.colour, timestamp=message.created_at)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/727087981285998593/788705037584564234/Dragonite_Evolution.gif")
                embed.set_author(name=self.dottie.user.name, url="https://github.com/smudgedpasta/Dottie", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
                embed.description = f"What? **{message.author.display_name.upper()}** is evolving!\nCongratulations! Your local **{message.author.display_name.upper()}** is now **level {self.users[author_id]['lvl']}**! " + random.choice(["✨", "🤍", "😏", "😊"])
                embed.set_footer(text="Gif from https://gifer.com/en/BnJ4")
                await message.channel.send(embed=embed)
                await error.add_reaction("❎")


    @commands.command(aliases=["pokemon", "pokémon"])
    async def level(self, ctx):
        spl = ctx.message.content.split(None, 1)
        if len(spl) > 1:
            try:
                member = await self.dottie.find_user(spl[-1], guild=ctx.guild)
            except:
                print2(traceback.format_exc(), end="")
                return await ctx.send(f"I can't find the user \"{spl[-1]}\"! Please specify a more specific identifier such a username#discriminator, or a user ID.")
        else:
            member = ctx.author
        member_id = str(member.id)

        if member_id == str(self.dottie.user.id):
            embed = discord.Embed(colour=discord.Colour(pink_embed), timestamp=ctx.message.created_at)
            embed.set_author(name=self.dottie.user.name, url="https://github.com/smudgedpasta/Dottie", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
            embed.add_field(name="Current level:", value="♾")
            embed.add_field(name="Total experience:", value="♾")
            embed.add_field(name="Next level at:", value="♾")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/751513839169831083/810925500649439302/EPYqEjlXkAA7ldD.png")
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Checked by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        elif not member_id in self.users:
            embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
            embed.set_author(name=self.dottie.user.name, url="https://github.com/smudgedpasta/Dottie", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
            embed.description = f"{member.display_name}'s still a starter Pokémon, awaiting the start of their journey..."
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/751513839169831083/788571007757713448/Dragonite.jpg")
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Checked by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
            embed.set_author(name=f"{member.display_name}'s Pokédex entry- I mean level!", url=member.avatar_url_as(format="png", size=4096), icon_url=member.avatar_url_as(format="png", size=4096))
            embed.add_field(name="Current level:", value=self.users[member_id]["lvl"])
            embed.add_field(name="Total experience:", value=self.users[member_id]["exp"])
            embed.add_field(name="Next level at:", value=round(self.users[member_id]["exp"] / self.users[member_id]["lvl"] + 1))
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/751513839169831083/788571644104671252/latest.png")
            embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Checked by {ctx.author.display_name}")
            await ctx.send(embed=embed)


def setup(dottie):
    dottie.add_cog(LEVELS(dottie))