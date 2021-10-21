from asyncio import events
import re
import discord
from discord import activity
from discord import role
from discord.channel import VoiceChannel
from discord.embeds import Embed, EmptyEmbed
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

from config import *

client = commands.Bot(command_prefix='/', activity=discord.Activity(type=discord.ActivityType.watching, name='Use '+settings['prefix']+'help if u dumb'))
slash = SlashCommand(client, sync_commands=True)


token = settings['token']
submit_id = settings['submit_channel']
submit_final_id = settings['submit_final_channel']
suggest_id = settings['suggest_channel']
event_id = settings['event_channel']
server_id = settings['suggest_server_channel']
online_id = settings['online_channel']
embed_channels = [settings['submit_channel'], settings['submit_final_channel'], settings['suggest_channel'], settings['suggest_server_channel'], settings['event_channel']]
subm_embed = Embed.from_dict(submission_embed)
sugst_embed = Embed.from_dict(suggestion_embed)

help_emb = Embed.from_dict(help_embed)


import psycopg2

# Connect to postgres DB
conn = psycopg2.connect(dbname="brainout", user="admin", password="password", host="postgres")

def author_id_check(msg_id: str, author_id: str, channel_type: str) -> bool:
    is_author_flag = False
    with conn.cursor() as cursor:
        conn.autocommit = True
        print(channel_type)
        if channel_type == 'submission':
            cursor.execute("SELECT author_id FROM brainout.submissions WHERE msg_id = %s", (msg_id,))
        elif channel_type == 'suggestion':
            cursor.execute("SELECT author_id FROM brainout.suggestions WHERE msg_id = %s", (msg_id,))
        result = cursor.fetchone()
        if author_id in result:
            is_author_flag = True
    return is_author_flag

@client.remove_command('help')
@client.command()
async def help(ctx, task_typo=None):
    if task_typo == "suggestion":
        await ctx.send(embed=sugst_embed)
    elif task_typo == "submission":
        await ctx.send(embed=subm_embed)
    else:
        await ctx.send(embed=help_emb)
    await delete_with_react(ctx.message)

import requests
from discord.ext import tasks

@tasks.loop(minutes=10)
async def OnlinePlayersUpdate():
    VoiceChannel = await client.fetch_channel(online_id)

    print(VoiceChannel)
    r=requests.get(update_url)
    print(r)
    await VoiceChannel.edit(name=f"Online: {r.json()['players']}")

async def add_сomment(comment, mode): # команда, добавляющая комментарий в ембед 
    submit_channel = client.get_channel(comment.channel.id)
    msg = await submit_channel.fetch_message(comment.reference.message_id)
    embed = msg.embeds[0]
    comment_time = comment.created_at.strftime("%A, %d %b %Y %H:%M") + ' UTC'
    embed.add_field(name=f"❗{mode} comment - {comment_time}❗", value=comment.content, inline = False)
    await msg.edit(embed=embed)


async def delete_with_react(msg):
    await msg.add_reaction("🚮")
    await msg.delete(delay=7)

#Embeded color thingi

async def reaction_count(payload):
    if payload.channel_id in embed_channels:
        submit_channel =client.get_channel(payload.channel_id)
        msg = await submit_channel.fetch_message(payload.message_id)
        react1 = get(msg.reactions, emoji="👍")
        react2 = get(msg.reactions, emoji="👎")
        embed = msg.embeds[0]

        react1 = react1.count
        react2 = react2.count

        if react1 > 2 and react2 < 2:
            #Move to final if paylod == submission channel id
            embed.colour = 0x3CB371

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

                    dispatched_embed = await delivery_channel.send(embed=embed)

                    embed.set_footer(text='Message ID: '+ str(dispatched_embed.id))

                    await dispatched_embed.edit(embed=embed)
                    await dispatched_embed.add_reaction("👍")
                    await dispatched_embed.add_reaction("👎")   
        elif react2 > 2:
            # delete 
            embed.colour = 0xFF0000
            await delete_with_react(msg)
        elif react1 > react2:
            embed.colour = 0x228B22
        elif react1 == react2:
            embed.colour = 0xFFFFFF 
        else:
            embed.colour = 0xFF8C00

        await msg.edit(embed=embed)

@client.event
async def on_raw_reaction_add(payload): #Чекеры на реакцию, обновляющие цвет embed'a
    await reaction_count(payload)

@client.event
async def on_raw_reaction_remove(payload):#Чекер на реакцию, обновляющие цвет embed'a. Вообще говнокод, но я не люблю писать декораторы 
    await reaction_count(payload)

@client.event
async def on_message(message):
    await client.process_commands(message)

    if message.reference is not None: #Проверяем является ли сообщение реплаем 
        if message.channel.id in [settings['submit_channel'], settings['submit_final_channel'], settings['suggest_channel'], settings['suggest_server_channel']]: # обрабатываем сообщения в канале sumbit_channel
            submit_channel = client.get_channel(message.channel.id)
            
            #role cheeeeeck
            roles_ids = []
            for r in message.author.roles:
                roles_ids.append(r.id)

            # Govnokod // pls review it later
            # FIXME
            if roles['dev'] in roles_ids:
                await add_сomment(message,'👨‍💻Dev')
            elif roles['designers'] in roles_ids:
                await add_сomment(message,'👨‍🎨Designer')
            elif roles['admin'] in roles_ids:
                await add_сomment(message,'🛌Admin')
            elif roles['moderator'] in roles_ids:
                await add_сomment(message,'👨‍⚖️Mod')
            elif roles['helper'] in roles_ids:
                await add_сomment(message,'🦸‍♂️Helper')
            else:
                await submit_channel.send("Yo, where is your roles")
            
            # удаляем реплаи!
            await message.delete()



# NEW ERA of SLASH COMMANDS
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow

select = create_select(
    options=[# the options in your dropdown
         create_select_option("'Submission' commands", value="submission", emoji="🙈"),
        create_select_option("'Suggestion' commands", value="suggestion", emoji="🙉"),
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
async def _hello(ctx): 
    await ctx.send(embed=help_emb, components=[create_actionrow(select)])  

@client.event
async def on_component(ctx):
    # ctx.selected_options is a list of all the values the user selected
    if ctx.selected_options[0] == "suggestion":
        await ctx.send(embed=sugst_embed, hidden=True)
    elif ctx.selected_options[0] == "submission":
        await ctx.send(embed=subm_embed, hidden=True)
    else:
        await ctx.send('uhhh im stuck')


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

    # ищем мессаге
    msg =  await msg_fetch(ctx, message_id, channel_flag)

    if msg == 0:
        return 0

    print(str(message_id),str(ctx.message.author.id), channel_flag )

    is_author_flag = author_id_check(str(message_id),str(ctx.message.author.id), channel_flag )

    if is_author_flag:
        #gettin msg
        embed = msg.embeds[0]
        if message: # Проверка на существование поля с комментарием и обновление/добавление его
            embed_dict = embed.to_dict()
            temp_flag = 0
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    if field['name'] == "Addendum":
                        temp_flag = 1
                        field['value'] = message

            if temp_flag:
                embed = Embed.from_dict(embed_dict)
            else:
                embed.add_field(name="Addendum", value=message, inline = False)

        # FIXME 
        try:
            embed.insert_field_at(index=999, name="Provided file", value=ctx.message.attachments[0].url, inline = False)
            
            
        except:
            bot_respond = await ctx.send(f'{ctx.message.author.mention}, what about image?')
            await delete_with_react(bot_respond)
            return 0

        await msg.edit(embed=embed)

    else:
        await ctx.send(f'{ctx.message.author.mention}, that\'s not your message 😡')
        # Удаляем изначальную команду
        await delete_with_react(ctx.message)   


async def add_text_to_embed(ctx, message, message_id, channel_flag):
    # ищем мессаге
    msg =  await msg_fetch_slash(ctx, message_id, channel_flag)

    if msg == 0:
        return 0

    is_author_flag = author_id_check(str(message_id),str(ctx.author.id), channel_flag )

    if is_author_flag:
        #gettin msg
        embed = msg.embeds[0]
        if message: # Проверка на существование поля с комментарием и обновление/добавление его
            embed_dict = embed.to_dict()
            temp_flag = 0
            if 'fields' in embed_dict:
                for field in embed_dict['fields']:
                    if field['name'] == "Addendum":
                        temp_flag = 1
                        field['value'] = message

            if temp_flag:
                embed = Embed.from_dict(embed_dict)
                
            else:
                embed.add_field(name="Addendum", value=message, inline = False)

        # FIXME 
        try:
            embed.insert_field_at(index=999, name="Provided file", value=ctx.message.attachments[0].url, inline = False)
            await ctx.send('File was provided' ,hidden=True)
            
        except:
            # TODO check if slash commands now can work with file attachments
            pass

        await msg.edit(embed=embed)
        await ctx.send('Addendum was replaced', hidden=True) if temp_flag else await ctx.send('Addendum was added', hidden=True)
    else:
        await ctx.send(f'{ctx.author.mention}, that\'s not your message 😡')
  

async def msg_fetch(ctx, message_id, channel_flag):
    # ищем мессаге
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

async def msg_fetch_slash(ctx, message_id, channel_flag):
    # ищем мессаге
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
    await dispatched_embed.add_reaction("👍")
    await dispatched_embed.add_reaction("👎")
    return str(dispatched_embed.id)

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
                #role cheeeeeck
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

@slash.slash(
    name="hello",
    description="Say hello to botti",
    guild_ids=[873835757238894592]
)
async def _hello(ctx:SlashContext): 
    await ctx.send(f'Hello, {ctx.author.mention}!', hidden=True)

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
    author = ctx.author
    
    #Разделяем на title и desc
    if description:
        msg_title = artwork_name
        msg_desc = description
    else:
        msg_title = artwork_name
        msg_desc = discord.Embed.Empty 

    msg_id = await create_embed_with_reactions(ctx, msg_title, msg_desc, submit_id, image_req=True)
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(f"INSERT INTO brainout.submissions(author_id, msg_id, in_final) VALUES ({author.id}, {msg_id}, {False})")

    await ctx.send(f'{author.mention}, provide the files in necessary format wia add command', hidden=True)  

# _submission_main command with attached image
# _submission_add command with attached image
@client.command()
async def submission(ctx, *, args): # submit команда создающая embed msg, добавляющая message_id и реакции сразу после создания.
    command_type, args=args.split(' ',1)
    print(command_type, args)
    msg = args
    author = ctx.message.author
    if command_type == 'main':
        msg_id = await send_embed_with_file(ctx, args, submit_id, "artwork_name:", "description:", image_req=True)
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f"INSERT INTO brainout.submissions(author_id, msg_id, in_final) VALUES ({author.id}, {msg_id}, {False})")
    elif command_type == 'add':
        await add_file_to_embed(ctx, args, "message_id:", "message:", channel_flag="submission")    
    else:
        await ctx.send('uhh im stuck')

""" @slash.subcommand(
    base="submission",
    name="event",
    description="Make a submission in event channel", 
    guild_ids=[873835757238894592],
    options=[
        create_option(
            name="artwork_name",
            description="Pls name it Hell",
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
    
    author = ctx.author
    
    #Разделяем на title и desc
    if description:
        msg_title = artwork_name
        msg_desc = description
    else:
        msg_title = artwork_name
        msg_desc = discord.Embed.Empty 

    await create_embed_with_reactions(ctx, msg_title, msg_desc, submit_id, image_req=True)

    await ctx.send(f'{author.mention}, provide the files in necessary format wia add command', hidden=True)   """

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
            description="Message for addendum field",
            option_type=3,
            required=False
        )
    ]
    )
async def _submission_add(ctx, message_id, message=None):
    await add_text_to_embed(ctx, message, message_id, channel_flag="submission")

@slash.subcommand(
    base="submission",
    name="addendum",
    description="Add an addendum to a submission", 
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
            description="Message for addendum field",
            option_type=3,
            required=True
        )
    ]
    )
async def _submission_addendum(ctx, message_id, message):
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
    await clear_embed(ctx, message_id, "submission")

import sys

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
    
    author = ctx.author
    
    #Разделяем на title и desc
    if description:
        msg_title = suggestion_topic
        msg_desc = description
    else:
        msg_title = suggestion_topic
        msg_desc = discord.Embed.Empty 
    
    msg_id = await create_embed_with_reactions(ctx, msg_title, msg_desc, suggest_id , image_req=False)
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(f"INSERT INTO brainout.suggestions(author_id, msg_id) VALUES ({author.id}, {msg_id})")
    await ctx.send(f'{author.mention}, provide the files in necessary format wia add command', hidden=True)

# _suggestion_main command with attached image
@client.command()
async def suggestion(ctx, *, args): # suggest команда создающая embed msg, добавляющая message_id и реакции сразу после создания.
    command_type, args=args.split(' ',1)
    print(command_type, args)
    msg = args
    author = ctx.message.author
    if command_type == 'main':
        msg_id = await send_embed_with_file(ctx, args, suggest_id, "suggestion_topic:", "description:", image_req=False)
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f"INSERT INTO brainout.suggestions(author_id, msg_id) VALUES ({author.id}, {msg_id})")
    elif command_type == 'server':
        msg_id = await send_embed_with_file(ctx, args, server_id,"artwork_name:",  "description:", image_req=False)
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f"INSERT INTO brainout.suggestions(author_id, msg_id) VALUES ({author.id}, {msg_id})")

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
    author = ctx.author
    
    #Разделяем на title и desc
    if description:
        msg_title = suggestion_topic
        msg_desc = description
    else:
        msg_title = suggestion_topic
        msg_desc = discord.Embed.Empty 

    msg_id = await create_embed_with_reactions(ctx, msg_title, msg_desc, server_id , image_req=False)
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(f"INSERT INTO brainout.suggestions(author_id, msg_id) VALUES ({author.id}, {msg_id})")
    await ctx.send(f'{author.mention}, provide the files in necessary format wia add command', hidden=True)


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
            description="Message for addendum field",
            option_type=3,
            required=False
        )
    ]
    )
async def _suggestion_add(ctx, message_id, message):
    await add_text_to_embed(ctx, message, message_id, channel_flag="suggestion")

@slash.subcommand(
    base="suggestion",
    name="addendum",
    description="Add an addendum to a suggestion", 
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
            description="Message for addendum field",
            option_type=3,
            required=True
        )
    ]
    )
async def _suggestion_addendum(ctx, message_id, message):
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

    msg =  await msg_fetch_slash(ctx, message_id, "suggestion")
    if msg == 0:
        return 0

    is_author_flag = author_id_check(str(message_id),str(ctx.author.id), 'suggestion' )

    if is_author_flag:
        await msg.delete(delay=5)
        await ctx.send('Message deleted', hidden=True)
    else:
        await ctx.send(f'{ctx.author.mention}, that\'s not your message 😡')

OnlinePlayersUpdate.start()
client.run(token)