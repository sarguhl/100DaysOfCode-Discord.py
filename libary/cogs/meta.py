from datetime import datetime, timedelta
from platform import python_version
from time import time

from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType, Embed
from discord import __version__ as discord_version
from discord.ext.commands import Cog
from discord.ext.commands import command



class Meta(Cog):
	def __init__(self, bot):
		self.bot = bot

		self._message = "watching !help | {users:,} users in {guilds:,} servers"

		#bot.scheduler.add_job(self.set, CronTrigger(second=0))

	@property
	def message(self):
		return self._message.format(users=len(self.bot.users), guilds=len(self.bot.guilds))

	@message.setter
	def message(self, value):
		if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
			raise ValueError("Invalid activity type.")

		self._message = value

	async def set(self):
		_type, _name = self.message.split(" ", maxsplit=1)

		await self.bot.change_presence(activity=Activity(
			name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
		))

	@command(name="setactivity")
	async def set_activity_message(self, ctx, *, text: str):
		self.message = text
		await self.set()

	@command(name="ping")
	async def ping(self, ctx):
		start = time()
		message = await ctx.send(f"Pong! DWSP latency: {self.bot.latency*1000:,.0f} ms.")
		end = time()

		await message.edit(content=f"Pong! DWSP latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms.")

	@command(name="stats")
	async def show_bot_stats(self, ctx):
		embed = Embed(title="Bot stats",
					  colour=ctx.author.colour,
					  thumbnail=self.bot.user.avatar_url,
					  timestamp=datetime.utcnow())

		fields = [
			("Bot version", self.bot.VERSION, True),
			("Python version", python_version(), True),
			("discord.py version", discord_version, True),
			("Users", f"{self.bot.guild.member_count:,}", True)
		]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)

	@command(name="shutdown")
	async def shutdown(self, ctx):
		await ctx.send("Shutting down...")

		#db.commit()
		#self.bot.scheduler.shutdown()
		await self.bot.logout()


def setup(bot):
	bot.add_cog(Meta(bot))