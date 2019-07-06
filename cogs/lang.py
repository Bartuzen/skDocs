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
                    msg = self.set_lang(ctx.guild, args)
                    if msg is None:
                        await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]),
                                                                   description=lang["lang"]["not-found"],
                                                                   color=self.bot.get_cog("Main").get_color("error")))
                    else:
                        await ctx.channel.send(embed=msg)
                else:
                    langs = []
                    emotes = []
                    for each in self.bot.lang:
                        langs.append("{} ({})".format(self.bot.lang[each]["name"], self.bot.lang[each]["emote"]))
                        emotes.append(self.bot.lang[each]["emote"])
                    embed = discord.Embed(title="{} {}".format(lang["lang"]["emote"], lang["lang"]["langs"]), color=self.bot.get_cog("Main").get_color("lang"))
                    embed.add_field(name=lang["lang"]["available-langs"], value="\n".join(langs), inline=False)
                    embed.add_field(name=lang["lang"]["usage-text"], value=lang["lang"]["usage"], inline=False)
                    msg = await ctx.channel.send(embed=embed)
                    self.bot.messages.update({msg.id: None})
                    try:
                        for each in emotes:
                            await msg.add_reaction(each)
                    except discord.errors.Forbidden:
                        pass
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

    @discord.ext.commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        if (msg.author != self.bot.user) or (user == self.bot.user):
            return
        try:
            await reaction.message.remove_reaction(reaction, user)
        except discord.errors.Forbidden:
            pass
        if msg.channel.permissions_for(user).manage_guild and msg.id in self.bot.messages:
            embed = self.set_lang(msg.guild, str(reaction))
            if embed is not None:
                await msg.edit(embed=embed)

    def set_lang(self, guild, lang):
        for each in self.bot.lang:
            if self.bot.lang[each]["name"].casefold() == lang.casefold() or self.bot.lang[each]["emote"] == lang:
                self.bot.guildLangs.update({guild.id: each})
                lang = self.bot.lang[each]
                with open("guilds.yml", "w") as f:
                    yaml.dump(self.bot.guildLangs, stream=f)
                return discord.Embed(title="✅ {}".format(lang["lang"]["successful"]),
                                     description="{}\n**{}**: `{}`".format(lang["lang"]["set"], lang["lang"]["translator"], lang["translator"]),
                                     color=self.bot.get_cog("Main").get_color("lang"))


def setup(bot):
    bot.add_cog(Lang(bot))
