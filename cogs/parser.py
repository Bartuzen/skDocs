import json
import discord
import requests
from parse import parse
from ruamel.yaml import YAML

yaml = YAML()


class Parsing(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def removeindent(self, text):
        if text.startswith("```") and text.endswith("```"):
            text = "\n".join(text.split("\n")[1:-1])
        return text

    def gettext(self, url):
        if not url.startswith("https://") and not url.startswith("http://"):
            return None
        if url.startswith("https://"):
            url = url[8:]
        elif url.startswith("http://"):
            url = url[7:]
        if url.startswith("www."):
            url = url[4:]
        if parse("gist.github.com/{}/{}", url) is not None:
            j = json.loads(requests.get("https://api.github.com/gists/" + parse("gist.github.com/{}/{}", url)[1]).text)
            return j["files"][list(j["files"].keys())[0]]["content"]
        if parse("hastebin.com/{}", url) is not None:
            return requests.get("https://hastebin.com/raw/" + parse("hastebin.com/{}", url)[0]).text
        if parse("github.com/{}/{}/{}/{}/{}", url) is not None:
            p = parse("github.com/{}/{}/{}/{}/{}", url)
            return requests.get("https://raw.githubusercontent.com/" + p[0] + "/" + p[1] + "/" + p[3] + "/" + p[4]).text
        return False

    async def yamlparse(self, ctx, t):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        t = Parsing.removeindent(self, t)
        try:
            text = Parsing.gettext(self, t)
        except requests.exceptions.RequestException:
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["parse"]["cant-access"].replace("\\n", "\n"), color=self.bot.get_cog("Main").get_color("error")))
            return
        if text is None:
            text = t
        if not text:
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["parse"]["unknown-website"].replace("\\n", "\n"), color=self.bot.get_cog("Main").get_color("error")))
            return
        try:
            yaml.load(text)
        except Exception as e:
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description="{}\n```py\n{}\n```".format(lang["parse"]["yaml"]["error"], e), color=self.bot.get_cog("Main").get_color("error")))
        else:
            try:
                await ctx.channel.send(embed=discord.Embed(title="{} {}".format(lang["parse"]["successful"]["emote"], lang["parse"]["successful"]["title"]), description=lang["parse"]["yaml"]["successful"], color=self.bot.get_cog("Main").get_color("parse-success")))
            except discord.errors.HTTPException:
                await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["parse"]["too-long"], color=self.bot.get_cog("Main").get_color("error")))

    async def jsonparse(self, ctx, t):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        t = Parsing.removeindent(self, t)
        try:
            text = Parsing.gettext(self, t)
        except requests.exceptions.RequestException:
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["parse"]["cant-access"].replace("\\n", "\n"), color=self.bot.get_cog("Main").get_color("error")))
            return
        if text is None:
            text = t
        if not text:
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["parse"]["unknown-website"].replace("\\n", "\n"), color=self.bot.get_cog("Main").get_color("error")))
            return
        try:
            json.loads(text)
        except Exception as e:
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description="{}\n```py\n{}\n```".format(lang["parse"]["json"]["error"], e), color=self.bot.get_cog("Main").get_color("error")))
        else:
            try:
                await ctx.channel.send(embed=discord.Embed(title="{} {}".format(lang["parse"]["successful"]["emote"], lang["parse"]["successful"]["title"]), description=lang["parse"]["json"]["successful"], color=self.bot.get_cog("Main").get_color("parse-success")))
            except discord.errors.HTTPException:
                await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["parse"]["too-long"], color=self.bot.get_cog("Main").get_color("error")))

    async def jsonbeautify(self, ctx, t):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        if t.split()[0].isdigit():
            ind = int(t.split()[0])
            t = " ".join(t.split()[1:])
        else:
            ind = 2
        t = Parsing.removeindent(self, t)
        try:
            text = Parsing.gettext(self, t)
        except requests.exceptions.RequestException:
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["parse"]["cant-access"].replace("\\n", "\n"), color=self.bot.get_cog("Main").get_color("error")))
            return
        if text is None:
            text = t
        if not text:
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["parse"]["unknown-website"].replace("\\n", "\n"), color=self.bot.get_cog("Main").get_color("error")))
            return
        try:
            j = json.loads(text)
        except Exception as e:
            await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description="{}\n```py\n{}\n```".format(lang["parse"]["json"]["error"], e), color=self.bot.get_cog("Main").get_color("error")))
        else:
            try:
                await ctx.channel.send(embed=discord.Embed(title="{} {}".format(lang["parse"]["successful"]["emote"], lang["parse"]["successful"]["title"]), description="{}\n```py\n{}\n```".format(lang["parse"]["json"]["beautified"], json.dumps(j, indent=ind)), color=self.bot.get_cog("Main").get_color("parse-success")))
            except discord.errors.HTTPException:
                await ctx.channel.send(embed=discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["parse"]["too-long"], color=self.bot.get_cog("Main").get_color("error")))


def setup(bot):
    bot.add_cog(Parsing(bot))
