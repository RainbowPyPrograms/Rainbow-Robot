import discord
from discord.ext import commands
from asyncdagpi import Client
import humanize
import aiosqlite
dagpi Client("")
# same here, if you want to use it put the token, if you dont, delete line
#class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roast(self, ctx, member: discord.Member):
        img = await dagpi.roast()
        if member.id == ctx.bot.owner_id:
            await ctx.send(embed=discord.Embed(title="I will not do that, dont ask Why i just wont", colour=discord.Colour.red()))
        elif member.id == ctx.bot.user.id:
            await ctx.send(embed=discord.Embed(title="I will not do that, dont ask Why i just wont", colour=discord.Colour.red()))
        else:
            await ctx.send(f'**{member.name}**, {img}')
    @commands.command()
    async def fact(self, ctx):
        facts = await dagpi.fact()
        await ctx.send(f'Did you know, that {facts}')

    @commands.command(name='8ball')
    async def _8ball(self, ctx, question):
    	now = await dagpi.eight_ball()
    	await ctx.send(f'{now}')


    @commands.command()
    async def joke(self, ctx):
    	now = await dagpi.joke()
    	await ctx.send(f'{now}')

    @commands.command()
    @commands.is_nsfw()
    async def pl(self, ctx):
    	now = await dagpi.pickup_line()
    	await ctx.send(embed=discord.Embed(title=now.category, description=now.line, colour=discord.Colour.blue()))        

    @commands.command()
    async def logo(self, ctx):
        now = await dagpi.logo()
        embed = discord.Embed(title=f'Guess that logo:', colour=discord.Colour.magenta())
        aswd = now.question
        embed.set_image(url=aswd)
        x = await ctx.send(embed=embed)
        channel = ctx.channel
        def check(m):
            return m.author.id == ctx.author.id and m.channel == channel
        msg = await self.client.wait_for('message', check=check)
        if msg.content == now.brand:
            await ctx.send("Correct")
            return
        if msg.content == now.brand.lower():
            await ctx.send("Correct")
            return
        else:
            await ctx.send(f'Wrong, Answer was {now.brand}')


    @commands.command()
    async def wtp(self, ctx):
        now = await dagpi.wtp()
        embed = discord.Embed(title=f'Guess that pokemon:', colour=discord.Colour.magenta())
        aswd = now.question
        embed.set_image(url=aswd)
        x = await ctx.send(embed=embed)
        channel = ctx.channel
        def check(m):
            return m.author.id == ctx.author.id and m.channel == channel
        msg = await self.client.wait_for('message', check=check)
        if msg.content == now.name:
            await ctx.send("Correct")
            return
        if msg.content == now.name.lower():
            await ctx.send("Correct")
            return
        else:
            await ctx.send(f'Wrong, Answer was {now.name}')

    @commands.command()
    async def spotify(self,ctx, user: discord.Member = None):
        user = user or ctx.author
        try:
            try:
                dfdfdf = user.activities[0].title
                spotify = user.activities[0]
            except:
                dfdfdf = user.activities[1].title
                spotify = user.activities[1]
        except:
            await ctx.send(embed=discord.Embed(title="The user is not listening to **Spotify**", colour=discord.Colour.red()))
        else:
            await ctx.send(embed=discord.Embed(title=str(spotify.title), description=f'<:member_join:596576726163914752> **Artist -** {spotify.artist}\n<:member_join:596576726163914752> **Album -** {spotify.album}\n<:member_join:596576726163914752> **Duration -** {humanize.precisedelta(spotify.duration.seconds)}', colour=spotify.color).set_thumbnail(url=spotify.album_cover_url))
def setup(client):
    client.add_cog(Fun(client))
