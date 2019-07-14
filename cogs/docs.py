import re
import random
import discord
import sre_yield
from parse import parse


class Docs(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def docs(self, ctx, args):
        if ctx.guild:
            lang = self.bot.lang[self.bot.guildLangs[ctx.guild.id]] if ctx.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]
        mainlang = self.bot.lang[self.bot.config["mainlang"]]
        if not ctx.author.bot:
            if len(args) > 0:
                t = 1
                query = list()
                filters = list()
                while ": " in args:
                    args = args.replace(": ", ":").casefold().replace("i̇", "i")
                for each in args.split(" "):
                    if t == 1:
                        if ":" not in each:
                            query.append(each)
                        else:
                            t += 1
                    if t == 2:
                        if len(each.split(":")) >= 3:
                            await self.send(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["docs"]["errors"]["incorrect-arg"].replace("%error%", each), color=self.bot.get_cog("Main").get_color("error")), ctx.channel, ctx)
                            return
                        elif ":" in each:
                            filters.append(each)
                        else:
                            filters[-1] = filters[-1] + " " + each
                param = {"type": list(), "addon": list(), "contains": list(), "!type": list(), "!addon": list(), "!contains": list()}
                for each in filters:
                    if "type" in lang["docs"]["commands"] and re.fullmatch(lang["docs"]["commands"]["type"], each.split(":")[0]) is not None or re.fullmatch(mainlang["docs"]["commands"]["type"], each.split(":")[0]) is not None:
                        allow = 0
                        for loop in ["event", "condition", "effect", "expression", "type", "function"]:
                            if (each.split(":")[1] in lang["docs"]["types"][loop].casefold().replace("i̇", "i")) or (each.split(":")[1].casefold() in mainlang["docs"]["types"][loop].casefold().replace("i̇", "i")):
                                param["type"].append(loop.casefold())
                                allow = 1
                        if allow == 0:
                            await self.send(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["docs"]["errors"]["incorrect-arg"].replace("%error%", each), color=self.bot.get_cog("Main").get_color("error")), ctx.channel, ctx)
                            return
                    elif (each.startswith("!")) and ("type" in lang["docs"]["commands"] and re.fullmatch(lang["docs"]["commands"]["type"], each.split(":")[0][1:]) is not None or re.fullmatch(mainlang["docs"]["commands"]["type"], each.split(":")[0][1:]) is not None):
                        allow = 0
                        for loop in ["event", "condition", "effect", "expression", "type", "function"]:
                            if (each.split(":")[1] in lang["docs"]["types"][loop].casefold().replace("i̇", "i")) or (each.split(":")[1].casefold() in mainlang["docs"]["types"][loop].casefold().replace("i̇", "i")):
                                param["!type"].append(loop.casefold())
                                allow = 1
                        if allow == 0:
                            await self.send(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["docs"]["errors"]["incorrect-arg"].replace("%error%", each), color=self.bot.get_cog("Main").get_color("error")), ctx.channel, ctx)
                            return
                    elif "addon" in lang["docs"]["commands"] and re.fullmatch(lang["docs"]["commands"]["addon"], each.split(":")[0]) is not None or re.fullmatch(mainlang["docs"]["commands"]["addon"], each.split(":")[0]):
                        param["addon"].append(each.split(":")[1])
                    elif (each.startswith("!")) and ("addon" in lang["docs"]["commands"] and re.fullmatch(lang["docs"]["commands"]["addon"], each.split(":")[0][1:]) is not None or re.fullmatch(mainlang["docs"]["commands"]["addon"], each.split(":")[0][1:])):
                        param["!addon"].append(each.split(":")[1])
                    elif "contains" in lang["docs"]["commands"] and re.fullmatch(lang["docs"]["commands"]["contains"], each.split(":")[0]) is not None or re.fullmatch(mainlang["docs"]["commands"]["contains"], each.split(":")[0]):
                        param["contains"].append(each.split(":")[1])
                    elif (each.startswith("!")) and ("contains" in lang["docs"]["commands"] and re.fullmatch(lang["docs"]["commands"]["contains"], each.split(":")[0][1:]) is not None or re.fullmatch(mainlang["docs"]["commands"]["contains"], each.split(":")[0][1:])):
                        param["!contains"].append(each.split(":")[1])
                    elif "page" in lang["docs"]["commands"] and re.fullmatch(lang["docs"]["commands"]["page"], each.split(":")[0]) is not None or re.fullmatch(mainlang["docs"]["commands"]["page"], each.split(":")[0]):
                        if each.split(":")[1].isdigit():
                            param.update({"page": int(each.split(":")[1])})
                        else:
                            await self.send(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["docs"]["errors"]["incorrect-arg"].replace("%error%", each), color=self.bot.get_cog("Main").get_color("error")), ctx.channel, ctx)
                            return
                    elif "id" in lang["docs"]["commands"] and re.fullmatch(lang["docs"]["commands"]["id"], each.split(":")[0]) is not None or re.fullmatch(mainlang["docs"]["commands"]["id"], each.split(":")[0]):
                        if each.split(":")[1].isdigit():
                            param.update({"id": int(each.split(":")[1])})
                        else:
                            await self.send(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["docs"]["errors"]["incorrect-arg"].replace("%error%", each), color=self.bot.get_cog("Main").get_color("error")), ctx.channel, ctx)
                            return
                    else:
                        await self.send(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["docs"]["errors"]["incorrect-arg"].replace("%error%", each), color=self.bot.get_cog("Main").get_color("error")), ctx.channel, ctx)
                        return
                for each in param:
                    if each != "id":
                        last = list()
                        for filt in param[each]:
                            for i in filt.split(" -- "):
                                last.append(i)
                        param[each] = last
                if len(query) > 0:
                    param.update({"query": " ".join(query)})
                    embed = self.get_docs(param, lang)
                    if embed is not None:
                        msg = await ctx.channel.send(embed=embed["embed"], content=(embed["msg"] if "msg" in embed else None))
                        self.bot.messages.update({msg.id: {"command": self, "user": ctx.author.id, "message": ctx.id, "type": embed["type"], "previous": list()}})
                        if "emotes" in embed:
                            for each in embed["emotes"]:
                                if self.bot.messages[msg.id]["type"] == embed["type"]:
                                    try:
                                        await msg.add_reaction(each)
                                    except (discord.errors.Forbidden, discord.errors.NotFound):
                                        break
                    else:
                        await self.send(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["docs"]["errors"]["no-with-args"], color=self.bot.get_cog("Main").get_color("error")), ctx.channel, ctx)
                else:
                    await self.send(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["docs"]["errors"]["incorrect-usage"].replace("%nl%", "\n"), color=self.bot.get_cog("Main").get_color("error")), ctx.channel, ctx)
                    return
            else:
                await self.send(discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description=lang["docs"]["errors"]["incorrect-usage"].replace("%nl%", "\n"), color=self.bot.get_cog("Main").get_color("error")), ctx.channel, ctx)

    def get_docs(self, param, lang):
        r = list()
        syntax = {}
        j = self.bot.j
        mainlang = self.bot.lang[self.bot.config["mainlang"]]
        id = 0
        if "addon" in param and len(param["addon"]) > 0:
            addon = list()
            addontext = list()
            for each in param["addon"]:
                if re.fullmatch("(s(k(r(i(p(t)?)?)?)?)?)", each.casefold()) is not None:
                    if "skript" not in addon:
                        for loop in self.bot.addonj:
                            if loop.casefold() == "skript":
                                addon.append(loop.casefold())
                                addontext.append("[{}]({})".format(loop, self.bot.addonj[loop]["url"]))
                                break
                else:
                    for loop in self.bot.addonj:
                        if each.casefold() in loop.casefold():
                            if loop.casefold() not in addon:
                                addon.append(loop.casefold())
                                addontext.append("[{}]({})".format(loop, self.bot.addonj[loop]["url"]))
                            break
            if len(addon) == 0:
                return
        if "!addon" in param and len(param["!addon"]) > 0:
            notaddon = list()
            notaddontext = list()
            for each in param["!addon"]:
                if re.fullmatch("(s(k(r(i(p(t)?)?)?)?)?)", each.casefold()) is not None:
                    if "skript" not in notaddon:
                        for loop in self.bot.addonj:
                            if loop.casefold() == "skript":
                                notaddon.append(loop.casefold())
                                notaddontext.append("[{}]({})".format(loop, self.bot.addonj[loop]["url"]))
                                break
                else:
                    for loop in self.bot.addonj:
                        if each.casefold() in loop.casefold():
                            if loop.casefold() not in notaddon:
                                notaddon.append(loop.casefold())
                                notaddontext.append("[{}]({})".format(loop, self.bot.addonj[loop]["url"]))
                            break
            if len(notaddon) == 0:
                return
        charsyntax = {"event": 0, "condition": 0, "effect": 0, "expression": 0, "type": 0, "function": 0}
        charid = {}
        for count in range(len(j)):
            if param["query"] != "*":
                cont = 0
                for each in param["query"].split(" "):
                    if not ((each.casefold() in j[count]["title"].casefold()) or (("description" in j[count]) and (each.casefold() in j[count]["description"].casefold())) or (each.casefold() in j[count]["syntax_pattern"].casefold())):
                        cont = 1
                        break
                if cont == 1:
                    continue
            if "type" in param and len(param["type"]) > 0:
                if j[count]["syntax_type"].casefold() not in param["type"]:
                    continue
            elif "!type" in param and len(param["!type"]) > 0:
                if j[count]["syntax_type"].casefold() in param["!type"]:
                    continue
            if "addon" in param and len(param["addon"]) > 0:
                if j[count]["addon"]["name"].casefold() not in addon:
                    continue
            elif "!addon" in param and len(param["!addon"]) > 0:
                if j[count]["addon"]["name"].casefold() in notaddon:
                    continue
            if "contains" in param and len(param["contains"]) > 0:
                cont = 0
                for each in param["contains"]:
                    if not ((each.casefold() in j[count]["title"].casefold()) or (("description" in j[count]) and (each.casefold() in j[count]["description"].casefold())) or (each.casefold() in j[count]["syntax_pattern"].casefold())):
                        cont = 1
                        break
                if cont == 1:
                    continue
            elif "!contains" in param and len(param["!contains"]) > 0:
                cont = 0
                for each in param["!contains"]:
                    if (each.casefold() in j[count]["title"].casefold()) or (("description" in j[count]) and (each.casefold() in j[count]["description"].casefold())) or (each.casefold() in j[count]["syntax_pattern"].casefold()):
                        cont = 1
                        break
                if cont == 1:
                    continue
            id += 1
            r.append(count)
            if j[count]["syntax_type"] in syntax:
                sy = syntax[j[count]["syntax_type"]]
            else:
                sy = list()
            if "char" in param:
                charid.update({j[count]["syntax_type"]: count})
                charsyntax.update({j[count]["syntax_type"]: charsyntax[j[count]["syntax_type"]] + 1})
                if "addon" in locals() and len(addon) == 1:
                    sy.append("[{}] {}".format(charsyntax[j[count]["syntax_type"]], j[count]["title"]))
                else:
                    sy.append("[{}] {} #{}".format(charsyntax[j[count]["syntax_type"]], j[count]["title"], j[count]["addon"]["name"]))
            else:
                if "addon" in locals() and len(addon) == 1:
                    sy.append("[{}] {}".format(id, j[count]["title"]))
                else:
                    sy.append("[{}] {} #{}".format(id, j[count]["title"], j[count]["addon"]["name"]))
            syntax.update({j[count]["syntax_type"]: sy})
            if ("id" in param) and ("char" not in param):
                if id == param["id"]:
                    sel_id = count
                    break
        desc = [("**{}:** {}".format(lang["docs"]["query"], param["query"])) if param["query"] != "*" else ("**{}:** \\*{}\\*".format(lang["docs"]["query"], lang["docs"]["everything"]))]
        cmd = [param["query"]]
        if "type" in param and len(param["type"]) > 0:
            types = []
            for each in param["type"]:
                types.append(lang["docs"]["types"][each])
            desc.append("**{}:** {}".format(lang["docs"]["type"], " - ".join(types)))
            cmd.append(mainlang["docs"]["commands"]["command-field"]["type"] + ":" + " -- ".join(param["type"]))
        elif "!type" in param and len(param["!type"]) > 0:
            types = []
            for each in param["!type"]:
                types.append(lang["docs"]["types"][each])
            desc.append("**!{}:** {}".format(lang["docs"]["type"], " - ".join(types)))
            cmd.append("!" + mainlang["docs"]["commands"]["command-field"]["type"] + ":" + " -- ".join(param["!type"]))
        elif "char" in param:
            desc.append("**{}:** {}".format(lang["docs"]["type"], lang["docs"]["types"][next(iter(syntax))]))
        if "contains" in param and len(param["contains"]) > 0:
            desc.append("**{}:** {}".format(lang["docs"]["contains"], " - ".join(param["contains"])))
            cmd.append(mainlang["docs"]["commands"]["command-field"]["contains"] + ":" + " -- ".join(param["contains"]))
        if "!contains" in param and len(param["!contains"]) > 0:
            desc.append("**!{}:** {}".format(lang["docs"]["contains"], " - ".join(param["!contains"])))
            cmd.append("!" + mainlang["docs"]["commands"]["command-field"]["contains"] + ":" + " -- ".join(param["!contains"]))
        if "addon" in param and len(param["addon"]) > 0:
            desc.append("**{}:** {}".format(lang["docs"]["addon"], " - ".join(addontext)))
            cmd.append(mainlang["docs"]["commands"]["command-field"]["addon"] + ":" + " -- ".join(addon))
        elif "!addon" in param and len(param["!addon"]) > 0:
            desc.append("**!{}:** {}".format(lang["docs"]["addon"], " - ".join(notaddontext)))
            cmd.append("!" + mainlang["docs"]["commands"]["command-field"]["addon"] + ":" + " -- ".join(notaddon))
        if ("page" in param) and (param["page"] >= 1) and (len(syntax) == 1):
            if param["page"] == 9999:
                page = int((len(syntax[next(iter(syntax))]) - 1) / 10) + 1
            else:
                page = param["page"]
        else:
            page = 1
        if len(syntax) == 1:
            desc.append("**{}:** {}/{}".format(lang["docs"]["page"], page, int((len(syntax[next(iter(syntax))]) - 1) / 10) + 1))
        if len(syntax) == 0:
            embed = discord.Embed(title="❌ {}".format(lang["errors"]["title"]), description="\n".join(desc) + "\n\n" + lang["docs"]["errors"]["no-with-args"], color=self.bot.get_cog("Main").get_color("error"))
            return {"embed": embed, "emotes": ["❌"], "type": 0}
        count = 0
        if "char" in param:
            if param["char"] > len(syntax):
                return
            for each in ["event", "condition", "effect", "expression", "type", "function"]:
                if each in syntax:
                    count += 1
                    if param["char"] == count:
                        syntax = {each: syntax[each]}
                        param.update({"type": [each]})
                        break
        if (id == 1) or ("sel_id" in locals()) or ("char" in param and len(syntax) == 1 and len(syntax[next(iter(syntax))]) == 1):
            old = id
            if "sel_id" in locals():
                id = sel_id
            elif "char" in param and len(syntax) == 1 and len(syntax[next(iter(syntax))]) == 1:
                id = charid[next(iter(syntax))]
            else:
                id = r[0]
            desc = []
            if j[id]["syntax_type"] == "event":
                if "event_cancellable" in j[id]:
                    if j[id]["event_cancellable"]:
                        desc.append("**{}:** {} **(**{}**)**".format(lang["docs"]["type"], lang["docs"]["types"]["event"], lang["docs"]["code"]["cancellable"]))
                    else:
                        desc.append("**{}:** {} **(**{}**)**".format(lang["docs"]["type"], lang["docs"]["types"]["event"], lang["docs"]["code"]["uncancellable"]))
                else:
                    desc.append("**{}:** {}".format(lang["docs"]["type"], lang["docs"]["types"]["event"]))
            else:
                desc.append("**{}:** {}".format(lang["docs"]["type"], lang["docs"]["types"][j[id]["syntax_type"]]))
            desc.append("**{}:** [{}]({})".format(lang["docs"]["addon"], j[id]["addon"]["name"], j[id]["addon"]["link_to_addon"]))
            embed = discord.Embed(title="{} {} | {}: {} ({})".format(lang["docs"]["emote"], lang["docs"]["title"], lang["docs"]["info"], j[id]["title"], id + 1), description="\n".join(desc), color=self.bot.get_cog("Main").get_color("docs"))
            if ("description" in j[id]) and (j[id]["description"] != "") and (j[id]["description"] is not None):
                for each in self.split_fields(j[id]["description"]):
                    embed.add_field(name=(lang["docs"]["code"]["description"] if "added1" not in locals() else "‎"), value=each, inline=False)
                    added1 = 1
            for each in self.split_fields(j[id]["syntax_pattern"]):
                embed.add_field(name=(lang["docs"]["code"]["patterns"] if "added2" not in locals() else "‎"), value="```vb\n{}\n```".format(each), inline=False)
                added2 = 1
            if j[id]["syntax_type"] != "type":
                e = self.gen_random(random.choice(j[id]["syntax_pattern"].split("\n")))
                if e is not None and j[id]["syntax_type"] == "event" and e[-1] != ":":
                    e = "{}:".format(e)
                if ("examples" in j[id]) and (j[id]["examples"] != "") and (j[id]["examples"] is not None):
                    if e is not None:
                        ex = "{}\n# ^ {}\n\n{}".format(e, lang["docs"]["code"]["random-code"], j[id]["examples"])
                    else:
                        ex = j[id]["examples"]
                elif e is not None:
                    ex = "{}\n# ^ {}".format(e, lang["docs"]["code"]["random-code"])
                if "ex" in locals():
                    for each in self.split_fields(ex):
                        embed.add_field(name=(lang["docs"]["code"]["examples"] if "added3" not in locals() else "‎"), value="```vb\n{}\n```".format(each), inline=False)
                        added3 = 1
            if (j[id]["syntax_type"] == "event") and ("event_values" in j[id]) and (j[id]["event_values"] != "") and (j[id]["event_values"] is not None):
                embed.add_field(name=lang["docs"]["code"]["event-values"], value="```vb\n{}\n```".format("\n".join(j[id]["event_values"].split(", "))), inline=False)
            elif (j[id]["syntax_type"] == "type") and ("type_usage" in j[id]) and (j[id]["type_usage"] != "") and (j[id]["type_usage"] is not None):
                embed.add_field(name=lang["docs"]["code"]["type-usage"], value="```vb\n{}\n```".format(j[id]["type_usage"])[:1016], inline=False)
            elif (j[id]["syntax_type"] == "expression") and ("return_type" in j[id]) and (j[id]["return_type"] != "") and (j[id]["return_type"] is not None):
                embed.add_field(name=lang["docs"]["code"]["return-type"], value=j[id]["return_type"])
            if ("compatible_addon_version" in j[id]) and (j[id]["compatible_addon_version"] != "") and (j[id]["compatible_addon_version"] is not None):
                embed.add_field(name=lang["docs"]["code"]["version"], value=j[id]["compatible_addon_version"])
            if ("required_plugins" in j[id]) and (j[id]["required_plugins"] is not None) and (len(j[id]["required_plugins"]) != 0):
                plugins = []
                for each in j[id]["required_plugins"]:
                    plugins.append("[{}]({})".format(each["name"], each["link"]))
                embed.add_field(name=lang["docs"]["code"]["required-plugins"], value=" - ".join(plugins))
            if "id" in j[id]:
                embed.add_field(name=lang["docs"]["link"], value="https://skripthub.net/docs/?id={}".format(j[id]["id"]))
            if old == 1 and "id" not in param:
                return {"embed": embed, "msg": lang["docs"]["only-one"], "emotes": ["❌"], "type": 3}
            return {"embed": embed, "emotes": ["❌"], "type": 3}
        if "id" in param:
            return
        if len(syntax) == 1:
            perpage = 10
        elif (len(syntax) == 2) or (len(syntax) == 3):
            perpage = 5
        elif (len(syntax) == 4) or (len(syntax) == 5):
            perpage = 3
        else:
            perpage = 2
        embed = discord.Embed(title="{} {}".format(lang["docs"]["emote"], lang["docs"]["title"]), description="\n".join(desc), color=self.bot.get_cog("Main").get_color("docs"))
        count = 0
        for each in ["event", "condition", "effect", "expression", "type", "function"]:
            if (each in syntax) and (len(syntax[each]) + 10 > perpage * page):
                if len(syntax) != 1:
                    count += 1
                    if count == 1:
                        emote = "\U0001f1e6"
                    elif count == 2:
                        emote = "\U0001F1e7"
                    elif count == 3:
                        emote = "\U0001f1e8"
                    elif count == 4:
                        emote = "\U0001f1e9"
                    elif count == 5:
                        emote = "\U0001f1ea"
                    elif count == 6:
                        emote = "\U0001f1eb"
                    embed.add_field(name="{} ({})".format(lang["docs"]["types-plural"]["{}s".format(each)], emote), value=("```vb\n{}\n+{}\n```".format("\n".join(syntax[each][page * perpage - (perpage - 1) - 1:page * perpage]), len(syntax[each]) - perpage * page)) if len(syntax[each]) > perpage * page else ("```vb\n{}\n```".format("\n".join(syntax[each][page * perpage - (perpage - 1) - 1:page * perpage]))), inline=False)
                else:
                    embed.add_field(name=lang["docs"]["types-plural"]["{}s".format(each)], value=("```vb\n{}\n+{}\n```".format("\n".join(syntax[each][page * perpage - (perpage - 1) - 1:page * perpage]), len(syntax[each]) - perpage * page)) if len(syntax[each]) > perpage * page else ("```vb\n{}\n```".format("\n".join(syntax[each][page * perpage - (perpage - 1) - 1:page * perpage]))), inline=False)
        embed.add_field(name=lang["docs"]["command-field"], value=mainlang["docs"]["commands"]["command-field"]["main"] + " " + " ".join(cmd))
        if len(syntax) > 0:
            if len(syntax) == 1:
                if int((len(syntax[next(iter(syntax))]) - 1) / 10) + 1 == 1:
                    emotes = ["❌"]
                else:
                    emotes = ["\U000023EE", "\U000025C0", "❌", "\U000025B6", "\U000023ED"]
                for each in range(len(syntax[next(iter(syntax))])):
                    if each == 0:
                        emotes.append("1\u20e3")
                    elif each == 1:
                        emotes.append("2\u20e3")
                    elif each == 2:
                        emotes.append("3\u20e3")
                    elif each == 3:
                        emotes.append("4\u20e3")
                    elif each == 4:
                        emotes.append("5\u20e3")
                    elif each == 5:
                        emotes.append("6\u20e3")
                    elif each == 6:
                        emotes.append("7\u20e3")
                    elif each == 7:
                        emotes.append("8\u20e3")
                    elif each == 8:
                        emotes.append("9\u20e3")
                    elif each == 9:
                        emotes.append("\U0001f51f")
                return {"embed": embed, "emotes": emotes, "type": 2}
            else:
                emotes = []
                emotes.append("❌")
                for each in range(len(syntax)):
                    if each == 0:
                        emotes.append("\U0001f1e6")
                    elif each == 1:
                        emotes.append("\U0001F1e7")
                    elif each == 2:
                        emotes.append("\U0001f1e8")
                    elif each == 3:
                        emotes.append("\U0001f1e9")
                    elif each == 4:
                        emotes.append("\U0001f1ea")
                    elif each == 5:
                        emotes.append("\U0001f1eb")
                return {"embed": embed, "emotes": emotes, "type": 1}
        else:
            return

    def split_fields(self, text):
        rlist = []
        ret = []
        for each in text.split("\n"):
            rlist.append(each)
            if len("\n".join(rlist)) + 10 > 1024:
                if len(rlist[-1]) > 1014:
                    return [text[i:i + 1014] for i in range(0, len(text), 1014)]
                ret.append("\n".join(rlist[:-1]))
                rlist = [each]
        ret.append("\n".join(rlist))
        return ret

    @discord.ext.commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        messages = self.bot.messages

        if msg.author != self.bot.user or user == self.bot.user or msg.id not in messages or messages[msg.id]["command"] != self:
            return

        if msg.guild:
            lang = self.bot.lang[self.bot.guildLangs[msg.guild.id]] if msg.guild.id in self.bot.guildLangs else self.bot.lang[self.bot.config["mainlang"]]
        else:
            lang = self.bot.lang[self.bot.config["mainlang"]]

        try:
            await msg.remove_reaction(reaction, user)
        except (discord.errors.Forbidden, discord.errors.NotFound):
            pass

        if not user.bot and messages[msg.id]["command"] == self and (messages[msg.id]["user"] == user.id or msg.channel.permissions_for(user).manage_guild):
            if str(reaction) == "❌":
                try:
                    delete_msg = await msg.channel.fetch_message(messages[msg.id]["message"])
                    await delete_msg.delete()
                except (discord.errors.Forbidden, discord.errors.NotFound):
                    pass
                try:
                    await msg.delete()
                except (discord.errors.Forbidden, discord.errors.NotFound):
                    pass
                messages.pop(msg.id)
                return
            if messages[msg.id]["type"] == 0:
                return
            param = {"type": [], "addon": [], "contains": [], "!type": [], "!addon": [], "!contains": []}
            for each in msg.embeds[0].description.split("\n"):
                if each.startswith("**{}:** ".format(lang["docs"]["query"])):
                    if each[len(lang["docs"]["query"]) + 6:] == "\\*{}\\*".format(lang["docs"]["everything"]):
                        param.update({"query": "*"})
                    else:
                        param.update({"query": each[len(lang["docs"]["query"]) + 6:]})
                elif each.startswith("**{}:** ".format(lang["docs"]["addon"])):
                    for addon in each[len(lang["docs"]["addon"]) + 6:].split(" - "):
                        param["addon"].append(parse("[{}]({})", addon)[0])
                elif each.startswith("**!{}:** ".format(lang["docs"]["addon"])):
                    for addon in each[len(lang["docs"]["addon"]) + 7:].split(" - "):
                        param["!addon"].append(parse("[{}]({})", addon)[0])
                elif each.startswith("**{}:** ".format(lang["docs"]["type"])):
                    for sy_type in each[len(lang["docs"]["type"]) + 6:].split(" - "):
                        for loop in lang["docs"]["types"]:
                            if lang["docs"]["types"][loop] == sy_type:
                                param["type"].append(loop)
                elif each.startswith("**!{}:** ".format(lang["docs"]["type"])):
                    for sy_type in each[len(lang["docs"]["type"]) + 7:].split(" - "):
                        for loop in lang["docs"]["types"]:
                            if lang["docs"]["types"][loop] == sy_type:
                                param["!type"].append(loop)
                elif each.startswith("**{}:** ".format(lang["docs"]["page"])):
                    param.update({"page": int(each[len(lang["docs"]["page"]) + 6:].split("/")[0])})
                elif each.startswith("**{}:** ".format(lang["docs"]["contains"])):
                    for loop in each[len(lang["docs"]["contains"]) + 6:].split(" - "):
                        param["contains"].append(loop)
                elif each.startswith("**!{}:** ".format(lang["docs"]["contains"])):
                    for loop in each[len(lang["docs"]["contains"]) + 7:].split(" - "):
                        param["!contains"].append(loop)
            param_raw = param.copy()
            if messages[msg.id]["type"] == 1:
                if str(reaction) == "\U0001f1e6":
                    param.update({"char": 1})
                elif str(reaction) == "\U0001f1e7":
                    param.update({"char": 2})
                elif str(reaction) == "\U0001f1e8":
                    param.update({"char": 3})
                elif str(reaction) == "\U0001f1e9":
                    param.update({"char": 4})
                elif str(reaction) == "\U0001f1ea":
                    param.update({"char": 5})
                elif str(reaction) == "\U0001f1eb":
                    param.update({"char": 6})
            if messages[msg.id]["type"] == 2:
                if str(reaction) == "\U000023EE":
                    param.update({"page": 1})
                elif str(reaction) == "\U000025C0":
                    param.update({"page": param["page"] - 1})
                elif str(reaction) == "\U000025B6":
                    param.update({"page": param["page"] + 1})
                elif str(reaction) == "\U000023ED":
                    param.update({"page": 9999})
                elif str(reaction) == "1\u20e3":
                    param.update({"id": param["page"] * 10 - 9})
                elif str(reaction) == "2\u20e3":
                    param.update({"id": param["page"] * 10 - 8})
                elif str(reaction) == "3\u20e3":
                    param.update({"id": param["page"] * 10 - 7})
                elif str(reaction) == "4\u20e3":
                    param.update({"id": param["page"] * 10 - 6})
                elif str(reaction) == "5\u20e3":
                    param.update({"id": param["page"] * 10 - 5})
                elif str(reaction) == "6\u20e3":
                    param.update({"id": param["page"] * 10 - 4})
                elif str(reaction) == "7\u20e3":
                    param.update({"id": param["page"] * 10 - 3})
                elif str(reaction) == "8\u20e3":
                    param.update({"id": param["page"] * 10 - 2})
                elif str(reaction) == "9\u20e3":
                    param.update({"id": param["page"] * 10 - 1})
                elif str(reaction) == "\U0001f51f":
                    param.update({"id": param["page"] * 10})
            if str(reaction) == "\U000021a9":
                if len(messages[msg.id]["previous"]) == 0:
                    return
                param = messages[msg.id]["previous"][-1]
                messages[msg.id].update({"previous": messages[msg.id]["previous"][:-1]})
            if param != param_raw:
                embed = self.get_docs(param, lang)
                if embed is not None:
                    await msg.edit(embed=embed["embed"])
                    if embed["type"] != messages[msg.id]["type"]:
                        messages[msg.id].update({"type": embed["type"]})
                        try:
                            await msg.clear_reactions()
                        except (discord.errors.Forbidden, discord.errors.NotFound):
                            pass
                        if str(reaction) != "\U000021a9":
                            messages[msg.id]["previous"].append(param_raw)
                        if len(messages[msg.id]["previous"]) != 0:
                            try:
                                await msg.add_reaction("\U000021a9")
                            except (discord.errors.Forbidden, discord.errors.NotFound):
                                pass
                        for each in embed["emotes"]:
                            if messages[msg.id]["type"] == embed["type"]:
                                try:
                                    await msg.add_reaction(each)
                                except (discord.errors.Forbidden, discord.errors.NotFound):
                                    break

    def gen_random(self, syntax):
        try:
            f = parse("{}({})", syntax)
            syntax = syntax.replace("%*", "%").replace("%~", "%").replace("%^", "%").replace("%-", "%").replace("[<", "[").replace(">]", "]")
            if (f is None) or (":" not in syntax) or (syntax[-1] != ")") or (syntax[0] == "(") or (len(syntax.split(")")) != 2) or (len(syntax.split("(")) != 2):
                c = 0
                ret = []
                for each in random.choice(sre_yield.AllStrings((syntax.replace("[", "(").replace("]", ")?")))).split("%"):
                    c += 1
                    if c % 2 == 0:
                        ret.append("{{_{}{}}}".format(random.choice(each.split("/")), "" if each[-1] != "s" else "::*"))
                    else:
                        ret.append(each)
                x = "".join(ret)
                while "  " in x:
                    x = x.replace("  ", " ")
                while x[0] == " ":
                    x = x[1:]
                while x[-1] == " ":
                    x = x[:-1]
                return x
            else:
                rlist = []
                for each in f[1].split(", "):
                    if parse("{} = [[{}:{}]]", each.split(": ")[1]) is not None:
                        rlist.append("{{_{}}}".format(parse("{} = [[{}:{}]]", each.split(": ")[1])[1]))
                    else:
                        rlist.append("{{_{}}}".format(each.split(": ")[1]))
                return "{}({})".format(f[0], ", ".join(rlist))
        except re.error:
            return

    async def send(self, embed, channel, message):
        msg = await channel.send(embed=embed)
        self.bot.messages.update({msg.id: {"command": self, "type": 0, "user": message.author.id, "message": message.id}})
        try:
            await msg.add_reaction("❌")
        except (discord.errors.Forbidden, discord.errors.NotFound):
            pass


def setup(bot):
    bot.add_cog(Docs(bot))
