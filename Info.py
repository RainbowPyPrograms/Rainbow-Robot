import discord
from discord.ext import commands
from .utils import checks, formats
from collections import OrderedDict, deque, Counter
from datetime import datetime
import humanize
import psutil
import time
"""A simple cog example with simple commands. Showcased here are some check decorators, and the use of events in cogs.
For a list of inbuilt checks:
http://dischttp://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checks
You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689
For a list of events:
http://discordpy.readthedocs.io/en/rewrite/api.html#event-reference
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#event-reference
"""
load_time = datetime.utcnow()
class info(commands.Cog):
    """SimpleCog"""

    def __init__(self, client):
        self.client = client


    @commands.command(alais=['si', 'gi', 'guildinfo'])
    async def serverinfo(self, ctx, *, guild_id: int = None):
        guild = guild_id or ctx.guild
        member_by_status = Counter(str(m.status) for m in guild.members)
        if guild.description is None:
            x = "-"
        else:
            x = guild.description
        embed = discord.Embed(title=guild.name, description=x)
        embed.add_field(name="Region:", value=f'{guild.region}')
        embed.add_field(name='Id', value=f'{guild.id}')
        embed.add_field(name='Owner', value=f'<@{guild.owner_id}>')
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        x = await self.client.fetch_user(782229285611372545)
        proc = psutil.Process()
        mem = proc.memory_full_info()
        embed = discord.Embed(title=f'{ctx.command.name}', description=f'{ctx.bot.description}.\nNote: My prefix is *"hi "*')
        embed.add_field(name='Info:', value=f'<:member_join:596576726163914752> **Developer -** [Rainbow](https://discord.com/users/688293803613880334)\n<:member_join:596576726163914752> **Library -** [discord.py](https://pypi.org/project/discord.py/)\n<:member_join:596576726163914752> **Last Boot -** {humanize.naturaltime(load_time - datetime.utcnow())}\n<:member_join:596576726163914752> **Created - ** {humanize.naturaltime(x.created_at)}')
        embed.add_field(name='Stats:', value=f'<:member_join:596576726163914752> **Number of commands -** {len(self.client.commands)}\n<:member_join:596576726163914752> **Guilds -** {len(list(map(str, [p.id for p in self.client.guilds])))}\n<:member_join:596576726163914752> **Users -** {len(list(map(str, [p.id for p in self.client.users])))}\n<:member_join:596576726163914752> **System -** {humanize.naturalsize(mem.uss)} / 2048 MB')
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send("Pinging...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        embed = discord.Embed(title='Ping:')
        embed.add_field(name='<:001download:783296618718953543> | Websocket:', value=f'{round(self.client.latency * 1000)}ms')
        embed.add_field(name='<a:typing:597589448607399949> | Typing:', value=f'{round(duration)}ms')
        await message.edit(embed=embed)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(embed=discord.Embed(title='Hi', description=f'I am [{self.client.user.name}](https://discord.com/users/782229285611372545), [{self.client.owner.name}](https://discord.com/users/688293803613880334) made me.'))

    @commands.command()
    async def uptime(self, ctx):
        x = load_time - datetime.utcnow()
        y = humanize.precisedelta(x, minimum_unit="seconds")
        """Tells you how long the bot has been up for."""
        await ctx.send(embed=discord.Embed(title=ctx.command.name, description=f'Uptime: **{y}**'))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if await self.client.is_owner(before.author):
            await self.client.process_commands(after)

def setup(client):
    client.add_cog(info(client))