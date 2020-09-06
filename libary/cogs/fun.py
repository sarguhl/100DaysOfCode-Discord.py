from random import choice, randint
from typing import Optional

from aiohttp import request, ClientSession
from discord import Embed, Member
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown, BadArgument


random_color = [
    0x374DAD,
    0x376EA8,
    0x378CA3,
    0x379E95,
    0x369973
]

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name="meme")
    async def meme(self, ctx):
        embed = Embed(title="MEME")
        
        async with ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)
    
    @command(name="roll", description="This command let's you roll dices!")
    async def roll_dice(self, ctx, dce: str):
        dice, value = (int(term) for term in dce.split("d"))
        
        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)]
            
            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = `{sum(rolls)}`")
        
        else:
            await ctx.send("I can't roll so many dices!")

    @command(name="fact")
    async def animal_fact(self, ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"
            
            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]
                
                else:
                    image_link=None
            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    embed = Embed(
                        title=f"{animal.title()} fact!",
                        description=data["fact"],
                        color=choice(random_color)
                    )
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)
                
                else:
                    await ctx.send(f"API returned a {response.status} status.")
                        
        else:
            await ctx.send(f"There are no facts about this animal :(")

def setup(bot):
    bot.add_cog(Fun(bot))