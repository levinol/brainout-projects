from asyncio import events
import discord
from discord import activity
from discord import role
from discord.embeds import Embed, EmptyEmbed
from discord.ext import commands
from discord.flags import PublicUserFlags
from discord.utils import get

import json
import requests
from threading import Timer
import datetime

from config import *

client = commands.Bot(command_prefix=settings['prefix'], activity=discord.Activity(type=discord.ActivityType.watching, name='Use '+settings['prefix']+'help if u dumb'))
token = settings['token']
submit_id = settings['submit_channel']
suggest_id = settings['suggest_channel']
event_id = settings['event_channel']
server_id = settings['suggest_server_channel']
embed_channels = [settings['submit_channel'], settings['submit_final_channel'], settings['suggest_channel'], settings['suggest_server_channel'], settings['event_channel']]
subm_embed = Embed.from_dict(submission_embed)
simp_embed = Embed.from_dict(simplified_embed)
sugst_embed = Embed.from_dict(suggestion_embed)
sugst_simp_embed = Embed.from_dict(suggestion_simp_embed)
help_emb = Embed.from_dict(help_embed)

@client.command() # Моя первая команда
async def hello(ctx): 
    author = ctx.message.author 
    print(author, type(author))

    await ctx.send(f'Hello, {author.mention}!') 

@client.remove_command('help')
@client.command()
async def help(ctx, type_help='s'): 
    if ctx.channel.id == settings['submit_desc_channel']:
        if type_help == 'r':
            await ctx.send(embed=subm_embed)
        elif type_help == 's':
            await ctx.send(embed=simp_embed)
    elif  ctx.channel.id == settings['suggest_desc_channel']:
        if type_help == 'r':
            await ctx.send(embed=sugst_embed)
        elif type_help == 's':
            await ctx.send(embed=sugst_simp_embed)
    else:
        await ctx.send(embed=help_emb)




@client.command()
async def submission(ctx, task_type, *, args):
    print(task_type, args)
    if ctx.channel.id == settings['submit_desc_channel']:
        if task_type == 'main' or task_type == 'event':
            await submit(ctx, args=args, task_type=task_type, subm_check=1)
        elif task_type == 'add' or task_type == 'addendum':
            await add(ctx, args=args, task_type=task_type, subm_check=1)
        elif task_type == 'remove' or  task_type == 'clear':
            await remove(ctx, args=args, task_type=task_type, subm_check=1)
        else:
            await ctx.send(embed=subm_embed)
    else:
        await ctx.send(embed=subm_embed)

@client.command()
async def suggestion(ctx, task_type, *, args):
    print(task_type, args)
    if ctx.channel.id == settings['suggest_desc_channel']:
        if task_type == 'main' or task_type == 'server':
            await submit(ctx, args=args, task_type=task_type, subm_check=0)
        elif task_type == 'add' or task_type == 'addendum':
            await add(ctx, args=args, task_type=task_type, subm_check=0)
        elif task_type == 'remove' or  task_type == 'clear':
            await remove(ctx, args=args, task_type=task_type, subm_check=0)
        else:
            await ctx.send(embed=sugst_embed)
    else:
        await ctx.send(embed=sugst_embed)


@client.command()
async def submit(ctx, *, args, task_type='main', subm_check=1): # submit команда создающая embed msg, добавляющая message_id и реакции сразу после создания.
    print(args)
    msg = args
    author = ctx.message.author
    
    if ctx.channel.id == settings['submit_desc_channel']:
        delivery_channel = client.get_channel(submit_id) if task_type == 'main' else client.get_channel(event_id)
    else:
        delivery_channel = client.get_channel(suggest_id) if task_type == 'main' else client.get_channel(server_id)

    #Разделяем на title и desc
    if msg.find('d=')!=-1:
        msg_title = msg[:msg.find('d=')]
        msg_desc = msg[msg.find('d=')+2:]
    else:
        msg_title = msg
        msg_desc = discord.Embed.Empty 

    embed=discord.Embed(title=msg_title, description=msg_desc, color=0xFFFFFF, timestamp=datetime.datetime.utcnow())
    embed.set_author(name=author.display_name, icon_url=author.avatar_url)
    try:
        embed.set_image(url=ctx.message.attachments[0].url)
        
    except IndexError:
        await ctx.send(f'{author.mention}, what about image?')
        return 0 

    
    await ctx.send(f'{author.mention}, provide the files in necessary format wia .add [message id] [message] [mandatory attachment]')
    
    dispatched_embed = await delivery_channel.send(embed=embed)

    embed.set_footer(text='Message ID: '+ str(dispatched_embed.id))
    await dispatched_embed.edit(embed=embed)
    await dispatched_embed.add_reaction("👍")
    await dispatched_embed.add_reaction("👎")        

async def submit_short(message, channel_type): # submit_short команда создающая embed msg, добавляющая message_id и реакции сразу после создания.
    msg = message.content
    author = message.author
    print(msg)
    cur_channel = message.channel
    delivery_channel = client.get_channel(submit_id) if channel_type == 'submit' else client.get_channel(suggest_id)

    #Разделяем на title и desc
    if msg.find('d=')!=-1:
        msg_title = msg[msg.find('>') + 1:msg.find('d=')]
        msg_desc = msg[msg.find('d=')+2:]
    else:
        msg_title = msg[msg.find('>') + 1:]
        msg_desc = discord.Embed.Empty 

    embed=discord.Embed(title=msg_title, description=msg_desc, color=0xFFFFFF, timestamp=datetime.datetime.utcnow())
    embed.set_author(name=author.display_name, icon_url=author.avatar_url)
    try:
        embed.set_image(url=message.attachments[0].url)
        
    except IndexError:
        if channel_type == 'submit':
            await cur_channel.send(f'{author.mention}, what about image?')
            return 0 

    
    await cur_channel.send(f'{author.mention}, provide the files in necessary format wia .add')
    
    dispatched_embed = await delivery_channel.send(embed=embed)

    embed.set_footer(text='Message ID: '+ str(dispatched_embed.id))
    await dispatched_embed.edit(embed=embed)
    await dispatched_embed.add_reaction("👍")
    await dispatched_embed.add_reaction("👎")  

@client.command()
async def add(ctx, *, args, task_type='add', subm_check=1): # команда, добавляющая ссылку и текст на отправленный пнг файл
    args_splitted = args.split(' ', 1)
    msg_id = args_splitted[0]

    if subm_check:
        submit_channel = client.get_channel(submit_id)
        submit_channel2 = client.get_channel(event_id)
    else:
        submit_channel = client.get_channel(suggest_id) 
        submit_channel2 = client.get_channel(server_id)

    subm_flag = 0

    try:
        msg = await submit_channel.fetch_message(msg_id)
    except discord.errors.NotFound:
        subm_flag = 1
    
    if subm_flag:
        try:
            msg = await submit_channel2.fetch_message(msg_id)
        except discord.errors.NotFound:
            subm_flag = 2
            ctx.send(f'{ctx.message.author.mention}, cant find your msg by id. Fix your brain or smth idk')

    if True or ctx.message.author == msg.author:
        #gettin msg
        embed = msg.embeds[0]
        if len(args_splitted) > 1:
            if len(args_splitted[1])>1 and not args_splitted[1].isspace(): # чекер на одно дополнение к сообщению
                embed_dict = embed.to_dict()
                temp_flag = 0
                if 'fields' in embed_dict:
                    for field in embed_dict['fields']:
                        if field['name'] == "Addendum":
                            temp_flag = 1
                            field['value'] = args_splitted[1]

                if temp_flag:
                    embed = Embed.from_dict(embed_dict)
                else:
                    embed.add_field(name="Addendum", value=args_splitted[1], inline = False)

        if task_type == 'add':
            # FIXME 
            try:
                embed.insert_field_at(index=999, name="Provided png", value=ctx.message.attachments[0].url, inline = False)
                
            except IndexError:
                await ctx.send(f'{ctx.message.author.mention}, what about image?')
                return 0

        await msg.edit(embed=embed)
    else:
        await ctx.send(f'{ctx.message.author.mention}, that\'s not your message 😡')


async def add_сomment(comment, mode): # команда, добавляющая комментарий в ембед 
    submit_channel = client.get_channel(comment.channel.id)
    msg = await submit_channel.fetch_message(comment.reference.message_id)
    embed = msg.embeds[0]
    comment_time = comment.created_at.strftime("%A, %d %b %Y %H:%M") + ' UTC'
    embed.add_field(name=f"❗{mode} comment - {comment_time}❗", value=comment.content, inline = False)
    await msg.edit(embed=embed)

@client.command()
async def remove(ctx, args, task_type='remove', subm_check=1): #команда, удаляющая сообщение или очищающая поля

    if subm_check:
        submit_channel = client.get_channel(submit_id)
        submit_channel2 = client.get_channel(event_id)
    else:
        submit_channel = client.get_channel(suggest_id) 
        submit_channel2 = client.get_channel(server_id)

    subm_flag = 0

    try:
        msg = await submit_channel.fetch_message(args)
    except discord.errors.NotFound:
        subm_flag = 1
    
    if subm_flag:
        try:
            msg = await submit_channel2.fetch_message(args)
        except discord.errors.NotFound:
            subm_flag = 2
            ctx.send(f'{ctx.message.author.mention}, cant find your msg by id. Fix your brain or smth idk')

    print(ctx.message.author.id, msg.author.id)

    if True or ctx.message.author == msg.author:
        embed = msg.embeds[0]
        if task_type == 'clear':
            embed.clear_fields()
            await msg.edit(embed=embed)
        else:
            await msg.delete(delay=5)
    else:
        await ctx.send(f'{ctx.message.author.mention}, that\'s not your message 😡')



#Embeded color thingi
@client.event
async def on_raw_reaction_add(payload): #Чекеры на реакцию, обновляющие цвет embed'a
    if payload.channel_id in embed_channels:
        react_channel =client.get_channel(payload.channel_id)
        msg = await react_channel.fetch_message(payload.message_id)
        react1 = get(msg.reactions, emoji="👍")
        react2 = get(msg.reactions, emoji="👎")
        embed = msg.embeds[0]

        react1 = react1.count
        react2 = react2.count


        if react1 > 50 and react2 < 20:
            embed.colour = 0x3CB371
        elif react2 >20:
            embed.colour = 0xFF0000
        elif react1 > react2:
            embed.colour = 0x228B22
        elif react1 == react2:
            embed.colour = 0xFFFFFF 
        else:
            embed.colour = 0xFF8C00

        await msg.edit(embed=embed)

@client.event
async def on_raw_reaction_remove(payload):#Чекер на реакцию, обновляющие цвет embed'a. Вообще говнокод, но я не люблю писать декораторы 
    if payload.channel_id in embed_channels:
        submit_channel =client.get_channel(payload.channel_id)
        msg = await submit_channel.fetch_message(payload.message_id)
        react1 = get(msg.reactions, emoji="👍")
        react2 = get(msg.reactions, emoji="👎")
        embed = msg.embeds[0]

        react1 = react1.count
        react2 = react2.count


        if react1 > 50 and react2 < 20:
            embed.colour =  0x3CB371
        elif react2 >20:
            embed.colour = 0xFF0000
        elif react1 > react2:
            embed.colour = 0x228B22
        elif react1 == react2:
            embed.colour = 0xFFFFFF 
        else:
            embed.colour = 0xFF8C00

        await msg.edit(embed=embed)

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
                

    elif len(message.mentions) > 0: 
        if message.raw_mentions[0] == 848518443926028288: #Проверяем является ли сообщение упоминанием бота
            #проверка на сообщение в канале
            if message.channel.id == settings['submit_desc_channel']:
                await submit_short(message, 'submit')
            elif  message.channel.id == settings['suggest_desc_channel']:
                await submit_short(message, 'suggest')
            else:
                await message.channel.send('aww you mention me')
            pass
            #await message.channel.send("test")

    


client.run(token)