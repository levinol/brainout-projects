from asyncio import events
import discord
from discord.embeds import Embed, EmptyEmbed
from discord.ext import commands
from discord.utils import get

import json
import requests
from threading import Timer
import datetime

from config import settings

client = commands.Bot(command_prefix=settings['prefix'])
token = settings['token']
submit_id = settings['submit_channel']
event_id= settings['event_channel']


subm_embed=discord.Embed(title="Improper usage of 'Submission'", description="Make submission. Note that you don't need to include the square brackets.", color=0x9b0389)
subm_embed.add_field(name="Usage:\n.submission [main/event] [message] [d=description] [optional attachment]", value="Make a submission.", inline=False)
subm_embed.add_field(name=".submission [clear/remove] [message id]", value="Clear all optional descriptions/Remove a submission.", inline=False)
subm_embed.add_field(name=".submission [add/addendum] [message id] [message] [optional attachment]", value="Add a addendum/attachment to a submission.", inline=False)
subm_embed.add_field(name="Aliases:", value="suggest, submit", inline=False)


@client.command() # Моя первая команда
async def hello(ctx): 
    author = ctx.message.author 

    await ctx.send(f'Hello, {author.mention}!') 

@client.remove_command('help')
@client.command()
async def help(ctx): 
    await ctx.send(embed=subm_embed)



@client.command()
async def submit(ctx, task_type, *, args):
    print(task_type, args)
    if task_type == 'main' or task_type == 'event':
        await submit_func(ctx, task_type, args)
    elif task_type == 'add' or task_type == 'addendum':
        await update_func(ctx, task_type, args)
    elif task_type == 'remove' or  task_type == 'clear':
        await remove_func(ctx, task_type, args)
    else:
        await ctx.send(embed=subm_embed)



async def submit_func(ctx, task_type, args): # submit команда создающая embed msg, добавляющая message_id и реакции сразу после создания.
    print(args)
    msg = args
    author = ctx.message.author
    
    cur_channel = client.get_channel(submit_id) if task_type == 'main' else client.get_channel(event_id)

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

    
    await ctx.send(f'{author.mention}, provide the file in png format wia .update')
    
    dispatched_embed = await cur_channel.send(embed=embed)

    embed.set_footer(text='Message ID: '+ str(dispatched_embed.id))
    await dispatched_embed.edit(embed=embed)
    await dispatched_embed.add_reaction("👍")
    await dispatched_embed.add_reaction("👎")        


@client.command()
async def update_func(ctx, task_type, args): # команда, добавляющая ссылку и текст на отправленный пнг файл
    submit_channel =client.get_channel(submit_id)
    args_splitted = args.split(' ', 1)
    msg_id = args_splitted[0]

    msg = await submit_channel.fetch_message(msg_id)

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
        try:
            embed.insert_field_at(index=999, name="Provided png", value=ctx.message.attachments[0].url, inline = False)
            
        except IndexError:
            await ctx.send(f'{ctx.message.author.mention}, what about image?')
            return 0

    await msg.edit(embed=embed)

@client.command()
async def remove_func(ctx, task_type, msg_id): #команда, удаляющая сообщение или очищающая поля
    submit_channel =client.get_channel(submit_id)
    msg = await submit_channel.fetch_message(msg_id)

    embed = msg.embeds[0]
    if task_type == 'clear':
        embed.clear_fields()
        await msg.edit(embed=embed)
    else:
        await msg.delete(delay=5)



#Embeded color thingi
@client.event
async def on_raw_reaction_add(payload): #Чекеры на реакцию, обновляющие цвет embed'a
    if payload.channel_id == settings['submit_channel']:
        submit_channel =client.get_channel(submit_id)
        msg = await submit_channel.fetch_message(payload.message_id)
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
    if payload.channel_id == settings['submit_channel']:
        submit_channel =client.get_channel(submit_id)
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

    if message.content == "test":
        await message.channel.send("test")

    if message.channel.id == settings['submit_channel']: # обрабатываем сообщения в канале sumbit_channel
        submit_channel = client.get_channel(submit_id)
        if message.reference is not None:
            await submit_channel.send("Thanks for the reply dude")


client.run(token)