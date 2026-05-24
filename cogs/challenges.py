import discord
from discord.ext import commands
import json
import os
import random
import string

class Challenges(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.characters_file = 'data/characters.json'
        self.words_file = 'data/word_list.json'
        
        os.makedirs('data', exist_ok=True)
        
        # load or create word list
        if not os.path.exists(self.words_file):
            self.create_word_list()
    
    def create_word_list(self):
        """create a list of words for challenges"""
        words = {
            'easy': ['cat', 'dog', 'tree', 'stone', 'sword', 'magic', 'fire', 'water', 'wind', 'earth'],
            'medium': ['dragon', 'wizard', 'castle', 'battle', 'ancient', 'kingdom', 'treasure', 'spell', 'forest', 'mountain'],
            'hard': ['enchanted', 'philosopher', 'manuscript', 'adventure', 'legendary', 'extraordinary', 'mysterious', 'magnificent', 'dangerous', 'prophecy']
        }
        
        with open(self.words_file, 'w') as f:
            json.dump(words, f, indent=2)
    
    def load_words(self):
        with open(self.words_file, 'r') as f:
            return json.load(f)
    
    def load_characters(self):
        with open(self.characters_file, 'r') as f:
            return json.load(f)
    
    def save_characters(self, characters):
        with open(self.characters_file, 'w') as f:
            json.dump(characters, f, indent=2)
    
    def get_word_difficulty(self, word_length):
        if word_length <= 5:
            return 'easy'
        elif word_length <= 10:
            return 'medium'
        else:
            return 'hard'
    
    def calculate_score(self, word, word_power):
        """calculate score based on word length and power"""
        base_score = len(word) * 10
        bonus = word_power * 2
        return base_score + bonus
    
    @commands.command(name='challenge')
    async def word_challenge(self, ctx):
        """start a word challenge"""
        user_id = str(ctx.author.id)
        characters = self.load_characters()
        
        if user_id not in characters:
            await ctx.send("you need a character first. use !create_character")
            return
        
        words = self.load_words()
        all_words = words['easy'] + words['medium'] + words['hard']
        challenge_word = random.choice(all_words)
        difficulty = self.get_word_difficulty(len(challenge_word))
        
        # scramble the word
        scrambled = ''.join(random.sample(challenge_word, len(challenge_word)))
        
        embed = discord.Embed(
            title='word challenge',
            description=f'unscramble this word: {scrambled}',
            color=discord.Color.purple()
        )
        embed.add_field(name='difficulty', value=difficulty, inline=True)
        embed.add_field(name='hints', value=f"length: {len(challenge_word)}", inline=True)
        
        msg = await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        try:
            answer = await self.bot.wait_for('message', timeout=30.0, check=check)
            
            if answer.content.lower() == challenge_word.lower():
                character = characters[user_id]
                score = self.calculate_score(challenge_word, character['word_power'])
                character['challenges_won'] += 1
                character['experience'] += 25
                
                # check for level up
                if character['experience'] >= 100:
                    character['level'] += 1
                    character['word_power'] += 2
                    character['experience'] = 0
                    level_up = True
                else:
                    level_up = False
                
                self.save_characters(characters)
                
                result_embed = discord.Embed(
                    title='challenge won',
                    description=f'the word was: {challenge_word}',
                    color=discord.Color.green()
                )
                result_embed.add_field(name='score', value=score, inline=True)
                result_embed.add_field(name='experience', value=f"+25", inline=True)
                
                if level_up:
                    result_embed.add_field(name='level up', value=f"you reached level {character['level']}", inline=False)
                
                await ctx.send(embed=result_embed)
            else:
                result_embed = discord.Embed(
                    title='challenge failed',
                    description=f'the correct answer was: {challenge_word}',
                    color=discord.Color.red()
                )
                await ctx.send(embed=result_embed)
        
        except:
            await ctx.send(f"time's up. the word was: {challenge_word}")
    
    @commands.command(name='inventory')
    async def view_inventory(self, ctx):
        """view your collected loot"""
        user_id = str(ctx.author.id)
        characters = self.load_characters()
        
        if user_id not in characters:
            await ctx.send("you need a character first. use !create_character")
            return
        
        character = characters[user_id]
        
        embed = discord.Embed(
            title=f"{character['name']}'s inventory",
            color=discord.Color.teal()
        )
        
        if character['loot']:
            loot_text = '\n'.join([f"{item['name']} - {item['rarity']}" for item in character['loot']])
            embed.add_field(name='items', value=loot_text, inline=False)
        else:
            embed.add_field(name='items', value='your inventory is empty', inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='spells')
    async def view_spells(self, ctx):
        """view your unlocked spells"""
        user_id = str(ctx.author.id)
        characters = self.load_characters()
        
        if user_id not in characters:
            await ctx.send("you need a character first. use !create_character")
            return
        
        character = characters[user_id]
        
        embed = discord.Embed(
            title=f"{character['name']}'s spells",
            color=discord.Color.purple()
        )
        
        spells_text = '\n'.join(character['spells']) if character['spells'] else 'you have no spells yet'
        embed.add_field(name='learned spells', value=spells_text, inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Challenges(bot))
