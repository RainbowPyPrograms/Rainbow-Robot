import discord
from discord.ext import commands
import os
import jishaku
from asyncdagpi import Client

async def get_prefix(client, message):
    if message.guild is None:
        prefixes = ["Rainbow ", "rr.", "rainbow "]
    elif message.author.id == 688293803613880334:
        prefixes = ["Rainbow ", "rr.", "rainbow ", ""]
    else:
        prefixes = ["Rainbow ", "rr.", "rainbow "]

    return commands.when_mentioned_or(*prefixes)(client, message)

intents = discord.Intents.all()

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True,description='This is a multi-purpose bot for servers with fun commands', intents=intents)

client.dagpi = Client("")
# if you want to use dagpi api put your token in the "" else just remove line 21
jsk = client.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
jsk = client.reload_extension("jishaku")
@client.event
async def on_ready():
    print(f'Main file Opened by bot consists basics.')

@client.command(hidden=False)
@commands.is_owner()
async def load(ctx, extension):
    message = ctx.message
    client.load_extension(f'cogs.{extension}')
    await message.add_reaction('<:greenTick:596576670815879169>')

@client.command(hidden=False)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    message = ctx.message
    await message.add_reaction('<:greenTick:596576670815879169>')
# a cog reloader command
@client.command(hidden=False)
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    message = ctx.message
    await message.add_reaction('<:greenTick:596576670815879169>')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('')
# your token 
