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
        if msg.content.casefold().startswith("!sk ") or msg.content.casefold().startswith("{} ".format(self.bot.user.mention)):
            cmd = msg.content.split()[1].casefold()
            args = msg.content.split()[2:]
            if re.fullmatch(lang["docs"]["commands"]["main"], cmd) is not None or re.fullmatch(mainlang["docs"]["commands"]["main"], cmd) is not None:
                await self.bot.get_cog("Docs").docs(msg, " ".join(args))
            elif re.fullmatch(lang["downloads"]["commands"]["main"], cmd) is not None or re.fullmatch(mainlang["downloads"]["commands"]["main"], cmd) is not None:
                await self.bot.get_cog("Download").download(msg, args)
            elif re.fullmatch(lang["names"]["command"], cmd) is not None or re.fullmatch(mainlang["names"]["command"], cmd) is not None:
                await self.bot.get_cog("Names").names(msg, " ".join(args))
            elif re.fullmatch(lang["help"]["command"], cmd) is not None or re.fullmatch(mainlang["help"]["command"], cmd) is not None:
                await self.bot.get_cog("Help").help(msg)
            elif re.fullmatch(lang["info"]["command"], cmd) is not None or re.fullmatch(mainlang["info"]["command"], cmd) is not None:
                await self.bot.get_cog("Info").info(msg)
            elif cmd == "yamlparse":
                await self.bot.get_cog("Parsing").yamlparse(msg, " ".join(args))
            elif cmd == "jsonparse":
                await self.bot.get_cog("Parsing").jsonparse(msg, " ".join(args))
            elif cmd == "jsonbeautify":
                await self.bot.get_cog("Parsing").jsonbeautify(msg, " ".join(args))
            elif cmd == "lang" or cmd == "language":
                await self.bot.get_cog("Lang").lang(msg, " ".join(args))
            elif cmd == "eval":
                await self.bot.get_cog("Admin").eval(msg, " ".join(args))
            elif cmd == "reload" or cmd == "rel" or cmd == "rl":
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
