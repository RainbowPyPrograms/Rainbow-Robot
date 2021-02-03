import discord
from discord.ext import commands
import humanize
import aiosqlite
from polaroid import Image
import requests
import io

class image(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def cali(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("cali")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def drmatic(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("dramatic")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def firenze(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("firenze")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def golden(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("golden")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def lix(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("lix")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def lofi(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("lofi")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def neue(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("neue")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def obsidian(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("obsidian")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def pink(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("pastel_pink")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def ryo(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("ryo")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def oceanic(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("oceanic")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def islands(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("islands")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def marine(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("marine")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def green(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("seagreen")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def blue(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("flagblue")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def liquid(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("liquid")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def diamante(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("diamante")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def radio(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("radio")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def twenties(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("twenties")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def rose(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("rosetint")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def mauve(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("mauve")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def vintage(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("vintage")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def perfume(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("purfume")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

	@commands.command()
	async def serenity(self, ctx, user: discord.User = None):
		user = user or ctx.author
		byt = requests.get(user.avatar_url_as(format=None, static_format='webp', size=1024)).content
		im = Image(byt)
		im.filter("serenity")
		ret_byt = im.save_bytes()
		await ctx.send("This command may not work with gif" ,file=discord.File(io.BytesIO(ret_byt), filename=f'{ctx.command.name}.png'))

def setup(client):
    client.add_cog(image(client))
