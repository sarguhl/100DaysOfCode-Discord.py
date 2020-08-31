from asyncio import sleep
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from discord import Embed, File, Member
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, NotOwner)

from discord.ext.commands import when_mentioned_or, command, has_permissions

OWNER_IDS = []
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot, message):
    prefix = "!"
    return when_mentioned_or(prefix)(bot, message)

class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler
        
        super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS)
    
    def setup(self):
        extentions = [
            "libary.cogs.meta",
            "libary.cogs.info",
            "libary.cogs.logging",
            "libary.cogs.livesupport"
        ]
        for ext in extentions:
            self.load_extension(ext)
            print(f"Cog ready: {ext}")
    
    def run(self, version):
        self.VERSION = version
        
        self.setup()
        
        print("Running setup")
        
        with open("./data/rest/token.txt", "r", encoding="utf-8") as f:
            self.TOKEN = f.read()
        
        print("running bot...")
        super().run(self.TOKEN)

    
    async def on_connect(self):
        print("bot connected...")
    
    async def on_disconnect(self):
        print("bot disconntected...")
    
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong!")
        
        await self.stdout.send("An error occured.")
        raise    

    async def on_command_error(self, ctx, exc):
        if any ([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("`Error`: One or more requred arguments are missing.")
        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs.")
        elif hasattr(exc, "original"):
            if isinstance(exc.original, Forbidden):
                await ctx.send("I don't have the required permissions to do this.")
            else:
                raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(749324744901263470)
            self.stdout = self.get_channel(749324797975986206)


            await self.stdout.send("Now online!")
            self.ready = True
            print(" bot ready")

            meta = self.get_cog("Meta")   
            await meta.set()

        else:
            print("bot reconnected")
        
bot = Bot()