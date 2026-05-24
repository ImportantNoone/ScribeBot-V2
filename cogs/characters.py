import discord
from discord.ext import commands
import json
import os

class Characters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.characters_file = 'data/characters.json'
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists(self.characters_file):
            with open(self.characters_file, 'w') as f:
                json.dump({}, f)
    
    def load_characters(self):
        with open(self.characters_file, 'r') as f:
            return json.load(f)
    
    def save_characters(self, characters):
        with open(self.characters_file, 'w') as f:
            json.dump(characters, f, indent=2)
    
    def char_exists(self, user_id):
        characters = self.load_characters()
        return str(user_id) in characters
    
    @commands.command(name='create_character')
    async def create_character(self, ctx):
        """create a new medieval character"""
        user_id = str(ctx.author.id)
        characters = self.load_characters()
        
        if user_id in characters:
            await ctx.send("you already have a character. use !character to view it.")
            return
        
        # character classes with different starting bonuses
        classes = {
            'scholar': {'word_power': 8, 'health': 50, 'mana': 100},
            'knight': {'word_power': 6, 'health': 100, 'mana': 40},
            'rogue': {'word_power': 7, 'health': 70, 'mana': 60}
        }
        
        embed = discord.Embed(
            title='choose your class',
            description='react to select your medieval character class',
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name='scholar',
            value='high intelligence, master of words\nword power: 8, health: 50, mana: 100',
            inline=False
        )
        embed.add_field(
            name='knight',
            value='strong and resilient warrior\nword power: 6, health: 100, mana: 40',
            inline=False
        )
        embed.add_field(
            name='rogue',
            value='balanced and cunning\nword power: 7, health: 70, mana: 60',
            inline=False
        )
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')
        await msg.add_reaction('3️⃣')
        
        def check(reaction, user):
            return user == ctx.author and reaction.emoji in ['1️⃣', '2️⃣', '3️⃣']
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            class_map = {'1️⃣': 'scholar', '2️⃣': 'knight', '3️⃣': 'rogue'}
            chosen_class = class_map[reaction.emoji]
            
            character = {
                'name': f"{ctx.author.name}'s {chosen_class.capitalize()}",
                'class': chosen_class,
                'level': 1,
                'experience': 0,
                'word_power': classes[chosen_class]['word_power'],
                'max_health': classes[chosen_class]['health'],
                'current_health': classes[chosen_class]['health'],
                'mana': classes[chosen_class]['mana'],
                'victories': 0,
                'challenges_won': 0,
                'loot': [],
                'spells': ['slash', 'puncture']
            }
            
            characters[user_id] = character
            self.save_characters(characters)
            
            result_embed = discord.Embed(
                title='character created',
                description=f"welcome, {character['name']}!",
                color=discord.Color.green()
            )
            result_embed.add_field(name='class', value=chosen_class, inline=True)
            result_embed.add_field(name='health', value=character['max_health'], inline=True)
            result_embed.add_field(name='word power', value=character['word_power'], inline=True)
            
            await ctx.send(embed=result_embed)
        
        except:
            await ctx.send("character creation timed out")
    
    @commands.command(name='character')
    async def view_character(self, ctx):
        """view your current character"""
        user_id = str(ctx.author.id)
        characters = self.load_characters()
        
        if user_id not in characters:
            await ctx.send("you don't have a character yet. use !create_character to start.")
            return
        
        char = characters[user_id]
        
        embed = discord.Embed(
            title=char['name'],
            color=discord.Color.gold()
        )
        
        embed.add_field(name='level', value=char['level'], inline=True)
        embed.add_field(name='class', value=char['class'], inline=True)
        embed.add_field(name='experience', value=f"{char['experience']}/100", inline=True)
        embed.add_field(name='word power', value=char['word_power'], inline=True)
        embed.add_field(name='health', value=f"{char['current_health']}/{char['max_health']}", inline=True)
        embed.add_field(name='mana', value=char['mana'], inline=True)
        embed.add_field(name='victories', value=char['victories'], inline=True)
        embed.add_field(name='challenges won', value=char['challenges_won'], inline=True)
        embed.add_field(name='spells', value=', '.join(char['spells']), inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='stats')
    async def view_stats(self, ctx):
        """view detailed progression stats"""
        user_id = str(ctx.author.id)
        characters = self.load_characters()
        
        if user_id not in characters:
            await ctx.send("you don't have a character yet. use !create_character to start.")
            return
        
        char = characters[user_id]
        
        embed = discord.Embed(
            title=f"{char['name']} - detailed stats",
            color=discord.Color.blue()
        )
        
        embed.add_field(name='progression', value=f"level {char['level']} - {char['experience']}/100 exp", inline=False)
        embed.add_field(name='combat', value=f"word power: {char['word_power']}\nhealth: {char['current_health']}/{char['max_health']}\nmana: {char['mana']}", inline=False)
        embed.add_field(name='achievements', value=f"battles won: {char['victories']}\nchallenges won: {char['challenges_won']}", inline=False)
        embed.add_field(name='active spells', value=', '.join(char['spells']) if char['spells'] else 'none', inline=False)
        embed.add_field(name='inventory size', value=len(char['loot']), inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Characters(bot))
