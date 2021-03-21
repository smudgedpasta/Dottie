from imports import *


class IMAGE(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    hug_source = "https://cdn.discordapp.com/attachments/687567100767633432/814812448678739968/unknown.gif"
    hug_frames = []
    @commands.command(aliases=["nuzzle", "cuddle"])
    async def hug(self, ctx, url=None):
        output_size = (440, 356)
        pos = (183, 161)
        diameter = 103
        caption = "Your image"
        if not url:
            if ctx.message.attachments:
                url = ctx.message.attachments[0].url
            else:
                url = ctx.author.avatar_url
                caption = ctx.author.name
        else:
            if url.isnumeric():
                u_ids = (url,)
            else:
                u_ids = re.findall("<@!?([0-9]+)>", url)
            if u_ids:
                u_id = int(u_ids[0])
                user = self.dottie.get_user(u_id)
                if user is None:
                    user = await self.dottie.fetch_user(u_id)
                url = user.avatar_url
                caption = user.display_name
        url = str(url).strip("<>")
        resp = await create_future(requests.get, url, _timeout_=12)
        resp.raise_for_status()
        b = io.BytesIO(resp.content)
        img = Image.open(b)
        if not self.hug_frames:
            resp = await create_future(requests.get, self.hug_source, _timeout_=12)
            resp.raise_for_status()
            b = io.BytesIO(resp.content)
            hug = Image.open(b)
            for i in range(2147483648):
                try:
                    hug.seek(i)
                except EOFError:
                    break
                frame = hug.convert("RGB").resize(output_size, resample=Image.LANCZOS)
                self.hug_frames.append(frame)
            self.crop = Image.new("L", (diameter,) * 2)
            shape_tool = ImageDraw.Draw(self.crop)
            shape_tool.ellipse((0, 0) + (diameter,) * 2, 255, 159, width=1)
        aspect_ratio = img.width / img.height
        if aspect_ratio < 1:
            width = round(diameter * aspect_ratio)
            height = diameter
        else:
            width = diameter
            height = round(diameter / aspect_ratio)
        size = (width, height)
        if width != height:
            x = (diameter - width) // 2
            y = (diameter - height) // 2
            crop = self.crop.crop((x, y, x + width, y + height))
        else:
            crop = self.crop
        target = tuple(pos[i] - size[i] // 2 for i in range(2))
        source_frames = []
        for i in range(2147483648):
            try:
                img.seek(i)
            except EOFError:
                break
            frame = img.resize(size, resample=Image.LANCZOS)
            if frame.mode == "P":
                frame = frame.convert("RGBA")
            source_frames.append(frame)
        ts = time.time_ns() // 1000
        fn = str(ts) + ".gif"
        args = [
            "ffmpeg", "-threads", "2", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-framerate", "1", "-pix_fmt", "rgb24", "-video_size", "x".join(map(str, output_size)), "-i", "-",
            "-gifflags", "-offsetting", "-an", "-vf", "split[s0][s1];[s0]palettegen=reserve_transparent=1:stats_mode=diff[p];[s1][p]paletteuse=diff_mode=rectangle:alpha_threshold=128", "-loop", "0", fn
        ]
        proc = psutil.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            dest_frames = []
            for i, frame in enumerate(self.hug_frames):
                source = source_frames[i % len(source_frames)]
                frame = frame.convert("RGBA")
                if source.mode == "RGBA":
                    alpha = ImageChops.multiply(source.getchannel("A"), crop)
                else:
                    alpha = crop
                source.putalpha(alpha)
                frame.alpha_composite(source, target)
                if frame.mode != "RGB":
                    frame = frame.convert("RGB")
                b = frame.tobytes()
                await create_future(proc.stdin.write, b)
            proc.stdin.close()
            await create_future(proc.wait)
            f = discord.File(fn, filename="huggies.gif")
            await ctx.channel.send(f"<:miza_dottie_hug:788165800448098324> ***{caption}*** *gets a hug!*", file=f)
        except:
            try:
                os.remove(fn)
            except:
                pass
            raise
        else:
            try:
                os.remove(fn)
            except:
                pass


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
                await ctx.send("Woah, be careful, this command pulls **graphic imagery**! Try again in an **NSFW channel**!")


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
                for name in http_cats:
                    if str(name["name"]) == code or code.lower() in name["description"].lower():
                        cat_response = name
                        break
            embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
            embed.set_footer(text="Images are from https://http.cat/")
            embed.description = cat_response["description"]
            embed.set_image(url=cat_response["image"])
            await ctx.send(embed=embed)

    
    @commands.command(aliases=["inspirobot", "inspiration"])
    async def inspiro(self, ctx):
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
        embed.set_footer(text="Images are from https://inspirobot.me/")
        quote = inspirobot.generate()
        embed.set_image(url=quote.url)
        if ctx.channel.is_nsfw():
                await ctx.send(embed=embed)
        else:
            await ctx.send("Woah, be careful, this command pulls **sexual references**! Try again in an **NSFW channel**!")


    @commands.command(aliases=["marble"])
    async def marble_fox(self, ctx):
        marble_foxes = None
        with open("json/marble_foxes.json", "r") as f:
                dreamstime_imgs = json.load(f)
                marble_foxes = random.choice(dreamstime_imgs)
                embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
                embed.set_footer(text="Images are from https://www.dreamstime.com/photos-images/marble-fox.html")
                embed.set_image(url=marble_foxes["image"])
                embed.description = random.choice(["Yip!", "Yap!", "🦊", "<:sleepysmudgy:799210361692749824>"])
                await ctx.send(embed=embed)


    @commands.command(aliases=["sea_doggo", "seals"])
    async def seal(self, ctx):
        seal_number = random.randint(1, 83)
        if seal_number >= 10:
            seal = f"https://raw.githubusercontent.com/FocaBot/random-seal/master/seals/00{seal_number}.jpg"
        else:
            seal = f"https://raw.githubusercontent.com/FocaBot/random-seal/master/seals/000{seal_number}.jpg"
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
        embed.set_footer(text="Images are from https://github.com/FocaBot/random-seal")
        embed.set_image(url=seal)
        embed.description = random.choice(["Egg!", ":ocean: :dog:", ":seal:", "<a:curiouseal:748840270069760072>", "<:seal_ball:670143859149242369>"])
        await ctx.send(embed=embed)


    @commands.command(aliases=["og", "doggo", "puppo"])
    async def dog(self, ctx):
        r = requests.get("https://dog.ceo/api/breeds/image/random")
        data = r.json()
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
        embed.set_footer(text="Images are from https://dog.ceo/api/breeds/image/random")
        embed.set_image(url=data["message"])
        embed.description = random.choice(["Bärk!", "Börk!", "🐶", "🐕", "<:sleepydottie:799210814841421835>"])
        await ctx.send(embed=embed)


    @commands.command()
    async def fox(self, ctx):
        r = requests.get("https://randomfox.ca/floof/")
        data = r.json()
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
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
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
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