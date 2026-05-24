import discord
from discord.ext import commands
import json
import os

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.characters_file = 'data/characters.json'
    
    def load_characters(self):
        if os.path.exists(self.characters_file):
            with open(self.characters_file, 'r') as f:
                return json.load(f)
        return {}
    
    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        """display the server leaderboard"""
        characters = self.load_characters()
        
        if not characters:
            await ctx.send("no characters found")
            return
        
        # sort by victories
        sorted_by_victories = sorted(
            characters.items(),
            key=lambda x: x[1]['victories'],
            reverse=True
        )[:10]
        
        # sort by challenges won
        sorted_by_challenges = sorted(
            characters.items(),
            key=lambda x: x[1]['challenges_won'],
            reverse=True
        )[:10]
        
        embed = discord.Embed(
            title='scribebot leaderboard',
            color=discord.Color.gold()
        )
        
        # battles leaderboard
        battles_text = ""
        if sorted_by_victories:
            for rank, (user_id, char) in enumerate(sorted_by_victories, 1):
                battles_text += f"{rank}. {char['name']} - {char['victories']} wins\n"
        else:
            battles_text = "no battles yet"
        
        embed.add_field(
            name='top battles won',
            value=battles_text,
            inline=False
        )
        
        # challenges leaderboard
        challenges_text = ""
        if sorted_by_challenges:
            for rank, (user_id, char) in enumerate(sorted_by_challenges, 1):
                challenges_text += f"{rank}. {char['name']} - {char['challenges_won']} completed\n"
        else:
            challenges_text = "no challenges yet"
        
        embed.add_field(
            name='top challenges completed',
            value=challenges_text,
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
