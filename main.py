import os
import requests
import json
import discord
from os.path import isfile, join
from datetime import datetime
from aioconsole import ainput
from ruamel.yaml import YAML
from discord.ext import commands


async def console():
    cmd = await ainput(">>> ")
    if cmd.replace(" ", "") != "":
        if cmd.startswith("reload"):
            try:
                bot.get_cog('Admin').rel()
            except Exception as e:
                print("Caught an error while reloading skDocs!\n{}".format(e))
            else:
                print("skDocs has been reloaded successfully.")
        elif cmd.startswith("help"):
            print("reload -> Reloads skDocs")
        else:
            print("Unknown command. Type help")
    await console()


def docs(t1, t2, cv, sv):
    if t1 in cv:
        if type(cv[t1]) == list:
            sv.update({t2: "\n".join(cv[t1])})
        else:
            sv.update({t2: cv[t1]})
    return sv


print("Starting skDocs...")
yaml = YAML()
bot = discord.ext.commands.Bot(command_prefix="")
bot.remove_command("help")
bot.messages = {}
print("Loading cogs...")
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
    bot.load_extension(f'cogs.{each}')
print("Getting langs, config, downloads, guild and names...")
bot.get_cog("Admin").rel(False)
print("Sending requests...")
a = json.loads(requests.get('https://skripthub.net/api/v1/addon/', headers={'Authorization': 'Token {}'.format(bot.config["skripthub"]["token"])}).text)
bot.addonj = {}
blacklisted = bot.config["skripthub"]["blacklisted_addons"]
if type(blacklisted) == str:
    if blacklisted == "none":
        blacklisted = []
    else:
        blacklisted = [blacklisted.casefold()]
else:
    blacklisted = list(map(str.casefold, blacklisted))
    if blacklisted[0] == "none":
        blacklisted = []
for each in a:
    if each["name"].casefold() not in blacklisted:
        bot.addonj.update({each["name"]: {"url": each["url"], "skripthub": True}})
examples = json.loads(requests.get('https://skripthub.net/api/v1/syntaxexample/', headers={'Authorization': 'Token {}'.format(bot.config["skripthub"]["token"])}).text)
adds = json.loads(requests.get('http://skripthub.net/api/v1/addonsyntaxlist/', headers={'Authorization': bot.config["skripthub"]["token"]}).text)
bot.j = []
with open("downloads.yml", "r", encoding="utf-8-sig") as stream:
    addons = yaml.load(stream)
if "addons" in addons["downloads"]:
    for each in addons["downloads"]["addons"]:
        if each in bot.addonj:
            if type(addons["downloads"]["addons"][each]) == str:
                bot.addonj.update({each: {"url": addons["downloads"]["addons"][each], "skripthub": True}})
        else:
            bot.addonj.update({each: {"url": addons["downloads"]["addons"][each], "skripthub": False}})
print("Creating syntax list...")
for each in adds:
    if each["addon"]["name"].casefold() not in blacklisted:
        ex = []
        for example in examples:
            if each["id"] == example["syntax_element"]:
                ex.append(example["example_code"])
        if len(ex) != 0:
            each.update({"examples": "\n\n".join(ex)})
        bot.j.append(each)
print("Getting custom addons...")
try:
    for each in [f for f in os.listdir("custom") if isfile(join("custom", f))]:
        if each[-5:] == ".json":
            with open("custom/{}".format(each), "r", encoding="utf-8-sig") as stream:
                a = json.loads(stream.read())
                for loop in a:
                    for loop2 in a[loop]:
                        ad = {"syntax_type": loop[:-1], "addon": {"name": each[:-5], "link_to_addon": bot.addonj[each[:-5]]["url"]}}
                        docs("title", "title", loop2, ad)
                        docs("name", "title", loop2, ad)
                        docs("desc", "description", loop2, ad)
                        docs("description", "description", loop2, ad)
                        docs("syntaxes", "syntax_pattern", loop2, ad)
                        docs("patterns", "syntax_pattern", loop2, ad)
                        docs("syntax pattern", "syntax_pattern", loop2, ad)
                        docs("syntax-pattern", "syntax_pattern", loop2, ad)
                        docs("syntax_pattern", "syntax_pattern", loop2, ad)
                        docs("example", "examples", loop2, ad)
                        docs("examples", "examples", loop2, ad)
                        docs("eventvalues", "event_values", loop2, ad)
                        docs("event values", "event_values", loop2, ad)
                        docs("event_values", "event_values", loop2, ad)
                        docs("event-values", "event_values", loop2, ad)
                        docs("returntype", "return_type", loop2, ad)
                        docs("return type", "return_type", loop2, ad)
                        docs("return_type", "return_type", loop2, ad)
                        docs("return-type", "return_type", loop2, ad)
                        docs("since", "compatible_addon_version", loop2, ad)
                        docs("compatible_addon_version", "compatible_addon_version", loop2, ad)
                        docs("addon version", "compatible_addon_version", loop2, ad)
                        docs("addon-version", "compatible_addon_version", loop2, ad)
                        docs("addon_version", "compatible_addon_version", loop2, ad)
                        docs("version", "compatible_addon_version", loop2, ad)
                        docs("event_cancellable", "event_cancellable", loop2, ad)
                        docs("cancellable", "event_cancellable", loop2, ad)
                        bot.j.append(ad)
except Exception as e:
    print('Custom addons error: {}'.format(e))
for each in bot.guilds:
    if each.id not in bot.guildLangs:
        bot.guildLangs.update({each.id: bot.config["mainlang"]})
with open("guilds.yml", "w") as f:
    yaml.dump(bot.guildLangs, stream=f)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(bot.config["status"]))
    bot.start = datetime.utcnow()
    print("skDocs has been loaded successfully!")
    await console()


bot.run(bot.config["token"])
