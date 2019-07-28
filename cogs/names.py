import re
import discord
import sre_yield
from ruamel.yaml import YAML

yaml = YAML()


class Names(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def names(self, ctx, args):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        mainlang = self.bot.lang[self.bot.config["mainlang"]]
        if len(args) > 0:
            for each in lang["names"]["sections"]:
                if re.fullmatch(lang["names"]["sections"][each]["command"], args.casefold()) is not None or re.fullmatch(mainlang["names"]["sections"][each]["command"], args.casefold()) is not None:
                    arg = each
                    break
            if "arg" in locals():
                file = self.bot.names[each]
                c = 0
                for each in file["names"]:
                    if each[0] != ".":
                        c += 1
                color = file["color"].replace(" ", "").split(",")
                embed = discord.Embed(title="{} {} ({})".format(file["emote"], lang["names"]["sections"][arg]["title"], c), color=discord.Colour.from_rgb(int(color[0]), int(color[1]), int(color[2])))
                c = 1
                l = {}
                div = (int(len(file["names"]) / int(file["column"]))) if len(file["names"]) % int(file["column"]) == 0 else (int(len(file["names"]) / int(file["column"])) + 1)
                for each in file["names"]:
                    if each[0] != ".":
                        if c in l:
                            if len(l[c]) >= div:
                                c += 1
                        if c in l:
                            e = l[c]
                            e.append("**•** {}".format(each))
                            l.update({c: e})
                        else:
                            l.update({c: ["**•** {}".format(each)]})
                    else:
                        if c in l:
                            e = l[c]
                            e.append("**-** {}".format(each[1:]))
                            l.update({c: e})
                        else:
                            l.update({c: ["**-** {}".format(each[1:])]})
                for each in l:
                    embed.add_field(name="‎", value="\n".join(l[each]))
                if "footer" in file:
                    embed.set_footer(text=file["footer"])
                await ctx.channel.send(embed=embed)
            else:
                await self.names(ctx, "")
        else:
            embed = discord.Embed(title="{} {}".format(lang["names"]["args"]["emote"], lang["names"]["args"]["title"]), color=self.bot.get_cog("Main").get_color("names"))
            embed.add_field(name=lang["names"]["args"]["usage"]["name"], value=lang["names"]["args"]["usage"]["text"], inline=False)
            field = []
            for each in lang["names"]["sections"]:
                field.append("[•] {}".format(", ".join(list(sre_yield.AllStrings(lang["names"]["sections"][each]["command"]))[:5])))
            embed.add_field(name=lang["names"]["args"]["sections"], value="```css\n{}\n```".format("\n".join(field)), inline=False)
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Names(bot))
