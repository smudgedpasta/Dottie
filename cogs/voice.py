from imports import *


class VOICE(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command(aliases=["get_your_butt_in_here", "join"], pass_context=True)
    async def connect(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            # Checks if the message author is in a voice channel and joins that one
            await channel.connect()
            await ctx.send("```ini\n[Successfully joined the Voice Channel! What a cozy place you got here! 😊]```")
        except:
            await ctx.send("Hey, I can't find you! You need to be in a voice channel first!")


    @commands.command(aliases=["go_naughty_step", "leave"], pass_context=True)
    async def disconnect(self, ctx):
        server = ctx.message.guild.voice_client
        # Simply checks if the VC is in the guild before disconnecting
        await server.disconnect()
        await ctx.send("```ini\n[Successfully disconnected from the Voice Channel... Sad that it is time to go... 😔]```")


    @commands.command(aliases=["espacito", "Despacito"], pass_context=True)
    async def despacito(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            for vc in self.dottie.voice_clients:
                if vc.guild == ctx.guild:
                    # Checks to make sure the vc and the guild are the same
                    vc.play(discord.FFmpegOpusAudio("misc/assets/music/Normal_Despacito.ogg"))
                    # Pulls the Despacito file straight from the directory
                    await ctx.send("***```css\n🥁 Embrace my [DESPACITO!]```***")
                    return
        except:
            await ctx.send("How are you meant to hear my *100% normal Despacito* from outside of a Voice Channel? Hop in one first!")


def setup(dottie):
    dottie.add_cog(VOICE(dottie))
