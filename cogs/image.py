from imports import *


class IMAGE(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    hug_source = "https://media.tenor.com/images/0244cd88bd3ab775c8937db10e5d2a57/tenor.gif"
    hug_frames = None
    @commands.command(aliases=["nuzzle"])
    async def hug(self, ctx, url=None):
        output_size = (440, 356)
        pos = (180, 160)
        if not url:
            if ctx.message.attachments:
                url = ctx.message.attachments[0].url
            else:
                url = ctx.author.avatar_url
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
        resp = await create_future(requests.get, url, _timeout_=12)
        resp.raise_for_status()
        b = io.BytesIO(resp.content)
        img = Image.open(b)
        if self.hug_frames is None:
            resp = await create_future(requests.get, self.hug_source, _timeout_=12)
            resp.raise_for_status()
            b = io.BytesIO(resp.content)
            hug = Image.open(b)
            self.hug_frames = []
            for i in range(2147483648):
                try:
                    hug.seek(i)
                except EOFError:
                    break
                frame = hug.convert("RGB").resize(output_size, resample=Image.LANCZOS)
                self.hug_frames.append(frame)
        aspect_ratio = img.width / img.height
        if aspect_ratio < 1:
            width = round(96 * aspect_ratio)
            height = 96
        else:
            width = 96
            height = round(96 / aspect_ratio)
        size = (width, height)
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
            "ffmpeg", "-threads", "2", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-framerate", "10", "-pix_fmt", "rgb24", "-video_size", "x".join(map(str, output_size)), "-i", "-",
            "-gifflags", "-offsetting", "-an", "-vf", "split[s0][s1];[s0]palettegen=reserve_transparent=1:stats_mode=diff[p];[s1][p]paletteuse=diff_mode=rectangle:alpha_threshold=128", "-loop", "0", fn
        ]
        proc = psutil.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dest_frames = []
        for i, frame in enumerate(self.hug_frames):
            source = source_frames[i % len(source_frames)]
            if source.mode == "RGBA":
                frame = frame.convert("RGBA")
                frame.alpha_composite(source, target)
            else:
                frame = frame.copy()
                frame.paste(source, target)
            if frame.mode != "RGB":
                frame = frame.convert("RGB")
            b = frame.tobytes()
            proc.stdin.write(b)
        proc.stdin.close()
        await create_future(proc.wait)
        f = discord.File(fn, filename="huggies.gif")
        await ctx.channel.send(file=f)
        try:
            os.remove(fn)
        except:
            pass
        
    '''
    Comments:

    Resizes the hug GIF to (440, 356) to provide more space to insert source image.
    "pos" centres position to paste image.
    If nothing is in the message but there are attachments, take the first one as input, otherwise take original author's avatar as input.
    Next determines if a user ID was provided, or determines if a user mention was provided.
    get_user works if the target user shares at least one server with dottie due to intents, if not then fetch_user searches Discord.
    Finally, uses user avatar as URL (in case the user search didn't find anything, assumes input is a direct URL).

    Uses "create_future" from Miza instead of "requests.get", because requests are not async, and while it's running Dottie will not be able to do anything else.
    "raise" refers to raising an exception if the request errored.
    Then wraps the response's content in a simulated file to open; opening the data as an image file (with many different formats supported).
    Loads hug image/GIF if used for the first time, this should not run on subsequent uses of the command.
    Seeks through every frame of the hug image for if it's a GIF, "I put 214743648 because it's what I did for Miza, but any number equal to or higher than the total frame count will work" - Thomas Xin
    Copies the current frame as an RGB image and adds it to the hug frames list, then calculates appropriate width/height to resize image in order to best fit the target size of (96, 96).
    "target = tuple(pos[i] - size[i] // 2 for i in range(2))" - Calculates target position of top left corner of rectangle to copy image into.
    Then extracts frames of source image (as it may be a GIF too).

    Resizes the target image to the targeted size.
    If the image is a PNG/GIF with a palette, assume it can store alpha values
    Creates filenames using the current time, so hopefully that won't conflict with any existing files.
    Copies every frame of the hug GIF and pastes a frame of the source image into it; uses the FFmpeg process to concatenate the frames into a GIF.
    
    Next blends with alpha if applicable.
    Converts the image to RGB raw bitmap format in bytes and passes to FFmpeg (with "stdin") before informing FFmpeg that the input is complete, and waits for FFmpeg to finish saving the file.
    Prepares the huggy cannon to send the huggies! :D
    And lastly, removes the temporary GIF file from Dottie's repository if possible.
    '''


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
                code = int(code)
                for name in http_cats:
                    if name["name"] == code:
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