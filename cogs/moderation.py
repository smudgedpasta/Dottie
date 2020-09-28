from modules import *


class MODERATION(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command()
    @has_permissions(administrator=True)
    async def purge(self, ctx, amount=1):
        if amount == 1:
            # If no amount is specified, only one message is purged
            await ctx.channel.purge(limit=amount+1)
            await ctx.send(f":broom: swept away **1** message!")
        elif amount > 0:
            await ctx.channel.purge(limit=amount+1)
            # The +1 allows for the command message to be deleted as well as the specified amount
            await ctx.send(f":broom: Swept away **{amount}** messages!")
        elif amount < 1:
            await ctx.send(f"How am I meant to purge **{amount}** messages, silly?".format(amount))


    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reasons=None):
        await member.kick(reason=reasons)
        await ctx.send(f"{member.name}#{member.discriminator} has been *yeet* right out the server! :lock:")


    @commands.command()
    @has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reasons=None):
        await member.ban(reason=reasons)
        await ctx.send(f"Good riddance, {member.name}#{member.discriminator}! :closed_lock_with_key:")


    @commands.command()
    @has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        # Removes the "#" from the argument as it searches for matching name and ID
        for ban_entry in banned_users:
            # Runs a for loop through the ban list to find the specified user
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Granted access back to the server for {user.name}#{user.discriminator}. :unlock:")
                return


def setup(dottie):
    dottie.add_cog(MODERATION(dottie))
