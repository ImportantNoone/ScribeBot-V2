import discord
from discord.ext import commands
import json
import os
import random

class Battles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.characters_file = 'data/characters.json'
        self.words_file = 'data/word_list.json'
    
    def load_characters(self):
        with open(self.characters_file, 'r') as f:
            return json.load(f)
    
    def save_characters(self, characters):
        with open(self.characters_file, 'w') as f:
            json.dump(characters, f, indent=2)
    
    def load_words(self):
        with open(self.words_file, 'r') as f:
            return json.load(f)
    
    def calculate_battle_score(self, word, word_power):
        """calculate battle damage based on word"""
        length_bonus = len(word) * 3
        power_bonus = word_power
        return length_bonus + power_bonus
    
    @commands.command(name='battle')
    async def battle(self, ctx, opponent: discord.User = None):
        """challenge another player to a word battle"""
        if opponent is None:
            await ctx.send("you must mention a player to battle. example: !battle @username")
            return
        
        if opponent.bot:
            await ctx.send("you can't battle a bot")
            return
        
        if opponent == ctx.author:
            await ctx.send("you can't battle yourself")
            return
        
        player1_id = str(ctx.author.id)
        player2_id = str(opponent.id)
        characters = self.load_characters()
        
        if player1_id not in characters or player2_id not in characters:
            await ctx.send("both players need to have characters")
            return
        
        player1_char = characters[player1_id]
        player2_char = characters[player2_id]
        
        words = self.load_words()
        all_words = words['easy'] + words['medium'] + words['hard']
        
        # first round
        embed = discord.Embed(
            title='word battle started',
            description=f"{ctx.author.name} vs {opponent.name}",
            color=discord.Color.red()
        )
        battle_msg = await ctx.send(embed=embed)
        
        player1_health = player1_char['current_health']
        player2_health = player2_char['current_health']
        round_num = 1
        
        while player1_health > 0 and player2_health > 0 and round_num <= 5:
            # player 1 turn
            challenge_word = random.choice(all_words)
            scrambled = ''.join(random.sample(challenge_word, len(challenge_word)))
            
            embed = discord.Embed(
                title=f'round {round_num} - {ctx.author.name} turn',
                description=f'unscramble: {scrambled}',
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            
            def check_player1(message):
                return message.author == ctx.author and message.channel == ctx.channel
            
            try:
                answer = await self.bot.wait_for('message', timeout=15.0, check=check_player1)
                
                if answer.content.lower() == challenge_word.lower():
                    damage = self.calculate_battle_score(challenge_word, player1_char['word_power'])
                    player2_health -= damage
                    result = f"correct. {damage} damage to opponent"
                else:
                    result = f"wrong. the word was {challenge_word}"
            except:
                result = "time's up"
            
            await ctx.send(result)
            
            if player2_health <= 0:
                break
            
            # player 2 turn
            challenge_word = random.choice(all_words)
            scrambled = ''.join(random.sample(challenge_word, len(challenge_word)))
            
            embed = discord.Embed(
                title=f'round {round_num} - {opponent.name} turn',
                description=f'unscramble: {scrambled}',
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            
            def check_player2(message):
                return message.author == opponent and message.channel == ctx.channel
            
            try:
                answer = await self.bot.wait_for('message', timeout=15.0, check=check_player2)
                
                if answer.content.lower() == challenge_word.lower():
                    damage = self.calculate_battle_score(challenge_word, player2_char['word_power'])
                    player1_health -= damage
                    result = f"correct. {damage} damage to opponent"
                else:
                    result = f"wrong. the word was {challenge_word}"
            except:
                result = "time's up"
            
            await ctx.send(result)
            
            round_num += 1
        
        # determine winner
        if player1_health > 0:
            winner = ctx.author
            loser_id = player2_id
            winner_id = player1_id
            winner_name = player1_char['name']
        else:
            winner = opponent
            loser_id = player1_id
            winner_id = player2_id
            winner_name = player2_char['name']
        
        # update stats
        characters[winner_id]['victories'] += 1
        self.save_characters(characters)
        
        embed = discord.Embed(
            title='battle over',
            description=f"{winner_name} wins the battle",
            color=discord.Color.gold()
        )
        embed.add_field(name='final health', value=f"winner: {max(player1_health, player2_health)}", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Battles(bot))
