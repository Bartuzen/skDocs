import io
import traceback
import textwrap
import discord
from os import listdir
from os.path import isfile, join
from contextlib import redirect_stdout
from ruamel.yaml import YAML

yaml = YAML()


class Admin(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    async def eval(self, ctx, body):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        if ctx.author.id not in self.bot.config["admins"]:
            await ctx.channel.send(embed=(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["errors"]["permission"], color=self.bot.get_cog("Main").get_color("error"))))
            return
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx,
            "_": self._last_result
        }
        env.update(globals())
        if body.startswith("```") and body.endswith("```"):
            body = "\n".join(body.split("\n")[1:-1])
        else:
            body = body.strip("` \n")
        stdout = io.StringIO()
        to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.channel.send(f"```py\n{e.__class__.__name__}: {e}\n```")
        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.channel.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.add_reaction("\u2705")
            except:
                pass
            if ret is None:
                if value:
                    await ctx.channel.send(f"```py\n{value}\n```")
            else:
                self._last_result = ret
                await ctx.channel.send(f"```py\n{value}{ret}\n```")

    async def reload(self, ctx):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        if ctx.author.id in self.bot.config["admins"]:
            msg = await ctx.channel.send(embed=(discord.Embed(title="✅ {}".format(lang["reload"]["reloading"]["title"]), description=lang["reload"]["reloading"]["desc"], color=self.bot.get_cog("Main").get_color("reload"))))
            try:
                Admin.rel(self)
            except Exception as e:
                await msg.edit(embed=(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description="{}\n```py\n{}\n```".format(lang["reload"]["reloaded"]["error"], e), color=self.bot.get_cog("Main").get_color("error"))))
            else:
                await msg.edit(embed=(discord.Embed(title="✅ {}".format(lang["reload"]["reloaded"]["title"]), description=lang["reload"]["reloaded"]["successfully"], color=self.bot.get_cog("Main").get_color("reload"))))
        else:
            await ctx.channel.send(embed=(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["errors"]["permission"], color=self.bot.get_cog("Main").get_color("error"))))

    def rel(self, cogs=True):
        self.bot.lang = {}
        for each in [f for f in listdir("lang") if isfile(join("lang", f))]:
            if each[-4:] == ".yml":
                with open("lang/{}".format(each), "r", encoding="utf-8-sig") as stream:
                    self.bot.lang.update({each[:-4]: yaml.load(stream)})
        with open("config.yml", "r", encoding="utf-8-sig") as stream:
            self.bot.config = yaml.load(stream)
        with open("downloads.yml", "r", encoding="utf-8-sig") as stream:
            self.bot.downs = yaml.load(stream)
        with open("guilds.yml", "r", encoding="utf-8-sig") as f:
            self.bot.guildLangs = yaml.load(f) or {}
        self.bot.names = {}
        for each in [f for f in listdir("names") if isfile(join("names", f))]:
            if each[-4:] == ".yml":
                with open("names/{}".format(each), "r", encoding="utf-8-sig") as stream:
                    self.bot.names.update({each[:-4]: yaml.load(stream)})
        if cogs:
            for each in ["admin",
                         "docs",
                         "download",
                         "ehandler",
                         "help",
                         "info",
                         "lang",
                         "main",
                         "names",
                         "parser"]:
                self.bot.reload_extension(f"cogs.{each}")


def setup(bot):
    bot.add_cog(Admin(bot))
