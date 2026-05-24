# scribebot v2

a discord bot for a medieval word-based rpg game. second version to old scribebot.

## features

- medieval fantasy rpg with word challenges
- character creation and progression system
- collect loot and unlock spells through word gameplay
- battle system based on vocabulary and word length
- persistent player data and character saves
- leaderboard tracking word scores and battles won

## requirements

- python 3.8+
- discord.py
- python-dotenv

## installation

1. clone the repository:
```bash
git clone https://github.com/ImportantNoone/ScribeBot-V2.git
cd ScribeBot-V2
```

2. install dependencies:
```bash
pip install -r requirements.txt
```

3. create a .env file in the root directory:
```
discord_token=your_bot_token_here
```

4. run the bot:
```bash
python bot.py
```

## commands

### character
- !create_character - create your medieval character
- !character - view your current character stats
- !stats - see your detailed progression

### gameplay
- !challenge - start a word challenge
- !battle - challenge another player to a word battle
- !inventory - view your collected loot
- !spells - see your unlocked spells

### general
- !leaderboard - view top players
- !help - display all commands

## how to get your bot token

1. go to discord developer portal
2. click new application
3. go to the bot tab and click add bot
4. under token, click copy
5. paste it in your .env file

## invite bot to server

1. in developer portal, go to oauth2 > url generator
2. select scopes: bot
3. select permissions: send messages, read messages/view channels, manage messages
4. copy the generated url and open it in your browser

## gameplay overview

scribebot v2 is a word-based rpg where players engage in linguistic challenges to defeat enemies and gain power. create your character, complete word challenges, battle other players, and climb the leaderboard.


## license

mit license
