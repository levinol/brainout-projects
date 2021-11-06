# Discord suggestion bot
Containerized Submission/Suggestion automatization bot. The bot combines regular and slash commands for comfortable use.

## Frontend features implemented in the bot

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

## Backend features 

Links under titles lead to raw code examples

#### 1. Simple database init.sql file to create schema bot will work with
[Raw code example](init.sql)
#### 2. Connect to database with psycopg2 
[Raw code example](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L57)
#### 3. SELECT/UPDATE/INSERT INTO/DELETE sql commands inside bot functions
[Raw code example](https://github.com/levinol/brainout-projects/blob/af5eb9e7aad2a770ae88f502bf47ceb57b670068/discord-suggestion-bot/bot-src/bot.py#L122-L128)
