import discord
from ruamel.yaml import YAML

yaml = YAML()


class Lang(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def lang(self, ctx, args):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
            if ctx.channel.permissions_for(ctx.author).manage_guild:
                if len(args) != 0:
                    for each in self.bot.lang:
                        if self.bot.lang[each]["name"].casefold() == args.casefold():
                            self.bot.guildLangs.update({ctx.guild.id: each})
                            with open("guilds.yml", "w") as f:
                                yaml.dump(self.bot.guildLangs, stream=f)
                            await ctx.channel.send(embed=discord.Embed(title="✅ {}".format(self.bot.lang[self.bot.guildLangs[ctx.guild.id]]["lang"]["successful"]), description="{}\n**{}**: `{}`".format(self.bot.lang[self.bot.guildLangs[ctx.guild.id]]["lang"]["set"], self.bot.lang[self.bot.guildLangs[ctx.guild.id]]["lang"]["translator"], self.bot.lang[self.bot.guildLangs[ctx.guild.id]]["translator"]), color=self.bot.get_cog("Main").get_color("lang")))
                            return
                    await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["lang"]["not-found"], color=self.bot.get_cog("Main").get_color("error")))
                else:
                    langs = []
                    for each in self.bot.lang:
                        langs.append(self.bot.lang[each]["name"])
                    embed = discord.Embed(title="{} {}".format(lang["lang"]["emote"], lang["lang"]["langs"]), color=self.bot.get_cog("Main").get_color("lang"))
                    embed.add_field(name=lang["lang"]["available-langs"], value=", ".join(langs), inline=False)
                    embed.add_field(name=lang["lang"]["usage-text"], value=lang["lang"]["usage"], inline=False)
                    await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send(embed=(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["errors"]["permission"], color=self.bot.get_cog("Main").get_color("error"))))
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["lang"]["only-in-guild"], color=self.bot.get_cog("Main").get_color("error")))

    @discord.ext.commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.guildLangs.update({guild.id: self.bot.config["mainlang"]})
        with open("guilds.yml", "w") as f:
            yaml.dump(self.bot.guildLangs, stream=f)


def setup(bot):
    bot.add_cog(Lang(bot))
