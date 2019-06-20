import re
import discord
import ruamel.yaml


class Main(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.ext.commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot or (msg.guild is not None and not msg.channel.permissions_for(msg.guild.me).send_messages):
            return
        if msg.guild:
            lang = self.bot.lang[self.bot.guildLangs[msg.guild.id]] if msg.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        mainlang = self.bot.lang[self.bot.config["mainlang"]]
        if msg.content.casefold().startswith("!sk ") or msg.content.startswith("{} ".format(self.bot.user.mention)):
            if re.fullmatch(lang["docs"]["commands"]["main"], msg.content.split()[1].casefold()) is not None or re.fullmatch(mainlang["docs"]["commands"]["main"], msg.content.split()[1].casefold()) is not None:
                await self.bot.get_cog("Docs").docs(msg, " ".join(msg.content.split()[2:]))
            elif re.fullmatch(lang["downloads"]["commands"]["main"], msg.content.split()[1].casefold()) is not None or re.fullmatch(mainlang["downloads"]["commands"]["main"], msg.content.split()[1].casefold()) is not None:
                await self.bot.get_cog("Download").download(msg, msg.content.split()[2:])
            elif re.fullmatch(lang["names"]["command"], msg.content.split()[1].casefold()) is not None or re.fullmatch(mainlang["names"]["command"], msg.content.split()[1].casefold()) is not None:
                await self.bot.get_cog("Names").names(msg, " ".join(msg.content.split()[2:]))
            elif re.fullmatch(lang["help"]["command"], msg.content.split()[1].casefold()) is not None or re.fullmatch(mainlang["help"]["command"], msg.content.split()[1].casefold()) is not None:
                await self.bot.get_cog("Help").help(msg)
            elif re.fullmatch(lang["info"]["command"], msg.content.split()[1].casefold()) is not None or re.fullmatch(mainlang["info"]["command"], msg.content.split()[1].casefold()) is not None:
                await self.bot.get_cog("Info").info(msg)
            elif msg.content.split()[1].casefold() == "yamlparse":
                await self.bot.get_cog("Parsing").yamlparse(msg, " ".join(msg.content.split()[2:]))
            elif msg.content.split()[1].casefold() == "jsonparse":
                await self.bot.get_cog("Parsing").jsonparse(msg, " ".join(msg.content.split()[2:]))
            elif msg.content.split()[1].casefold() == "jsonbeautify":
                await self.bot.get_cog("Parsing").jsonbeautify(msg, " ".join(msg.content.split()[2:]))
            elif msg.content.split()[1].casefold() == "lang" or msg.content.split()[1].casefold() == "language":
                await self.bot.get_cog("Lang").lang(msg, " ".join(msg.content.split()[2:]))
            elif msg.content.split()[1].casefold() == "eval":
                await self.bot.get_cog("Admin").eval(msg, msg.content[len(msg.content.split()[0]) + 6:])
            elif (msg.content.split()[1].casefold() == "reload") or (msg.content.split()[1].casefold() == "rel") or (msg.content.split()[1].casefold() == "rl"):
                await self.bot.get_cog("Admin").reload(msg)

    def get_color(self, color):
        color = self.bot.config["embed-colors"][color].replace(" ", "").split(",")
        return discord.Colour.from_rgb(int(color[0]), int(color[1]), int(color[2]))

    def get_text(self, value, rp1=None, rp2=None):
        if type(value) == ruamel.yaml.comments.CommentedSeq:
            value = "\n".join(value)
        elif type(value) != str:
            value = str(value)
        value = value.replace("\\n", "\n")
        if rp2 is not None:
            for each in range(len(rp1)):
                value = value.replace(rp1[each], rp2[each])
        return value


def setup(bot):
    bot.add_cog(Main(bot))
