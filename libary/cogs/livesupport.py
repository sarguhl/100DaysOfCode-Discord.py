from discord.ext import commands
from discord.ext.commands import Cog, command

from discord import Embed, Member
from discord.channel import DMChannel
from datetime import datetime

class Livesupport(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_message(self, message):
        live_support_channel = self.bot.get_channel(749989564965322952)
        
        if not message.author.bot:
            if isinstance(message.channel, DMChannel):
                if len(message.content) < 50:
                    
                    embed = Embed(
                        title="Text error",
                        description="Your message should be at least 50 characters in length."
                    )
                    
                    await message.channel.send(embed=embed)
                    
                else:
                    embed = Embed(
                        title="Livesupport Mail",
                        timestamp=datetime.utcnow()
                    )
                    
                    if len(message.attachments):
                        embed.set_image(url=message.attachments[0].url)
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    
                    fields = [
                        ("Message:", message.content)
                    ]
                    
                    
                    for name, value in fields:
                        embed.add_field(name=name, value=value, inline=False)
                    
                    await live_support_channel.send(embed=embed)
                    await message.channel.send("Message sent to the Support.")

    @command(name="pn")
    async def pn_command(self, ctx, member: Member, *, message):
        await member.send(f"**{ctx.author.display_name}**: {message}")
def setup(bot):
    bot.add_cog(Livesupport(bot))