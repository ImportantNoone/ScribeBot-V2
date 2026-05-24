import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('discord_token')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'loaded {filename}')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to discord')
    print('------')

@bot.command(name='help')
async def help_command(ctx):
    """display all available commands"""
    embed = discord.Embed(title='scribebot v2 commands', color=discord.Color.gold())
    
    embed.add_field(
        name='character commands',
        value='!create_character - create your character\n!character - view character stats\n!stats - see progression',
        inline=False
    )
    
    embed.add_field(
        name='gameplay commands',
        value='!challenge - start word challenge\n!battle - duel another player\n!inventory - view loot\n!spells - see unlocked spells',
        inline=False
    )
    
    embed.add_field(
        name='general commands',
        value='!leaderboard - view top players\n!help - show this message',
        inline=False
    )
    
    await ctx.send(embed=embed)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
