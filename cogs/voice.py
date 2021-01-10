from imports import *


class VOICE(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie

    
    """
    VOICE COMMANDS TEMPORARILY REMOVED FOR USE OF VOICE COMMANDS LOCATED AT HTTPS://GITHUB.COM/THOMAS-XIN/MIZA/BLOB/MASTER/COMMANDS/VOICE.PY
    ALL COMMANDS STILL WORK ASIDE FROM THE "get_your_butt_in_here" AND "go_naughty_step" ALIASES.
    """


    # @commands.command(aliases=["get_your_butt_in_here", "join"], pass_context=True)
    # async def connect(self, ctx):
    #     try:
    #         channel = ctx.message.author.voice.channel
    #         await channel.connect()
    #         await ctx.send("```ini\n[Successfully joined the Voice Channel! What a cozy place you got here! 😊]```")
    #     except:
    #         await ctx.send("Hey, I can't find you! You need to be in a voice channel first!")


    # @commands.command(aliases=["go_naughty_step", "leave"], pass_context=True)
    # async def disconnect(self, ctx):
    #     server = ctx.message.guild.voice_client
    #     await server.disconnect()
    #     await ctx.send("```ini\n[Successfully disconnected from the Voice Channel... Sad that it is time to go... 😔]```")


    @commands.command(aliases=["espacito"], pass_context=True)
    async def despacito(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            for vc in self.dottie.voice_clients:
                if vc.guild == ctx.guild:
                    vc.play(discord.FFmpegOpusAudio("misc/assets/music/Normal_Despacito.ogg"))
                    await ctx.send("***```css\n🥁 Embrace my [DESPACITO!]```***")
                    return
        except:
            await ctx.send("How are you meant to hear my *100% normal Despacito* from outside of a Voice Channel? Hop in one first!")


def setup(dottie):
    dottie.add_cog(VOICE(dottie))
