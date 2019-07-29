import os
import sys
import math
import psutil
import discord
from datetime import datetime


class Info(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def info(self, ctx):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        embed = discord.Embed(title="🛠️ {}".format(lang["info"]["title"]), color=self.bot.get_cog("Main").get_color("info"))
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        used_ram = psutil.Process(pid=os.getpid()).memory_info().rss / (1024 * 1024)
        total_ram = psutil.virtual_memory().total / (1024 * 1024)
        embed.add_field(name=lang["info"]["ram"], value=f"{math.floor(used_ram)} / {math.floor(total_ram)} MB")
        embed.add_field(name=lang["info"]["uptime"], value=self.uptime(lang))
        embed.add_field(name=lang["info"]["guilds"], value="{} - [{}](https://discordapp.com/oauth2/authorize?client_id={}&scope=bot)".format(len(self.bot.guilds), lang["info"]["invite"], self.bot.user.id))
        embed.add_field(name=lang["info"]["version"]["python"], value=sys.version.split(" ")[0])
        embed.add_field(name=lang["info"]["version"]["discord.py"], value=discord.__version__)
        embed.add_field(name="GitHub", value="[{}]({})".format(lang["info"]["click"], self.bot.config["github"]))
        try:
            developer = await self.bot.fetch_user(self.bot.config["developer"])
            embed.set_footer(text=lang["info"]["developer"].replace("%owner%", developer.name + "#" + developer.discriminator), icon_url=developer.avatar_url)
        except discord.NotFound:
            pass
        await ctx.channel.send(embed=embed)

    def uptime(self, lang):
        delta_uptime = datetime.utcnow() - self.bot.start
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if days > 0:
            return "{} {} {} {}".format(days, lang["info"]["time"]["day"], hours, lang["info"]["time"]["hour"])
        elif hours > 0:
            return "{} {} {} {}".format(hours, lang["info"]["time"]["hour"], minutes, lang["info"]["time"]["minute"])
        elif minutes > 0:
            return "{} {} {} {}".format(minutes, lang["info"]["time"]["minute"], seconds, lang["info"]["time"]["second"])
        return "{} {}".format(seconds, lang["info"]["time"]["second"])


def setup(bot):
    bot.add_cog(Info(bot))
