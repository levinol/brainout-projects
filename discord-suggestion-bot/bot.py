import discord
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

@client.command() # Моя первая команда
async def hello(ctx): 
    author = ctx.message.author 

    await ctx.send(f'Hello, {author.mention}!') 


@client.command()
async def submit(ctx): # submit команда создающая embed msg, добавляющая message_id и реакции сразу после создания.
    msg = ctx.message.content
    author = ctx.message.author
    submit_channel =client.get_channel(submit_id)

    #Разделяем на title и desc
    if msg.find('d=')!=-1:
        msg_title = msg[len('submit')+1:msg.find('d=')]
        msg_desc = msg[msg.find('d=')+2:]
    else:
        msg_title = msg[len('submit')+1:]
        msg_desc = discord.Embed.Empty 

    embed=discord.Embed(title=msg_title, description=msg_desc, color=0xFFFFFF, timestamp=datetime.datetime.utcnow())
    embed.set_author(name=author.display_name, icon_url=author.avatar_url)
    try:
        embed.set_image(url=ctx.message.attachments[0].url)
        
    except IndexError:
        await ctx.send(f'{author.mention}, what about image?')
        return 0 

    
    await ctx.send(f'{author.mention}, provide the file in png format wia .update')
    
    dispatched_embed = await submit_channel.send(embed=embed)

    embed.set_footer(text='Message ID: '+ str(dispatched_embed.id))
    await dispatched_embed.edit(embed=embed)
    await dispatched_embed.add_reaction("👍")
    await dispatched_embed.add_reaction("👎")        


@client.command()
async def update(ctx, msg_id): # update команда, добавляющая ссылку на отправленный пнг файл
    submit_channel =client.get_channel(submit_id)
    msg = await submit_channel.fetch_message(msg_id)

    #gettin msg
    embed = msg.embeds[0]
    try:
        embed.add_field(name="Provided png", value=ctx.message.attachments[0].url)
        
    except IndexError:
        await ctx.send(f'{ctx.message.author.mention}, what about image?')
        return 0

    await msg.edit(embed=embed)


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

client.run(token)
