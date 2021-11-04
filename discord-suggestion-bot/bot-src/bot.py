from asyncio import events
import re
import discord
from discord import activity
from discord import role
from discord.channel import VoiceChannel
from discord.embeds import Embed, EmptyEmbed
from discord.emoji import Emoji
from discord.ext import commands
from discord.flags import PublicUserFlags
from discord.utils import get

from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

import json
import requests
from threading import Timer
import datetime
import os

from config import *

client = commands.Bot(command_prefix=settings['prefix'], activity=discord.Activity(type=discord.ActivityType.watching, name='Use '+settings['prefix']+'help'))
slash = SlashCommand(client, sync_commands=True)


token = os.getenv('BOT_TOKEN')
submit_id = settings['submit_channel']
submit_final_id = settings['submit_final_channel']
suggest_id = settings['suggest_channel']
event_id = int(os.getenv('EVENT_CHANNEL_ID'))
server_id = settings['suggest_server_channel']
online_id = settings['online_channel']
embed_channels = [submit_id, submit_final_id, suggest_id, server_id, event_id]

botgate_id = 873900855676526643

subm_embed = Embed.from_dict(submission_embed)
sugst_embed = Embed.from_dict(suggestion_embed)
help_emb = Embed.from_dict(help_embed)
help_emb_disabled = Embed.from_dict(help_embed_slash_disabled)
message_id_emb = Embed.from_dict(message_id_embed)

positive_emoji_id = int(os.getenv('POSITIVE_REACTION_EMOJI_ID'))
neutral_emoji_id = int(os.getenv('NEUTRAL_REACTION_EMOJI_ID'))
negative_emoji_id = int(os.getenv('NEGATIVE_REACTION_EMOJI_ID'))

import psycopg2

# Connect to postgres DB
conn = psycopg2.connect(dbname="brainout", user="admin", password="password", host="postgres")

# check if author of original message has same id as author_id
def author_id_check(msg_id: str, author_id: str, channel_type: str) -> bool:
    is_author_flag = False
    with conn.cursor() as cursor:
        conn.autocommit = True
        if channel_type == 'submission':
            cursor.execute("SELECT author_id FROM brainout.submissions WHERE msg_id = %s", (msg_id,))
        elif channel_type == 'suggestion':
            cursor.execute("SELECT author_id FROM brainout.suggestions WHERE msg_id = %s", (msg_id,))
        result = cursor.fetchone()
        if author_id in result:
            is_author_flag = True
    return is_author_flag

# standart help page without slash commands
@client.remove_command('help')
@client.command()
async def help(ctx, task_typo=None):
    if ctx.channel.id != botgate_id:
        bot_respond = await ctx.send(f'{ctx.message.author.mention}, this command works only in <#{botgate_id}> channel')
        await delete_with_react(bot_respond)
        await delete_with_react(ctx.message)
        return None
    if task_typo == "suggestion":
        await ctx.send(embed=sugst_embed)
    elif task_typo == "submission":
        await ctx.send(embed=subm_embed)
    elif task_typo == "message_id":
        message_id_file = discord.File("message_id.gif", filename="message_id.gif")
        await ctx.send(file=message_id_file, embed=message_id_emb.set_image(url="attachment://message_id.gif"))
    else:
        slash_on = discord.File("slash_on.gif", filename="slash_on.gif")
        await ctx.send(file=slash_on, embed=help_emb_disabled.set_image(url="attachment://slash_on.gif"))
    await delete_with_react(ctx.message)

import requests
from discord.ext import tasks

# Get current online of brain/out 
@tasks.loop(minutes=10)
async def OnlinePlayersUpdate():
    VoiceChannel = await client.fetch_channel(online_id)
    r=requests.get(update_url)
    await VoiceChannel.edit(name=f"Online: {r.json()['players']}")

# Add comment to embed msg (ahaha these code comments are so helpfull)
async def add_сomment(comment, mode): 
    submit_channel = client.get_channel(comment.channel.id)
    msg = await submit_channel.fetch_message(comment.reference.message_id)
    embed = msg.embeds[0]
    comment_time = comment.created_at.strftime("%A, %d %b %Y %H:%M") + ' UTC'
    embed.add_field(name=f"❗{mode} comment - {comment_time}❗", value=comment.content, inline = False)
    await msg.edit(embed=embed)


async def delete_with_react(msg):
    await msg.add_reaction("🚮")
    await msg.delete(delay=7)

# Clear comment section
def clear_comments(embed_message):
    embed_dict = embed_message.to_dict()

    if 'fields' in embed_dict:
        mode_array = dumb_emoji_dict.values()
        
        # Ughh so this is one-line for inside one-line for if
        # This code check if field in embed msg is comment and doent include it to final embed msg 
        new_fields = [field for field in embed_dict['fields'] if not field['name'].startswith(tuple([f'❗{mode} comment' for mode in mode_array]))]
        
        print(new_fields)

        embed_dict['fields'] = new_fields
    
    return Embed.from_dict(embed_dict)


# Change embed color due to reacts count
async def reaction_count(payload):
    if payload.channel_id in embed_channels:
        submit_channel =client.get_channel(payload.channel_id)
        msg = await submit_channel.fetch_message(payload.message_id)

        positive_emoji = client.get_emoji(id=positive_emoji_id)
        react1 = get(msg.reactions, emoji=positive_emoji)

        negative_emoji = client.get_emoji(id=negative_emoji_id)
        react2 = get(msg.reactions, emoji=negative_emoji)
        embed_from_msg = msg.embeds[0]

        react1 = react1.count
        react2 = react2.count

        if react1 > 2 and react2 < 2:
            #Move to final if paylod == submission channel id
            embed_from_msg.colour = 0x3CB371

            if payload.channel_id == submit_id:
                with conn.cursor() as cursor:
                    conn.autocommit = True
                    cursor.execute("SELECT in_final FROM brainout.submissions WHERE msg_id = %s", (str(msg.id),))
                    result = cursor.fetchone()

                if result[0]:
                    # already in finals
                    pass
                else:
                    with conn.cursor() as cursor:
                        conn.autocommit = True
                        cursor.execute("UPDATE brainout.submissions SET in_final = %s WHERE msg_id = %s", (True, str(msg.id),))

                    delivery_channel = client.get_channel(submit_final_id)

                    dispatched_embed = embed_from_msg.copy()
                    
                    dispatched_embed = clear_comments(dispatched_embed)

                    dispatched_embed_msg = await delivery_channel.send(embed=dispatched_embed)

                    dispatched_embed.set_footer(text='Message ID: '+ str(dispatched_embed_msg.id))

                    dispatched_embed.add_field(name='Link to primary message:', inline=False, value=f'[Link to message in <#{submit_id}>]({msg.jump_url})')

                    await dispatched_embed_msg.edit(embed=dispatched_embed)

                    positive_emoji = client.get_emoji(id=positive_emoji_id)
                    await dispatched_embed_msg.add_reaction(positive_emoji)

                    neutral_emoji = client.get_emoji(id=neutral_emoji_id)
                    await dispatched_embed_msg.add_reaction(neutral_emoji)

                    negative_emoji = client.get_emoji(id=negative_emoji_id)
                    await dispatched_embed_msg.add_reaction(negative_emoji)   
        elif react2 > 2:
            # delete 
            # TODO think about it
            embed_from_msg.colour = 0xFF0000
        elif react1 > react2:
            embed_from_msg.colour = 0x228B22
        elif react1 == react2:
            embed_from_msg.colour = 0xFFFFFF 
        else:
            embed_from_msg.colour = 0xFF8C00

        await msg.edit(embed=embed_from_msg)

# Event handlers for embed reacts count
@client.event
async def on_raw_reaction_add(payload): 
    await reaction_count(payload)

@client.event
async def on_raw_reaction_remove(payload):
    await reaction_count(payload)

# Every msg handler
@client.event
async def on_message(message):
    await client.process_commands(message)

    # Check if this message is reply 
    if message.reference is not None: 
        if message.channel.id in [settings['submit_channel'], settings['submit_final_channel'], settings['suggest_channel'], settings['suggest_server_channel']]: # обрабатываем сообщения в канале sumbit_channel
            submit_channel = client.get_channel(message.channel.id)
            
            #role check
            roles_ids = []
            for r in message.author.roles:
                roles_ids.append(r.id)

            
            
            for role, mode in dumb_emoji_dict.items():
                if roles[role] in roles_ids:
                    await add_сomment(message, mode)
                    break
            
            # Delete reply
            await message.delete()



# NEW ERA of SLASH COMMANDS
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_button, create_select, create_select_option, create_actionrow

help_select = create_select(
    options=[# the options in your dropdown
         create_select_option("'Submission' commands", value="submission", emoji="🙈"),
        create_select_option("'Suggestion' commands", value="suggestion", emoji="🙉"),
        create_select_option("How to get message_id", value="message_id", emoji="🙊"),
    ],
    placeholder="Choose your help page",  # the placeholder text to show when no options have been chosen
    min_values=1,  # the minimum number of options a user must select
    max_values=1,  # the maximum number of options a user can select
)

@slash.slash(
    name="help",
    description="Get help page",
    guild_ids=[873835757238894592]
)
async def _help(ctx):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None
    await ctx.send(embed=help_emb, components=[create_actionrow(help_select)])

@client.event
async def on_component(ctx):
    # ctx.selected_options is a list of all the values the user selected
    if ctx.selected_options[0] == "suggestion":
        await ctx.send(embed=sugst_embed, hidden=True)
    elif ctx.selected_options[0] == "submission":
        await ctx.send(embed=subm_embed, hidden=True)
    elif ctx.selected_options[0] == "message_id":
        message_id_file = discord.File("message_id.gif", filename="message_id.gif")
        await ctx.send(file=message_id_file, embed=message_id_emb.set_image(url="attachment://message_id.gif"), hidden=True)
    else:
        await ctx.send('uhhh im stuck')

# handler for slash commands that were sent with the file
async def send_embed_with_file(ctx, args, channel_id, sep_1, sep_2, image_req):
    author = ctx.message.author
    arg_partition = args.partition(sep_2)
    if arg_partition[0]!= '':
        msg_desc = arg_partition[2]
        msg_title = arg_partition[0].partition(sep_1)[2]
    else:
        msg_desc = arg_partition[2].partition(sep_1)[0]
        msg_title = arg_partition[2].partition(sep_1)[2]

    if msg_desc == '': msg_desc = discord.Embed.Empty

    msg_id = await create_embed_with_reactions(ctx, msg_title, msg_desc, channel_id, image_req)    

    return msg_id

from discord_slash.context import ComponentContext

# handler for slash commands that were sent with the file
async def add_file_to_embed(ctx, args, sep_1, sep_2, channel_flag):
    arg_partition = args.partition(sep_2)
    if arg_partition[0]!= '':
        message = arg_partition[2]
        message_id = arg_partition[0].partition(sep_1)[2]
    else:
        message = arg_partition[2].partition(sep_1)[0]
        message_id = arg_partition[2].partition(sep_1)[2]
    
    message = message.strip()
    message_id = message_id.strip()

    # looking for message
    msg =  await msg_fetch(ctx, message_id, channel_flag)

    if msg == 0:
        return 0

    print(str(message_id),str(ctx.message.author.id), channel_flag )

    is_author_flag = author_id_check(str(message_id),str(ctx.message.author.id), channel_flag )

    if is_author_flag:
        #get msg
        embed = msg.embeds[0]
        # Checking for the existence of a field with a comment and updating / adding it
        if message: 
            embed_dict = embed.to_dict()
            temp_flag = 0
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    if field['name'] == "Addition":
                        temp_flag = 1
                        field['value'] = message

            if temp_flag:
                embed = Embed.from_dict(embed_dict)
            else:
                embed.add_field(name="Addition", value=message, inline = False)

        # FIXME 
        try:

            url_link = ctx.message.attachments[0].url
            url_file = url_link[url_link.rfind('.')+1:].upper()

            embed_dict = embed.to_dict()
            field_values = ''
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    if field['name'] == "Provided files":
                        field_values = field['value']
                        field['value'] += '\n' + url_link

            if field_values:
                # Get current buttons from msg
                url_buttons = []
                for url_iterator in field_values.split('\n'):
                    url_buttons.append(create_button(
                        style=ButtonStyle.URL,
                        label=url_iterator[url_iterator.rfind('.')+1:].upper(),
                        url=url_iterator
                        )
                    )
                embed = Embed.from_dict(embed_dict)
            else:
                url_buttons = []
                embed.add_field(name="Provided files", value=url_link, inline = False)
             

            url_buttons.append(create_button(
                style=ButtonStyle.URL,
                label=url_file,
                url=url_link
                )
            )

        except:
            bot_respond = await ctx.send(f'{ctx.message.author.mention}, what about image?')
            await delete_with_react(bot_respond)
            return 0

        # TODO discord_slash.error.IncorrectFormat: Number of components in one row should be between 1 and 5.
        await msg.edit(embed=embed, components=[create_actionrow(*url_buttons)])

    else:
        await ctx.send(f'{ctx.message.author.mention}, that\'s not your message 😡')
        # Delete original message
        await delete_with_react(ctx.message)   

# Add addition to embed msg 
async def add_text_to_embed(ctx, message, message_id, channel_flag):
    # Looking for msg
    msg =  await msg_fetch_slash(ctx, message_id, channel_flag)

    if msg == 0:
        return 0

    is_author_flag = author_id_check(str(message_id),str(ctx.author.id), channel_flag )

    if is_author_flag:
        #get msg
        embed = msg.embeds[0]
        # Checking for the existence of a field with a comment and updating / adding it
        if message: 
            embed_dict = embed.to_dict()
            temp_flag = 0
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    if field['name'] == "Addition":
                        temp_flag = 1
                        field['value'] = message

            if temp_flag:
                embed = Embed.from_dict(embed_dict)
                
            else:
                embed.add_field(name="Addition", value=message, inline = False)

        # FIXME 
        try:
            embed.insert_field_at(index=999, name="Provided file", value=ctx.message.attachments[0].url, inline = False)
            await ctx.send('File was provided' ,hidden=True)
            
        except:
            # TODO check if slash commands now can work with file attachments
            pass

        await msg.edit(embed=embed)
        await ctx.send('Addition was replaced', hidden=True) if temp_flag else await ctx.send('Addition was added', hidden=True)
    else:
        await ctx.send(f'{ctx.author.mention}, that\'s not your message 😡')
  
# Get msg from any of 4 channels
async def msg_fetch(ctx, message_id, channel_flag):
    # Looking for msg
    first_channel = client.get_channel(submit_id) if channel_flag == "submission" else client.get_channel(suggest_id)
    second_channel = client.get_channel(event_id) if channel_flag == "submission" else client.get_channel(server_id)

    flag = 0

    try:
        msg = await first_channel.fetch_message(message_id)
    except discord.errors.NotFound:
        flag = 1
    
    if flag:
        try:
            msg = await second_channel.fetch_message(message_id)
        except discord.errors.NotFound:
            bot_respond = await ctx.send(f'{ctx.message.author.mention}, cant find your msg by id.')
            await delete_with_react(bot_respond)
            return 0  
    return msg

# Get msg from any of 4 channels. Feedback with hidden=true parameter
async def msg_fetch_slash(ctx, message_id, channel_flag):
    # Looking for msg
    first_channel = client.get_channel(submit_id) if channel_flag == "submission" else client.get_channel(suggest_id)
    second_channel = client.get_channel(event_id) if channel_flag == "submission" else client.get_channel(server_id)

    flag = 0

    try:
        msg = await first_channel.fetch_message(message_id)
    except discord.errors.NotFound:
        flag = 1
    
    if flag:
        try:
            msg = await second_channel.fetch_message(message_id)
        except discord.errors.NotFound:
            bot_respond = await ctx.send(f'{ctx.author.mention}, cant find your msg by id.', hidden=True)
            return 0  
    return msg

# Create embed msg in channel_id
async def create_embed_with_reactions(ctx, msg_title, msg_desc,channel_id, image_req: bool ) -> None:
    author = ctx.author

    embed=discord.Embed(title=msg_title, description=msg_desc, color=0xFFFFFF, timestamp=datetime.datetime.utcnow())
    embed.set_author(name=author.display_name, icon_url=author.avatar_url)

    #Image check
    try:
        embed.set_image(url=ctx.message.attachments[0].url)
    except:
        if image_req:
            bot_respond = await ctx.send(f'{author.mention}, what about image?')
            await delete_with_react(bot_respond)
            return 0
        else:
            pass
    
    delivery_channel = client.get_channel(channel_id)
    dispatched_embed = await delivery_channel.send(embed=embed)

    embed.set_footer(text='Message ID: '+ str(dispatched_embed.id))

    await dispatched_embed.edit(embed=embed)

    positive_emoji = client.get_emoji(id=positive_emoji_id)
    await dispatched_embed.add_reaction(positive_emoji)

    neutral_emoji = client.get_emoji(id=neutral_emoji_id)
    await dispatched_embed.add_reaction(neutral_emoji)

    negative_emoji = client.get_emoji(id=negative_emoji_id)
    await dispatched_embed.add_reaction(negative_emoji) 

    return str(dispatched_embed.id)

# Clear addition fields if there are no 'role' comments
async def clear_embed(ctx, message_id, channel_flag):

    msg =  await msg_fetch_slash(ctx, message_id, channel_flag)
    if msg == 0:
        return 0

    is_author_flag = author_id_check(str(message_id),str(ctx.author.id), channel_flag)

    if is_author_flag:
        embed = msg.embeds[0]
        # check if any comment exists
        embed_dict = embed.to_dict()
        temp_flag = 0
        if 'fields' in embed_dict:
            for field in embed_dict['fields']:
                if 'comment' in field['name']:
                    temp_flag = 1

        if temp_flag:
                #role check
            roles_ids = []
            for r in ctx.author.roles:
                roles_ids.append(r.id)

            if set(roles.values()).intersection(set(roles_ids)):
                embed.clear_fields()
                await msg.edit(embed=embed)
            else:
                await ctx.send(f"{ctx.author.mention}, the message contains someone else's comment, I cannot clear it", hidden=True)
        else:
            embed.clear_fields()
            await msg.edit(embed=embed)
            await ctx.send('Fields cleared', hidden=True)

    else:
        await ctx.send(f'{ctx.author.mention}, that\'s not your message 😡')

from discord_slash.model import ButtonStyle

@slash.slash(
    name="hello",
    description="Say hello to botti",
    guild_ids=[873835757238894592]
)
async def _hello(ctx:SlashContext): 
    url_bottons = [create_button(
        style=ButtonStyle.URL,
        label="Press to spend all ur moneybags",
        url='https://brainout.org/'
        ),
        ]
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None
    msg = await ctx.send(f'Hello, {ctx.author.mention}!')
    await msg.edit(components=[create_actionrow(*url_bottons)])

# submission part
@slash.subcommand(
    base="submission",
    name="main", 
    description="Make a submission in main channel", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="artwork_name",
            description="Name of your artwork",
            option_type=3,
            required=True
        ),
        create_option(
            name="description",
            description="Optional description of your work",
            option_type=3,
            required=False
        )
    ]
    )
async def _submission_main(ctx, artwork_name, description=None):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None
    author = ctx.author
    
    #Divide into title and desc
    if description:
        msg_title = artwork_name
        msg_desc = description
    else:
        msg_title = artwork_name
        msg_desc = discord.Embed.Empty 

    msg_id = await create_embed_with_reactions(ctx, msg_title, msg_desc, submit_id, image_req=True)

    if len(str(msg_id)) < 2:
        await ctx.send(f'{author.mention}, ask helper to update message id of your embed')
    else:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f"INSERT INTO brainout.submissions(author_id, msg_id, in_final) VALUES ({author.id}, {msg_id}, {False})")
        await ctx.send(f'{author.mention}, provide the files in necessary format wia add command', hidden=True)  

@slash.subcommand(
    base="submission",
    name="event", 
    description="Make a submission in event channel", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="artwork_name",
            description="Name of your artwork",
            option_type=3,
            required=True
        ),
        create_option(
            name="description",
            description="Optional description of your work",
            option_type=3,
            required=False
        )
    ]
    )
async def _submission_event(ctx, artwork_name, description=None):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None
    
    if event_id:
        pass
    else:
        await ctx.send('No active event', hidden=True)
        return 0
    author = ctx.author
    
    #Divide into title and desc
    if description:
        msg_title = artwork_name
        msg_desc = description
    else:
        msg_title = artwork_name
        msg_desc = discord.Embed.Empty 

    msg_id = await create_embed_with_reactions(ctx, msg_title, msg_desc, event_id, image_req=True)

    if len(str(msg_id)) < 2:
        await ctx.send(f'{author.mention}, ask helper to update message id of your embed')
    else:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f"INSERT INTO brainout.submissions(author_id, msg_id, in_final) VALUES ({author.id}, {msg_id}, {False})")
        await ctx.send(f'{author.mention}, provide the files in necessary format wia add command', hidden=True)  

# submit command creates an embed message, adds the message_id and reactions immediately after creation.
# _submission_main command with attached image
# _submission_add command with attached image
@client.command()
async def submission(ctx, *, args): 
    if ctx.channel.id != botgate_id:
        bot_respond = await ctx.send(f'{ctx.message.author.mention}, this command works only in <#{botgate_id}> channel')
        await delete_with_react(bot_respond)
        await delete_with_react(ctx.message)
        return None
    command_type, args=args.split(' ',1)
    print(command_type, args)
    msg = args
    author = ctx.message.author
    if command_type == 'main':
        msg_id = await send_embed_with_file(ctx, args, submit_id, "artwork_name:", "description:", image_req=True)
        if len(str(msg_id)) < 2:
            await ctx.send(f'{author.mention}, ask helper to update message id of your embed')
        else:
            with conn.cursor() as cursor:
                conn.autocommit = True
                cursor.execute(f"INSERT INTO brainout.submissions(author_id, msg_id, in_final) VALUES ({author.id}, {msg_id}, {False})")
                bot_respond = await ctx.reply(f'{author.mention}, Submission was successfully created')
            await delete_with_react(bot_respond) if bot_respond else await ctx.reply(f'{author.mention}, Submission was not successfully created')
    elif command_type == 'event':
        if event_id:
            pass
        else:
            await ctx.send('No active event')
            return 0
        msg_id = await send_embed_with_file(ctx, args, event_id, "artwork_name:", "description:", image_req=True)
        if len(str(msg_id)) < 2:
            await ctx.send(f'{author.mention}, ask helper to update message id of your embed')
        else:
            with conn.cursor() as cursor:
                conn.autocommit = True
                cursor.execute(f"INSERT INTO brainout.submissions(author_id, msg_id, in_final) VALUES ({author.id}, {msg_id}, {False})")
                bot_respond = await ctx.reply(f'{author.mention}, Submission was successfully created')
            await delete_with_react(bot_respond) if bot_respond else await ctx.reply(f'{author.mention}, Submission was not successfully created')
    elif command_type == 'add':
        await add_file_to_embed(ctx, args, "message_id:", "message:", channel_flag="submission")    
    else:
        await ctx.send('uhh im stuck')

@slash.subcommand(
    base="submission",
    name="add",
    description="Add an attachment to a submission", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id from submission",
            option_type=3,
            required=True
        ),
        create_option(
            name="message",
            description="Message for addition field",
            option_type=3,
            required=False
        )
    ]
    )
async def _submission_add(ctx, message_id, message=None):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None
    await add_text_to_embed(ctx, message, message_id, channel_flag="submission")

@slash.subcommand(
    base="submission",
    name="addition",
    description="Add an addition to a submission", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id from submission",
            option_type=3,
            required=True
        ),
        create_option(
            name="message",
            description="Message for addition field",
            option_type=3,
            required=True
        )
    ]
    )
async def _submission_addition(ctx, message_id, message):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None
    await add_text_to_embed(ctx, message, message_id, channel_flag="submission")

@slash.subcommand(
    base="submission",
    name="сlear",
    description="Clear all optional description fields", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id from submission",
            option_type=3,
            required=True
        )
    ]
    )
async def _submission_clear(ctx, message_id):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None
    await clear_embed(ctx, message_id, "submission")

@slash.subcommand(
    base="submission",
    name="remove",
    description="Remove a submission", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id from submission",
            option_type=3,
            required=True
        )
    ]
    )
async def _submission_remove(ctx, message_id):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None

    msg =  await msg_fetch_slash(ctx, message_id, "submission")
    if msg == 0:
        return 0

    is_author_flag = author_id_check(str(message_id),str(ctx.author.id), 'submission' )

    if is_author_flag:
        await msg.delete(delay=5)
        await ctx.send('Message deleted', hidden=True)
    else:
        await ctx.send(f'{ctx.author.mention}, that\'s not your message 😡')

# suggestion part
@slash.subcommand(
    base="suggestion",
    name="main", 
    description="Make a suggestion in main channel", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="suggestion_topic",
            description="The topic of your suggestion",
            option_type=3,
            required=True
        ),
        create_option(
            name="description",
            description="Description of your suggestion",
            option_type=3,
            required=True
        )
    ]
    )
async def _suggestion_main(ctx, suggestion_topic, description=None):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None

    author = ctx.author
    
    # Divide into title and desc
    if description:
        msg_title = suggestion_topic
        msg_desc = description
    else:
        msg_title = suggestion_topic
        msg_desc = discord.Embed.Empty 
    
    msg_id = await create_embed_with_reactions(ctx, msg_title, msg_desc, suggest_id , image_req=False)
    if len(str(msg_id)) < 2:
        await ctx.send(f'{author.mention}, ask helper to update message id of your embed')
    else:
        db_flag = 0
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f"INSERT INTO brainout.suggestions(author_id, msg_id) VALUES ({author.id}, {msg_id})")
            db_flag = 1
            await ctx.send(f'Suggestion was successfully created', hidden=True)
        await ctx.send(f'{author.mention}, provide the files in necessary format wia add command', hidden=True) if db_flag else await ctx.send(f'{author.mention}, Suggestion was not successfully created')



# suggest command creates embed msg, adding message_id and reactions immediately after creation
# _suggestion_main command with attached image
@client.command()
async def suggestion(ctx, *, args): 
    if ctx.channel.id != botgate_id:
        bot_respond = await ctx.send(f'{ctx.message.author.mention}, this command works only in <#{botgate_id}> channel')
        await delete_with_react(bot_respond)
        await delete_with_react(ctx.message)
        return None
    
    command_type, args=args.split(' ',1)
    print(command_type, args)
    msg = args
    author = ctx.message.author
    if command_type == 'main':
        msg_id = await send_embed_with_file(ctx, args, suggest_id, "suggestion_topic:", "description:", image_req=False)
        if len(str(msg_id)) < 2:
            await ctx.send(f'{author.mention}, ask helper to update message id of your embed')
        else:
            with conn.cursor() as cursor:
                conn.autocommit = True
                cursor.execute(f"INSERT INTO brainout.suggestions(author_id, msg_id) VALUES ({author.id}, {msg_id})")
                bot_respond = await ctx.reply(f'{author.mention}, Suggestion was successfully created')
            await delete_with_react(bot_respond) if bot_respond else await ctx.reply(f'{author.mention}, Suggestion was not successfully created')
    elif command_type == 'server':
        msg_id = await send_embed_with_file(ctx, args, server_id,"suggestion_topic:",  "description:", image_req=False)
        if len(str(msg_id)) < 2:
            await ctx.send(f'{author.mention}, ask helper to update message id of your embed')
        else:
            with conn.cursor() as cursor:
                conn.autocommit = True
                cursor.execute(f"INSERT INTO brainout.suggestions(author_id, msg_id) VALUES ({author.id}, {msg_id})")
                bot_respond = await ctx.reply(f'{author.mention}, Suggestion was successfully created')
            await delete_with_react(bot_respond) if bot_respond else await ctx.reply(f'{author.mention}, Suggestion was not successfully created')
    elif command_type == 'add':
        await add_file_to_embed(ctx, args, "message_id:", "message:", channel_flag="suggestion")
    else:
        await ctx.send('uhh im stuck')

@slash.subcommand(
    base="suggestion",
    name="server",
    description="Make a suggestion in event channel", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="suggestion_topic",
            description="The topic of your suggestion",
            option_type=3,
            required=True
        ),
        create_option(
            name="description",
            description="Description of your suggestion",
            option_type=3,
            required=True
        )
    ]
    )
async def _suggestion_server(ctx, suggestion_topic, description=None):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None

    author = ctx.author
    
    # Divide into title and desc
    if description:
        msg_title = suggestion_topic
        msg_desc = description
    else:
        msg_title = suggestion_topic
        msg_desc = discord.Embed.Empty 

    msg_id = await create_embed_with_reactions(ctx, msg_title, msg_desc, server_id , image_req=False)
    if len(str(msg_id)) < 2:
        await ctx.send(f'{author.mention}, ask helper to update message id of your embed')
    else:   
        db_flag = 0
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f"INSERT INTO brainout.suggestions(author_id, msg_id) VALUES ({author.id}, {msg_id})")
            db_flag = 1
            await ctx.send(f'Suggestion was successfully created', hidden=True)
        await ctx.send(f'{author.mention}, provide the files in necessary format wia add command', hidden=True) if db_flag else await ctx.send(f'{author.mention}, Suggestion was not successfully created')


@slash.subcommand(
    base="suggestion",
    name="add",
    description="Add an attachment to a suggestion", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id from suggestion",
            option_type=3,
            required=True
        ),
        create_option(
            name="message",
            description="Message for addition field",
            option_type=3,
            required=False
        )
    ]
    )
async def _suggestion_add(ctx, message_id, message):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None
    await add_text_to_embed(ctx, message, message_id, channel_flag="suggestion")

@slash.subcommand(
    base="suggestion",
    name="addition",
    description="Add an addition to a suggestion", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id from suggestion",
            option_type=3,
            required=True
        ),
        create_option(
            name="message",
            description="Message for addition field",
            option_type=3,
            required=True
        )
    ]
    )
async def _suggestion_addition(ctx, message_id, message):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None

    await add_text_to_embed(ctx, message, message_id, channel_flag="suggestion")

@slash.subcommand(
    base="suggestion",
    name="сlear",
    description="Clear all optional description fields", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id from suggestion",
            option_type=3,
            required=True
        )
    ]
    )
async def _suggestion_clear(ctx, message_id):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None

    await clear_embed(ctx, message_id, "suggestion")

@slash.subcommand(
    base="suggestion",
    name="remove",
    description="Remove a suggestion", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id from suggestion",
            option_type=3,
            required=True
        )
    ]
    )
async def _suggestion_remove(ctx, message_id):
    if ctx.channel_id != botgate_id:
        await ctx.send(f'This slash command works only in <#{botgate_id}> channel', hidden=True)
        return None

    msg =  await msg_fetch_slash(ctx, message_id, "suggestion")
    if msg == 0:
        return 0

    is_author_flag = author_id_check(str(message_id),str(ctx.author.id), 'suggestion' )

    if is_author_flag:
        await msg.delete(delay=5)
        await ctx.send('Message deleted', hidden=True)
    else:
        await ctx.send(f'{ctx.author.mention}, that\'s not your message 😡')

# Mod tools
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

@slash.subcommand(
    base="bottools",
    name="update_msg_id",
    description="Update footer with msg_id of embed message", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id",
            option_type=3,
            required=True
        ),
        create_option(
            name="channel_flag",
            description="Original msg channel",
            option_type=3,
            required=True,
            choices=[
                  create_choice(
                    name="msg in sumbission channel",
                    value="submission"
                  ),
                  create_choice(
                    name="msg in suggestion channel",
                    value="suggestion"
                  )
            ]
        )
    ],
    base_default_permission=False,
    base_permissions={
        873835757238894592: [
            create_permission(roles['helper'], SlashCommandPermissionType.ROLE, True),
            create_permission(roles['moderator'], SlashCommandPermissionType.ROLE, True),
            create_permission(roles['admin'], SlashCommandPermissionType.ROLE, True),
        ]
    }
    )
async def _bottools_update_msg_id(ctx, message_id, channel_flag):
    dispatched_embed = await msg_fetch_slash(ctx, message_id, channel_flag)
    if dispatched_embed:
        embed = dispatched_embed.embeds[0]
        embed.set_footer(text='Message ID: '+ str(dispatched_embed.id))
        await dispatched_embed.edit(embed=embed)
        await ctx.send('Msg id updated', hidden=True)
    else:
        await ctx.send('Can\'t find the message', hidden=True)

@slash.subcommand(
    base="bottools",
    name="reset_final_flag",
    description="Reset final_flag on msg, so its can appears in finals again", 
    guild_ids=[873835757238894592],
    base_default_permission=False,
    base_permissions={
        873835757238894592: [
            create_permission(roles['helper'], SlashCommandPermissionType.ROLE, True),
            create_permission(roles['moderator'], SlashCommandPermissionType.ROLE, True),
            create_permission(roles['admin'], SlashCommandPermissionType.ROLE, True),
        ]
    },
    options=[
        create_option(
            name="message_id",
            description="Copy message id from suggestion, ONLY FOR SUBMISSIONS",
            option_type=3,
            required=True
        )
    ]
)
async def _bottools_reset_final_flag(ctx, message_id):
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute("UPDATE brainout.submissions SET in_final = %s WHERE msg_id = %s", (False, message_id,))
    await ctx.send('Final flag was reset', hidden=True)

@slash.subcommand(
    base="bottools",
    name="clear_comments",
    description="Wow this command clear comments", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="message_id",
            description="Copy message id",
            option_type=3,
            required=True
        ),
        create_option(
            name="channel_flag",
            description="Original msg channel",
            option_type=3,
            required=True,
            choices=[
                  create_choice(
                    name="msg in sumbission channel",
                    value="submission"
                  ),
                  create_choice(
                    name="msg in suggestion channel",
                    value="suggestion"
                  )
            ]
        )
    ],
    base_default_permission=False,
    base_permissions={
        873835757238894592: [
            create_permission(roles['helper'], SlashCommandPermissionType.ROLE, True),
            create_permission(roles['moderator'], SlashCommandPermissionType.ROLE, True),
            create_permission(roles['admin'], SlashCommandPermissionType.ROLE, True),
        ]
    }
    )
async def _bottools_clear_comments(ctx, message_id, channel_flag):
    msg= await msg_fetch_slash(ctx, message_id, channel_flag)
    if msg:
        msg_embed = msg.embeds[0]
        msg_embed = clear_comments(msg_embed)

        await msg.edit(embed=msg_embed)
        await ctx.send('Comments cleared', hidden=True)
    else:
        await ctx.send('Can\'t find the message', hidden=True)


if __name__ == "__main__":
    #OnlinePlayersUpdate.start()
    client.run(token)