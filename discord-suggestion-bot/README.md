# Discord suggestion bot
Containerized Submission/Suggestion automatization bot. The bot combines regular and slash commands for comfortable use.

## Frontend features implemented in the bot

When using a bot, it is assumed that only slash commands are used. 
When a user attaches files, the bot uses standard commands. Thus, without affecting the user experience.

Links on titles lead to visual examples, links under them lead to [bot.py](discord-suggestion-bot/bot-src/bot.py) functions 

#### 1. [Voice channel with display of necessary statistic](bot-src/online_channel_edit_example.gif)
[Raw code example](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L97-L102)
#### 2. [Help page with dropdown menu](bot-src/help_dropdown_example.gif)
[Raw code example](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L300-L320)
#### 3. [Embed messages with url buttons for attached files](bot-src/url_buttons_example.png)
[Raw code example](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L397-L442)
#### 4. [Slash commands with select options and limited permission commands for staff](bot-src/bottools_command_with_select_example.gif)
[Raw code example](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L1116-L1162)
#### 5. [Convert replies on embed message into comments](bot-src/reply_to_comment_example.gif)
[Raw code example](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L104-L132)

## Backend features implemented in the bot

The bot's backend is needed to assign the author to each embed message. The database stores the user's ID with embed messages ids, 
allowing to create functions to check embed ownership.

Links under titles lead to raw code examples

#### 1. Simple database init.sql file to create schema bot will work with
[Raw code example](init.sql)
#### 2. Connect to database with psycopg2 
[Raw code example](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L57)
#### 3. SELECT/UPDATE/INSERT INTO/DELETE sql commands inside bot functions
[Raw code example](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L122-L128)

## How to host/launch bot

Since the solution is containerized you only need to change the roles, channels and other ID values.
#### 1. [config.py](bot-src/config.py)
Change channels ids in [```settings``` dictionary](https://github.com/levinol/brainout-projects/blob/bf8e935cfae6fb6148f71f5cead06fe17ec4d6a4/discord-suggestion-bot/bot-src/config.py#L1-L13) and roles ids in [```roles``` dictionary](https://github.com/levinol/brainout-projects/blob/bf8e935cfae6fb6148f71f5cead06fe17ec4d6a4/discord-suggestion-bot/bot-src/config.py#L17-L23)
#### 2. [bot.py](bot-src/bot.py)
Change [```guild_ids``` array](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L607) in **all** slash commands and [guild_id](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L1223) in permissions commands
#### 3. [docker-compose.yaml](bot-src/docker-compose.yaml)
Change [```BOT_TOKEN```](https://github.com/levinol/brainout-projects/blob/bf8e935cfae6fb6148f71f5cead06fe17ec4d6a4/discord-suggestion-bot/docker-compose.yaml#L30) to your bot token

[```BOTGATE_CHANNEL```](https://github.com/levinol/brainout-projects/blob/bf8e935cfae6fb6148f71f5cead06fe17ec4d6a4/discord-suggestion-bot/docker-compose.yaml#L31) - set the id of the channel in which the commands will be active to use

[```*_REACTION_EMOJI_ID```](https://github.com/levinol/brainout-projects/blob/bf8e935cfae6fb6148f71f5cead06fe17ec4d6a4/discord-suggestion-bot/docker-compose.yaml#L33-L35) - set the id of custom emojis that will be added on every embed message

### Run bot with ```docker-compose up --build``` from the directory with the docker-compose.yaml file

##### I hope my bot example will help you with the development and hosting your own bot
