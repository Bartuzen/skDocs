import discord


class EHandler(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass


def setup(bot):
    bot.add_cog(EHandler(bot))
