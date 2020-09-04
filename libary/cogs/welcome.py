import random

from discord import Embed, Member

from discord.ext import commands
from discord.ext.commands import Cog, command

from datetime import datetime, timedelta
from random import choice

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.welcome_channel = self.bot.get_channel(751171067573436477)
    
    @Cog.listener()
    async def on_member_join(self, member):
        random_color = [
            0x374DAD,
            0x376EA8,
            0x378CA3,
            0x379E95,
            0x369973
        ]
        
        random_c = f"0x{choice(random_color)}"
        
        embed = Embed(
            title=f"{choice(('Hello', 'Welcome', 'Salute', 'AYAYAYAAAAY', 'Hallo', 'Hyia'))} **{member.display_name}**!",
            description=f"Welcome to {member.guild.name}. Have a nice time and make sure to read the **rules**!",
            color=choice(random_color)
        )
        embed.set_thumbnail(url=member.avatar_url)
        
        await self.welcome_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))