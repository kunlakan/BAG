import discord
from discord.ext.command import Bot
from discord.ext import commands
import asyncio
import time

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content == "Hello":
        await
        client.send_message(message.channel, "World")


client.run("NDE5NTMxOTMxNTk2NzUwODU4.DXxkQA.y_ybewiQYtRpo_TPTSn5Qo5Txwk")
