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
            "libary.cogs.meta"
        ]
        for ext in extentions:
            self.load_extension(ext)
    
    def run(self, version):
        self.VERSION = version
        
        self.setup()
        
        print("Running setup")
        
        with open("./data/rest/token.txt", "r", encoding="utf-8") as f:
            self.TOKEN = f.read()
        
        print("running bot...")
        super().run(self.TOKEN)
    
    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            
            else:
                await ctx.send("I'm not ready to process any commands. Please wait a second.")
    
    async def on_connect(self):
        print("bot connected...")
    
    async def on_disconnect(self):
        print("bot disconntected...")
    
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