import discord
from discord.ext import commands
from datetime import datetime
import humanize
import psutil
import time
import inspect
import os
import io
import re
import zlib
from .utils import Fuzzy as fuzzy
import mystbin
from discord.ext.commands.cooldowns import BucketType
import prettify_exceptions
import mystbin
load_time = datetime.utcnow()
mystbin_client = mystbin.Client()
import aiohttp
class Context(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pool = self.bot.pool
        self._db = None

    @property
    def session(self):
        return self.bot.session

class SphinxObjectFileReader:
    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode('utf-8')

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b''
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b'\n')
            while pos != -1:
                yield buf[:pos].decode('utf-8')
                buf = buf[pos + 1:]
                pos = buf.find(b'\n')

class Info(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.bot = client
        self.bot.session = aiohttp.ClientSession()

    def parse_object_inv(self, stream, url):
        # key: URL
        # n.b.: key doesn't have `discord` or `discord.ext.commands` namespaces
        result = {}

        # first line is version info
        inv_version = stream.readline().rstrip()

        if inv_version != '# Sphinx inventory version 2':
            raise RuntimeError('Invalid objects.inv file version.')

        # next line is "# Project: <name>"
        # then after that is "# Version: <version>"
        projname = stream.readline().rstrip()[11:]
        version = stream.readline().rstrip()[11:]

        # next line says if it's a zlib header
        line = stream.readline()
        if 'zlib' not in line:
            raise RuntimeError('Invalid objects.inv file, not z-lib compatible.')

        # This code mostly comes from the Sphinx repository.
        entry_regex = re.compile(r'(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)')
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(':')
            if directive == 'py:module' and name in result:
                # From the Sphinx Repository:
                # due to a bug in 1.1 and below,
                # two inventory entries are created
                # for Python modules, and the first
                # one is correct
                continue

            # Most documentation pages have a label
            if directive == 'std:doc':
                subdirective = 'label'

            if location.endswith('$'):
                location = location[:-1] + name

            key = name if dispname == '-' else dispname
            prefix = f'{subdirective}:' if domain == 'std' else ''

            if projname == 'discord.py':
                key = key.replace('discord.ext.commands.', '').replace('discord.', '')

            result[f'{prefix}{key}'] = os.path.join(url, location)

        return result

    async def build_rtfm_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            sub = cache[key] = {}
            async with self.bot.session.get(page + '/objects.inv') as resp:
                if resp.status != 200:
                    raise RuntimeError('Cannot build rtfm lookup table, try again later.')

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._rtfm_cache = cache

    async def do_rtfm(self, ctx, key, obj):
        page_types = {
            'latest': 'https://discordpy.readthedocs.io/en/latest',
            'latest-jp': 'https://discordpy.readthedocs.io/ja/latest',
            'python': 'https://docs.python.org/3',
            'python-jp': 'https://docs.python.org/ja/3',
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, '_rtfm_cache'):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)

        if key.startswith('latest'):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == '_':
                    continue
                if q == name:
                    obj = f'abc.Messageable.{name}'
                    break

        cache = list(self._rtfm_cache[key].items())
        def transform(tup):
            return tup[0]

        matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        e = discord.Embed(colour=discord.Colour.blurple())
        if len(matches) == 0:
            return await ctx.send('Could not find anything. Sorry.')

        e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
        await ctx.send(embed=e)


    def transform_rtfm_language_key(self, ctx, prefix):
        if ctx.guild is not None:
            #                             日本語 category
            if ctx.channel.category_id == 490287576670928914:
                return prefix + '-jp'
            #                    d.py unofficial JP   Discord Bot Portal JP
            elif ctx.guild.id in (463986890190749698, 494911447420108820):
                return prefix + '-jp'
        return prefix

    @commands.command()
    async def info(self, ctx):
        x = await self.client.fetch_user(782229285611372545)
        proc = psutil.Process()
        mem = proc.memory_full_info()
        embed = discord.Embed(title=f'{ctx.command.name}', description=f'{ctx.bot.description}', colour=0x2F3136)
        embed.add_field(name='Info:', value=f'<:member_join:596576726163914752> **Developer -** [Rainbow](https://discord.com/users/688293803613880334)\n<:member_join:596576726163914752> **Library -** [discord.py](https://pypi.org/project/discord.py/)\n<:member_join:596576726163914752> **Last Boot -** {humanize.naturaltime(load_time)}\n<:member_join:596576726163914752> **Created - ** {humanize.naturaltime(x.created_at)}')
        embed.add_field(name='Stats:', value=f'<:member_join:596576726163914752> **Number of commands -** {len(self.client.commands)}\n<:member_join:596576726163914752> **Guilds -** {len(list(map(str, [p.id for p in self.client.guilds])))}\n<:member_join:596576726163914752> **Users -** {len(list(map(str, [p.id for p in self.client.users])))}\n<:member_join:596576726163914752> **Prefix -** `rr.`, `rainbow`, `rainbow `')
        await ctx.send(embed=embed)

    @commands.group(aliases=['rtfd'], invoke_without_command=True)
    async def rtfm(self, ctx, *, obj: str = None):
        """Gives you a documentation link for a discord.py entity.
        Events, objects, and functions are all supported through a
        a cruddy fuzzy algorithm.
        """
        key = self.transform_rtfm_language_key(ctx, 'latest')
        await self.do_rtfm(ctx, key, obj)
    @commands.command()
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send(embed=discord.Embed(title='Pinging...', colour=0x2F3136))
        end = time.perf_counter()
        duration = (end - start) * 1000
        embed = discord.Embed(title='Ping:', colour=0x2F3136)
        embed.add_field(name='<a:loading:747680523459231834> | Websocket:', value=f'{round(self.client.latency * 1000)}ms')
        embed.add_field(name='<a:typing:597589448607399949> | Typing:', value=f'{round(duration)}ms')
        await message.edit(embed=embed)

    @commands.command()
    @commands.cooldown(1,10,BucketType.user)
    async def hello(self, ctx):
        await ctx.send(embed=discord.Embed(title='Hi', description=f'I am [{self.client.user.name}](https://discord.com/users/782229285611372545), [Rainbow](https://discord.com/users/688293803613880334) made me.', colour=0x2F3136))

    @commands.command()
    async def uptime(self, ctx):
        x = load_time - datetime.utcnow()
        y = humanize.precisedelta(x, minimum_unit="seconds")
        await ctx.send(embed=discord.Embed(title=ctx.command.name, description=f'Uptime: **{y}**', colour=0x2F3136))

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.id == 688293803613880334:
            await self.client.process_commands(after)

    @commands.command()
    async def source(self, ctx, *, command: str = None):
        await ctx.send("https://github.com/RainbowPyPrograms/Rainbow-Robot")
    @commands.Cog.listener()
    async def on_command_error(self, ctx,  error):
        if isinstance(error ,commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(title=f'{error}', colour=discord.Colour.red()))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(title='The parameter was invalid', colour=discord.Colour.red()))
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(embed=discord.Embed(title='NSFW channel required', colour=discord.Colour.red()))
        elif isinstance(error, commands.NotOwner):
            await ctx.send(embed=discord.Embed(title=f'You cannot use this command', colour=discord.Colour.red()))
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(title='Command is on cooldown', colour=discord.Colour.red()))
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(embed=discord.Embed(title='Too many arguments were given', colour=discord.Colour.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(title=f'{error}', colour=discord.Colour.red()))
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=discord.Embed(title=f'{error}', colour=discord.Colour.red()))
        elif isinstance(error ,commands.CommandError):
            prettify_exceptions.DefaultFormatter().theme['_ansi_enabled'] = False
            traceback = ''.join(prettify_exceptions.DefaultFormatter().format_exception(type(error), error, error.__traceback__))
            if len(traceback) < 1999:
                texts = f"```{traceback}```"
            else:
                paste = await mystbin_client.post(traceback,syntax="python")
                texts = f"{str(paste)}"
            print(f'{texts}')
            await ctx.send(embed=discord.Embed(title='Error:', description=f"```py\n{error}```\n{texts}", colour=discord.Colour.red()))

    @commands.command(aliases=['ui', 'profile'])
    async def userinfo(self, ctx, *,user: discord.Member = None):
        user = user or ctx.author
        if user.bot is True:
            sdf = '<:bot_tag:596576775555776522>'
        if user.bot is False:
            sdf = ''
        if user.nick is None:
            user.nick = user.name
        x = discord.utils.find(lambda e: e.name.lower() == f"status_{user.raw_status}", self.client.emojis)
        my = discord.utils.find(lambda e: e.name.lower() == f"status_{str(user.mobile_status)}", self.client.emojis)
        wy = discord.utils.find(lambda e: e.name.lower() == f"status_{str(user.web_status)}", self.client.emojis)
        dy = discord.utils.find(lambda e: e.name.lower() == f"status_{str(user.desktop_status)}", self.client.emojis)
        embed = discord.Embed(description=f'Platform Status:\n**Mobile -** {my}\n**Desktop -** {dy}\n**Website -** {wy}', colour=user.color)
        if user.color == discord.Colour.default():
            embed.color = 0x2F3136
        else:
            embed.color = user.color
        embed.set_author(name=str(user.name), icon_url=f'{str(ctx.guild.icon_url)}', url=f'https://discord.com/users/{user.id}')
        embed.add_field(name='Profile:', value=f'<:member_join:596576726163914752> **ID -** {user.id}\n<:member_join:596576726163914752> **Discriminator -** {user.discriminator}\n<:member_join:596576726163914752> **Nickname -** {user.nick} {sdf}\n<:member_join:596576726163914752> **Default Avatar -** [Link]({str(user.default_avatar_url)})')
        embed.add_field(name='Information:', value=f'<:member_join:596576726163914752> **Created -** {humanize.naturaltime(user.created_at)}\n<:member_join:596576726163914752> **Joined -** {humanize.naturaltime(user.joined_at)}\n<:member_join:596576726163914752> **Status -** {x}\n<:member_join:596576726163914752> **Roles -** {", ".join(r.name for r in user.roles)}')
        embed.set_thumbnail(url=str(user.avatar_url))
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == self.client.user.mention:
            await message.channel.send(embed=discord.Embed(title="Hi there", description=f"Hi there, I am {self.client.user.name}, for more Information please use `rr.help`"))
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        g = await self.client.fetch_channel(716715457863876699)
        if member.guild.id == 708355954843975821:
            embed=discord.Embed(title=f'Welcome to {member.guild.name}',description=f'Hope you enjoy your stay and have lots of fun here. Be sure to get your roles and colours', colour=discord.Colour.red())
            embed.set_author(name=member.guild.name, icon_url=str(member.guild.icon_url))
            embed.add_field(name="Channels", value=f'Be sure to check out these channels\n<#727562849622425681>\n<#716716485330075788>\n<#71671554420719390>')
            embed.set_image(url='https://c.tenor.com/wZW05QUURk4AAAAM/welcome-anime.gif')
            await g.send(embed=embed)
        else:
            print(member.guild.id)

    @commands.command()
    async def support(self, ctx):
        await ctx.send("https://discord.gg/UQ8qh4aMAj")

    @commands.command(aliases=['gi'])
    async def guildinfo(self, ctx):
        await ctx.channel.trigger_typing()
        lulw = discord.utils.find(lambda e: e.name.lower() == f"member_join", self.client.emojis)
        gg = ", ".join(str(g) for g in list(map(lambda f: f.title().replace("_", " "), ctx.guild.features[:2])))
        embed = discord.Embed(description=ctx.guild.description or "", colour=0x2F3136)
        embed.set_author(name=ctx.guild.name, icon_url=str(ctx.guild.icon_url))
        embed.add_field(name="Stats:", value=f"{lulw} **Emojis -** {''.join(str(e) for e in ctx.guild.emojis[:3])} + {len(ctx.guild.emojis) - 3} more\n{lulw} **Region -** {ctx.guild.region}\n{lulw} **AFK Channel -** {ctx.guild.afk_channel}\n{lulw} **AFK Timeout -** {humanize.precisedelta(ctx.guild.afk_timeout)}\n{lulw} **Channels -** {len(ctx.guild.channels)}\n{lulw} **Features -** {gg} + {len(ctx.guild.features) - 1} more\n{lulw} **Roles -** {' ,'.join(role.mention for role in ctx.guild.roles[:1])} + {len(ctx.guild.roles) - 1}\n{lulw} **Created -** {humanize.naturaltime(ctx.guild.created_at)}")
        embed.add_field(name="About:", value=f'{lulw} **ID -** {ctx.guild.id}\n{lulw} **Owner -** {ctx.guild.owner.mention}\n{lulw} **MFA Level -** {ctx.guild.mfa_level}\n{lulw} **Verification Level-** {ctx.guild.verification_level}\n{lulw} **Boost Level -** {ctx.guild.premium_tier}\n{lulw} **Number of Boosts -** {ctx.guild.premium_subscription_count}\n{lulw} **Members -** {ctx.guild.member_count}\n{lulw} **Number of Boosts -** {len(ctx.guild.premium_subscribers)}')
        embed.set_image(url=ctx.guild.banner_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, *, user:discord.User = None):
        user = user or ctx.author
        await ctx.send(embed=discord.Embed(title=f"{user.name}'s avatar:", colour=0x2F3136).set_image(url=f'{user.avatar_url}'))

    @commands.command(aliases=['inv'])
    async def invite(self, ctx):
        await ctx.send(embed=discord.Embed(title=f'Invite links:', description=f"<:member_join:596576726163914752> **Bot invite -** [With no perms]({discord.utils.oauth_url(ctx.bot.user.id)})\n<:member_join:596576726163914752> **Bot invite -** [Administrator perms]({discord.utils.oauth_url(ctx.bot.user.id, permissions=discord.Permissions(8))})\n<:member_join:596576726163914752> **Bot invite -** [Basic perms(recommended)]({discord.utils.oauth_url(ctx.bot.user.id, permissions=discord.Permissions.all_channel())})", colour=0x2F3136))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def announce(self, ctx, role: discord.Role, *, announcement):
        x = ctx.bot.get_channel(803089445381210123)
        await x.send(str(role), embed=discord.Embed(title="Announcement", description=announcement, colour=discord.Colour.random()))
        await ctx.send(embed=discord.Embed(title="Announced", description=f'`{announcement}`'))
    @commands.command(hidden=True)
    @commands.is_owner()
    async def update(self, ctx,*, log):
        x = ctx.bot.get_channel(802590019868688384)
        await x.send(embed=discord.Embed(title=str(datetime.utcnow()), description=log, colour=discord.Colour.blue()))
        await ctx.send(embed=discord.Embed(title="Pushed the update"))

def setup(client):
    client.add_cog(Info(client))
