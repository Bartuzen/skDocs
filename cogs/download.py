import re
import discord


class Download(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def download(self, ctx, args):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        mainlang = self.bot.lang[self.bot.config["mainlang"]]
        addons = []
        if len(args) == 0:
            down = ["skript", "addon", "aliases", "paper", "spigot"]
        else:
            down = []
            for each in args:
                if "skript" in lang["downloads"]["commands"] and re.fullmatch(lang["downloads"]["commands"]["skript"], each.casefold()) is not None or re.fullmatch(mainlang["downloads"]["commands"]["skript"], each.casefold()) is not None:
                    if "skript" not in down:
                        down.append("skript")
                elif "addon" in lang["downloads"]["commands"] and re.fullmatch(lang["downloads"]["commands"]["addon"], each.casefold()) is not None or re.fullmatch(mainlang["downloads"]["commands"]["addon"], each.casefold()) is not None:
                    if "addon" not in down:
                        down.append("addon")
                elif "aliases" in lang["downloads"]["commands"] and re.fullmatch(lang["downloads"]["commands"]["aliases"], each.casefold()) is not None or re.fullmatch(mainlang["downloads"]["commands"]["aliases"], each.casefold()) is not None:
                    if "aliases" not in down:
                        down.append("aliases")
                elif "paper" in lang["downloads"]["commands"] and re.fullmatch(lang["downloads"]["commands"]["paper"], each.casefold()) is not None or re.fullmatch(mainlang["downloads"]["commands"]["paper"], each.casefold()) is not None:
                    if "paper" not in down:
                        down.append("paper")
                elif "spigot" in lang["downloads"]["commands"] and re.fullmatch(lang["downloads"]["commands"]["spigot"], each.casefold()) is not None or re.fullmatch(mainlang["downloads"]["commands"]["spigot"], each.casefold()) is not None:
                    if "spigot" not in down:
                        down.append("spigot")
                else:
                    ok = 0
                    for loop in self.bot.addonj:
                        if each.casefold() in loop.casefold():
                            ok = 1
                            if "{}||{}".format(loop, self.bot.addonj[loop]["url"]) not in addons:
                                addons.append("{}||{}".format(loop, self.bot.addonj[loop]["url"]))
                                break
                    if ok == 0:
                        msg = await ctx.channel.send(embed=(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["downloads"]["unknown-file"].replace("%file%", each), color=self.bot.get_cog("Main").get_color("error"))))
                        self.bot.messages.update({msg.id: {"command": self, "user": ctx.author.id, "message": ctx.id}})
                        try:
                            await msg.add_reaction("❌")
                        except (discord.errors.Forbidden, discord.errors.NotFound):
                            pass
                        return
        embed = discord.Embed(title="{} {}".format(lang["downloads"]["emote"], lang["downloads"]["title"]), color=self.bot.get_cog("Main").get_color("downloads"))
        if len(down) + len(addons) <= 20:
            if len(down) + len(addons) >= 1:
                if "skript" in down:
                    skript = []
                    for each in self.bot.downs["downloads"]["Skript"]:
                        if each != "latest":
                            if len(each.split("_")) > 1:
                                skript.append("[Skript {}]({}) {}".format(each.split("_")[0], self.bot.downs["downloads"]["Skript"][each], each.split("_")[1]))
                            else:
                                skript.append("[Skript {}]({})".format(each, self.bot.downs["downloads"]["Skript"][each]))
                        else:
                            skript.append("[Skript {}]({})".format(lang["downloads"]["latest"], self.bot.downs["downloads"]["Skript"][each]))
                    embed.add_field(name="Skript", value=" - ".join(skript), inline=False)
                if "addon" in down:
                    addon = []
                    for each in self.bot.addonj:
                        if each.casefold() != "skript":
                            addon.append("[{}]({})".format(each, self.bot.addonj[each]["url"]))
                    addon.sort()
                    perfield = int(len(addon) / 6) + (0 if (len(addon) / 6).is_integer() else 1)
                    add = []
                    count = 0
                    for each in addon:
                        count += 1
                        add.append("**{}.** {}".format(count, each))
                        if len(add) == perfield:
                            embed.add_field(name=(lang["downloads"]["addons"] if "name" not in locals() else "‎"), value="\n".join(add))
                            add.clear()
                            added = 1
                            name = 1
                        else:
                            added = 0
                    if added == 0:
                        embed.add_field(name=(lang["downloads"]["addons"] if "name" not in locals() else "‎"), value="\n".join(add))
                elif len(addons) > 0:
                    for each in addons:
                        embed.add_field(name=lang["downloads"]["file-link"].replace("%file%", each.split("||")[0]), value=each.split("||")[1], inline=False)
                if "aliases" in down:
                    aliases = []
                    for each in self.bot.downs["downloads"]["aliases"]:
                        aliases.append("[Minecraft {}]({})".format(each, self.bot.downs["downloads"]["aliases"][each]))
                    embed.add_field(name="Aliases", value=" - ".join(aliases), inline=False)
                if "paper" in down:
                    paper = []
                    for each in self.bot.downs["downloads"]["Paper"]:
                        paper.append("[{}](https://papermc.io/api/v1/paper/{}/latest/download)".format(each, each))
                    embed.add_field(name=lang["downloads"]["paper"], value=" - ".join(paper), inline=False)
                if "spigot" in down:
                    embed.add_field(name=lang["downloads"]["spigot"], value=self.bot.downs["downloads"]["Spigot"], inline=False)
                try:
                    msg = await ctx.channel.send(embed=embed)
                except discord.errors.HTTPException:
                    msg = await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["downloads"]["too-long"], color=self.bot.get_cog("Main").get_color("error")))
            else:
                msg = await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["downloads"]["no-arg"], color=self.bot.get_cog("Main").get_color("error")))
        else:
            msg = await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["downloads"]["too-long"], color=self.bot.get_cog("Main").get_color("error")))
        self.bot.messages.update({msg.id: {"command": self, "user": ctx.author.id, "message": ctx.id}})
        try:
            await msg.add_reaction("❌")
        except (discord.errors.Forbidden, discord.errors.NotFound):
            pass

    @discord.ext.commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        messages = self.bot.messages

        if msg.author != self.bot.user or user == self.bot.user or msg.id not in messages or messages[msg.id]["command"] != self:
            return

        try:
            await msg.remove_reaction(reaction, user)
        except (discord.errors.Forbidden, discord.errors.NotFound):
            pass

        if not user.bot and ((messages[msg.id]["user"] == user.id) or reaction.message.channel.permissions_for(user).manage_guild) and (str(reaction) == "❌"):
            try:
                delete_msg = await reaction.message.channel.fetch_message(messages[msg.id]["message"])
                await delete_msg.delete()
            except (discord.errors.Forbidden, discord.errors.NotFound):
                pass
            await reaction.message.delete()
            messages.pop(reaction.message.id)


def setup(bot):
    bot.add_cog(Download(bot))
