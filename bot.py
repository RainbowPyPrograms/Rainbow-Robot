import discord
print('imported discord')
from discord.ext import commands
print('imported commands from discord.ext')
import os
print('imported os')
import json
print('imported json')
import jishaku
print('imported jishaku')
import random
print('imported random')
from datetime import datetime
import asyncio
import humanize

class CustomEmbed(discord.Embed):


    def __init__(self, *a, **kw):
        super().__init__(color=0x2F3136, *a, **kw)

load_time = datetime.utcnow()

async def get_prefix(client, message):
    if message.guild is None:
        prefixes = ["Rainbow ", "hi ", "rainbow "]
    elif message.author.id == 688293803613880334:
        prefixes = ["Rainbow ", "hi ", "rainbow ", ""]
    else:
        prefixes = ["Rainbow ", "hi ", "rainbow "]

    return commands.when_mentioned_or(*prefixes)(client, message)

intents = discord.Intents.all()

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True,description='This is a multi-purpose bot for servers with fun commands', intents=intents)

def callable_pref(bot, message):
  ## so stuff to load your prefixes
  # where `prefix_return` is a string or list of strings
  # in my case it's this:
    prefix_return = ["rr."]
    return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)

jsk = client.load_extension("jishaku")

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

@reload.error
async def r_handler(ctx, error):
    message = ctx.message
    await message.remove_reaction('<:greenTick:596576670815879169>', ctx.guild.me)
    await message.add_reaction('<:redTick:596576672149667840>')
    await ctx.send(embed=discord.Embed(title='Exception caught:', description=f'{error}'))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
x = input('Token:')
client.run(x)
