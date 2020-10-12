# bot.py
import os

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

baseURL = "https://9157b335f219.ngrok.io/"

client = discord.Client()
bot = commands.Bot(command_prefix='!')


@bot.command(name='register', help='Start user registration')
async def on_message(ctx):
    user = ctx.message.author
    channel = await user.create_dm()
    roles = []
    for i in user.roles:
        roles.append(i.name)

    check = requests.post(baseURL + '/validatebot/', json={"userID": "368755063104995339"})

    if(check.json()['status'] == True):
        response = f'We have met before! I have sent you your key on the DM again ;)'
        await ctx.send(response)
        userHash = check.json()['userHash']
        resp2 = f'Your key is: {userHash}. Please enter it in the CLI'
        await channel.send(resp2)
    else:
        response = (
            f'Starting user registration for {user}. Please check your DM to receive your user key'
        )
        await ctx.send(response)
        r = requests.post(
            url=baseURL + '/register/',
            json={"userId": str(user.id), "userName": str(user), "roles": roles},
        )
        res = r.json()
        userHash = res['userHash']
        resp2 = f'Your key is: {userHash}. Please enter it in the CLI'
        await channel.send(resp2)


bot.run(TOKEN)
