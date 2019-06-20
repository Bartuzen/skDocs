import discord


class Help(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def help(self, ctx):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        embeds = []
        for embed in lang["help"]["embeds"]:
            embeds.append(discord.Embed(title=lang["help"]["embeds"][embed]["title"], description="\n".join(lang["help"]["embeds"][embed]["description"] if "description" in lang["help"]["embeds"][embed] else None),colour=(discord.Colour.from_rgb(int(lang["help"]["embeds"][embed]["color"].replace(" ", "").split(",")[0]),int(lang["help"]["embeds"][embed]["color"].replace(" ", "").split(",")[1]),int(lang["help"]["embeds"][embed]["color"].replace(" ", "").split(",")[2])) if "color" in lang["help"]["embeds"][embed] else discord.Embed.Empty)))
            for field in lang["help"]["embeds"][embed]["fields"]:
                embeds[-1].add_field(name=lang["help"]["embeds"][embed]["fields"][field]["title"], value="\n".join(lang["help"]["embeds"][embed]["fields"][field]["content"]) if "content" in lang["help"]["embeds"][embed]["fields"][field] else None,inline=lang["help"]["embeds"][embed]["fields"][field]["inline"] if "inline" in lang["help"]["embeds"][embed]["fields"][field] else False)
        for each in embeds:
            try:
                await ctx.author.send(embed=each)
            except discord.Forbidden:
                send = False
        if "send" in locals():
            await ctx.channel.send(lang["help"]["forbidden"].replace("%user%", ctx.author.mention))
        elif ctx.guild:
            await ctx.channel.send(lang["help"]["sent-dm"].replace("%user%", ctx.author.mention))


def setup(bot):
    bot.add_cog(Help(bot))
