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
            embed = discord.Embed(colour=discord.Colour(pink_embed))
            embed.description = random_image["desc"]
            embed.set_image(url=random_image["img"])
            embed.set_footer(text="Art by " + random_image["artist"])
            await ctx.send(embed=embed)


    @commands.command()
    async def nsfw_photo(self, ctx):
        NSFW_Image_Pool = None
        with open("json/NSFW_Image_Pool.json", "r") as f:
            NSFW_Image_Pool = json.load(f)
            random_image = random.choice(NSFW_Image_Pool)
            embed = discord.Embed(colour=discord.Colour(pink_embed))
            embed.description = random_image["desc"]
            embed.set_image(url=random_image["img"])
            embed.set_footer(text="Art by " + random_image["artist"])
            if ctx.channel.is_nsfw():
                await ctx.send(embed=embed)
            else:
                await ctx.send("Woah, be careful, this command pulls graphic imagery! Try again in an **nsfw channel**!")


    @commands.command()
    async def art(self, ctx):
        async for message in ctx.channel.history(limit=None):
            if message.attachments:
                embed = discord.Embed(colour=discord.Colour(pink_embed))
                embed.description = "𝒴𝑜𝓊 𝓌𝒶𝓃𝓃𝒶 𝓈𝑒𝑒 𝑔𝓇𝑒𝒶𝓉 𝒶𝓇𝓉?\n𝒮𝓊𝓇𝑒, 𝓉𝒽𝑒𝓇𝑒'𝓈 𝓈𝑜𝓂𝑒 𝓪𝓶𝓪𝔃𝓲𝓷𝓰 𝒶𝓇𝓉 𝓇𝒾𝑔𝒽𝓉 𝒽𝑒𝓇𝑒! :blush:"
                embed.set_footer(text=f"Art by {message.author.name}")
                embed.set_image(url=message.attachments[0].proxy_url)
                await ctx.send(embed=embed)
                break

        
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
            embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds))
            embed.set_footer(text="Images are from https://http.cat/")
            embed.description = cat_response["description"]
            embed.set_image(url=cat_response["image"])
            await ctx.send(embed=embed)

        
    @commands.command(aliases=["inspirobot", "inspiration"])
    async def inspiro(self, ctx):
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds))
        embed.set_footer(text="Images are from https://inspirobot.me/")
        quote = inspirobot.generate()
        embed.set_image(url=quote.url)
        await ctx.send(embed=embed)


    @commands.command(aliases=["og", "doggo", "puppo"])
    async def dog(self, ctx):
        r = requests.get("https://dog.ceo/api/breeds/image/random")
        data = r.json()
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds))
        embed.set_footer(text="Images are from https://dog.ceo/api/breeds/image/random")
        embed.set_image(url=data["message"])
        embed.description = random.choice(["Bärk!", "Börk!", "🐶", "🐕", "<:sleepydottie:799210814841421835>"])
        await ctx.send(embed=embed)

    
    @commands.command(aliases=["marble"])
    async def marble_fox(self, ctx):
        marble_foxes = None
        with open("json/marble_foxes.json", "r") as f:
                dreamstime_imgs = json.load(f)
                marble_foxes = random.choice(dreamstime_imgs)
                embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds))
                embed.set_footer(text="Images are from https://www.dreamstime.com/photos-images/marble-fox.html")
                embed.set_image(url=marble_foxes["image"])
                embed.description = random.choice(["Yip!", "Yap!", "🦊", "<:sleepysmudgy:799210361692749824>"])
                await ctx.send(embed=embed)


    @commands.command()
    async def fox(self, ctx):
        r = requests.get("https://randomfox.ca/floof/")
        data = r.json()
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds))
        embed.set_footer(text="Images are from https://randomfox.ca/")
        embed.set_image(url=data["image"])
        embed.description = random.choice(["Squeak!", "Ring-ding-ding-ding-dingeringeding!", "🦊", "<:sleepy_fox:762367799150510164>"])
        await ctx.send(embed=embed)


    @commands.command(aliases=["muffins"])
    async def muffin(self, ctx):
        def get_random_page():
            html = requests.get(f"https://www.gettyimages.co.uk/photos/muffin?page={random.randint(1, 100)}").text
            url = "https://media.gettyimages.com/photos/"
            spl = html.split(url)[1:]
            imageset = {url + i.split('"', 1)[0].split("?", 1)[0] for i in spl}
            images = list(imageset)
            return images
        images = get_random_page()
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds))
        embed.set_footer(text="Images are from https://www.gettyimages.co.uk/photos/")
        embed.set_image(url=random.choice(images))
        embed.description = random.choice(["Its muffin time!", "Muffin!!! 🤗", "🧁", "🧁🧁🧁"])
        await ctx.send(embed=embed)
 
    
    @commands.command(aliases=["dab"])
    async def ab(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/688253918890688521/739424083556696104/unknown.gif")


    @commands.command()
    async def how(self, ctx):
        await ctx.send("https://imgur.com/gallery/8cfRt")


def setup(dottie):
    dottie.add_cog(IMAGE(dottie))