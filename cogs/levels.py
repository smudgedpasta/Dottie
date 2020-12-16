from imports import *
from bot import print2


class LEVELS(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie
        dottie.LEVELS = self
        dottie.loop.create_task(self.update_userbase())
        if not os.path.exists("json/leveldata.json"):
            self.users = {}
        else:
            with open("json/leveldata.json", "r") as f:
                self.users = json.load(f)

    async def update_userbase(self):
        await self.dottie.wait_until_ready()
        while not self.dottie.is_closed():
            with open("json/leveldata.json", "w") as f:
                json.dump(self.users, f, indent=4)
            await asyncio.sleep(10)


    def give_exp(self, author_id, exp=1):
        data = self.users.setdefault(author_id, dict(lvl=5, exp=0))
        data["exp"] += 1
        return data["exp"]


    def lvl_up(self, author_id):
        if author_id not in self.users:
            self.users[author_id] = dict(lvl=5, exp=0)
        exp_amount = self.users[author_id]["exp"]
        lvl_amount = self.users[author_id]["lvl"]

        requirement = round((4 * (lvl_amount ** 3)) / 5)
        if exp_amount >= requirement:
            self.users[author_id]["lvl"] += 1
            self.users[author_id]["exp"] -= requirement
            return True
        else:
            return False

    
    async def on_message(self, message):
        if message.author == self.dottie.user:
            return
        author_id = str(message.author.id)
        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]["lvl"] = 5
            self.users[author_id]["exp"] = 0

        self.give_exp(author_id, 1)

        if self.lvl_up(author_id):
            embed = discord.Embed(colour=message.author.colour, timestamp=message.created_at)
            embed.set_author(name=self.dottie.user.name, url="https://github.com/smudgedpasta/Dottie", icon_url=dottie.user.avatar_url_as(format="png", size=4096))
            embed.description = f"What? {message.author.display_name.upper()} is evolving!\nCongratulations! Your local {message.author.display_name.upper()} is now level {self.users[author_id]['lvl']}" + random.choice(["✨", "🤍", "😏", "😊"])
            await message.channel.send(embed=embed)


    @commands.command()
    async def level(self, ctx, aliases=["pokemon, pokémon"]):
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

        if not member_id in self.users:
            embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
            embed.set_author(name=self.dottie.user.name, icon_url=member.avatar_url_as(format="png", size=4096))
            embed.description = "They are still a starter Pokémon, awaiting the start of their journey..."
            embed.set_image(url="https://cdn.discordapp.com/attachments/751513839169831083/788571007757713448/Dragonite.jpg")
            await ctx.send(embed=embed)
        else:
            # await ctx.send(self.users[member_id]["lvl"], self.users[member_id]["exp"])
            embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
            embed.set_author(name=f"{member.name}'s Pokédex entry! ... I mean level.", icon_url=member.avatar_url_as(format="png", size=4096))
            embed.add_field(name="Current level:", value=self.users[member_id]["lvl"])
            embed.add_field(name="Total experience points:", value=self.users[member_id]["exp"])
            embed.set_image(url="https://cdn.discordapp.com/attachments/751513839169831083/788571644104671252/latest.png")
            await ctx.send(embed=embed)


def setup(dottie):
    dottie.add_cog(LEVELS(dottie))