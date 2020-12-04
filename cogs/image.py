from imports import *


class IMAGE(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command()
    async def photo(self, ctx):
        Image_Pool = None
        with open("json/Image_Pool.json", "r") as f:
            Image_Pool = json.load(f)
            random_image = random.choice(Image_Pool)
            embed = discord.Embed(colour=discord.Colour(15277667))
            embed.description = random_image["desc"]
            embed.set_image(url=random_image["img"])
            embed.set_footer(text=random_image["artist"])
            await ctx.send(embed=embed)


    @commands.command()
    async def nsfw_photo(self, ctx):
        NSFW_Image_Pool = None
        with open("json/NSFW_Image_Pool.json", "r") as f:
            NSFW_Image_Pool = json.load(f)
            random_image = random.choice(NSFW_Image_Pool)
            embed = discord.Embed(colour=discord.Colour(15277667))
            embed.description = random_image["desc"]
            embed.set_image(url=random_image["img"])
            embed.set_footer(text=random_image["artist"])
            if ctx.channel.is_nsfw():
                await ctx.send(embed=embed)
            else:
                await ctx.send("Woah, be careful, this command pulls graphic imagery! Try again in an **nsfw channel**!")

        
    @commands.command(aliases=["cats", "http"])
    async def http_cats(self, ctx, code=None):
        http_cats = None
        with open("json/http_cats.json", "r", encoding="utf-8") as f:
            http_cats = json.load(f)
            for name in http_cats:
                if name["name"] == 404:
                    cat_response = name
            if code is None:
                cat_response = random.choice(http_cats)
            if code is not None:
                code = int(code)
                for name in http_cats:
                    if name["name"] == code:
                        cat_response = name
                        break
            embed_colours = random.choice([1146986, 2067276, 2123412, 7419530, 11342935, 12745742, 11027200, 10038562, 9936031, 5533306])
            embed = discord.Embed(colour=discord.Colour(embed_colours))
            embed.set_footer(text="Images are from https://http.cat/")
            embed.description = cat_response["description"]
            embed.set_image(url=cat_response["image"])
            await ctx.send(embed=embed)


    @commands.command(aliases=["og", "doggo", "puppo"])
    async def dog(self, ctx):
        r = requests.get("https://dog.ceo/api/breeds/image/random")
        data = r.json()
        embed_colours = random.choice([1146986, 2067276, 2123412, 7419530, 11342935, 12745742, 11027200, 10038562, 9936031, 5533306])
        embed = discord.Embed(colour=discord.Colour(embed_colours))
        embed.set_footer(text="Images are from https://dog.ceo/api/breeds/image/random")
        embed.set_image(url=data["message"])
        embed.description = random.choice(["Bärk!", "Börk!", "🐶", "🐕"])
        await ctx.send(embed=embed)

    
    @commands.command(aliases=["marble"])
    async def marble_fox(self, ctx):
        marble_foxes = None
        with open("json/marble_foxes.json", "r") as f:
                dreamstime_imgs = json.load(f)
                marble_foxes = random.choice(dreamstime_imgs)
                embed_colours = random.choice([1146986, 2067276, 2123412, 7419530, 11342935, 12745742, 11027200, 10038562, 9936031, 5533306])
                embed = discord.Embed(colour=discord.Colour(embed_colours))
                embed.set_footer(text="Images are from https://www.dreamstime.com/photos-images/marble-fox.html")
                embed.set_image(url=marble_foxes["image"])
                embed.description = random.choice(["Yip!", "Yap!", "🦊", "<:sleepy_smudgy:762368404069023784>"])
                await ctx.send(embed=embed)


    @commands.command()
    async def fox(self, ctx):
        r = requests.get("https://randomfox.ca/floof/")
        data = r.json()
        embed_colours = random.choice([1146986, 2067276, 2123412, 7419530, 11342935, 12745742, 11027200, 10038562, 9936031, 5533306])
        embed = discord.Embed(colour=discord.Colour(embed_colours))
        embed.set_footer(text="Images are from https://randomfox.ca/")
        embed.set_image(url=data["image"])
        embed.description = random.choice(["Squeak!", "Ring-ding-ding-ding-dingeringeding!", "🦊", "<:sleepy_fox:762367799150510164>"])
        await ctx.send(embed=embed)


def setup(dottie):
    dottie.add_cog(IMAGE(dottie))