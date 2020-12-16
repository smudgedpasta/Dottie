from imports import *


class LEVELS(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    self.dottie.loop.create_task(self.save_userbase())


    with open("json/leveldata.json", "r") as f:
        self.users = json.load(f)

    async def update_userbase(self):
        await self.dottie.wait_until_ready()
        while not self.dottie.is_closed():
            with open("json/leveldata.json", "w") as f:
                json.dump(self.users, f, indent=4)


    def lvl_up(self, author_id):
        exp_amount = self.users[author_id]["exp"]
        lvl_amount = self.users[author_id]["lvl"]

        if exp_amount >= round((4 * (exp_amount ** 3)) / 5):
            self.users[author_id]["lvl"] += 1
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

        self.users[author_id]["exp"] += 1

        if self.lvl_up(author_id):
            embed = discord.Embed(colour=discord.Colour(15277667), timestamp=ctx.message.created_at)
            embed.set_author(name=self.dottie.user.name, url="https://github.com/smudgedpasta/Dottie", icon_url=dottie.user.avatar_url_as(format="png", size=4096))
            embed.description = f"What? {message.author.display_name.upper()} is evolving!\nCongratulations! Your local {message.author.display_name.upper()} is now level {self.users[author_id]['lvl']}" + random.choice(["✨", "🤍", "😏", "😊"])
            await ctx.send(embed=embed)


    @commands.command()
    async def level(self, ctx, member: discord.Member = None, aliases=["pokemon, pokémon"]):
        member = ctx.author if not member else member
        author_id = str(member.id)

        if not member_id in self.users:
            embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
            embed.description = "They are still a starter Pokémon, awaiting the start of their journey..."
            embed.set_image(url="https://cdn.discordapp.com/attachments/751513839169831083/788571007757713448/Dragonite.jpg")
            await ctx.send(embed=embed)
        else:
            # await ctx.send(self.users[member_id]["lvl"], self.users[member_id]["exp"])
            embed = discord.Embed(colour=member.colour(15277667), timestamp=ctx.message.created_at)

            embed.set_image(url="https://cdn.discordapp.com/attachments/751513839169831083/788571644104671252/latest.png")


def setup(dottie):
    dottie.add_cog(LEVELS(dottie))