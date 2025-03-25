import sys # sys for define external moduels
import os # for env
import json # for parse response data 
import requests 
import random

import discord # discord moduel important for dealing with discord API's & BOT 

# dotenv moduel for loading hidden keys in envirement 
from dotenv import dotenv_values
keys = dotenv_values(".env") # load keys from env file
import asyncio

# set key's
discord_key = keys["discord_key"]
tenor_key   = keys["tenor_key"]
nasa_key    = keys["nasa_key"]
nasa_url    = keys["nasa_url"]
trans_key   = keys["trans_key"]

# for define project folders to the envirement
def define_path(folder_path = ""):
    sys.path.append(folder_path)

### define ###
define_path("./gifs/")
define_path("./reactions/")
define_path("./nasa/")
define_path("./jokes/")
### import after define ###
from gif_api import get_gif
from reaction import get_reaction
import nasa
import joke
from jokeapi import Jokes

# discord controller
client = discord.Client()

# function who handle sending gif's
# this function using moduel => "gif/gif_api.py" 
async def send_gif(message,msg):
    
    try: 
        # function get_gif will try to get gif for you 
        if len(message) >= 1 :

            gif_path = await get_gif(tenor_key , message[1]) # get gif
            await msg.channel.send( gif_path ) #send it

        else : 
            # argument message[1] is missing" 
            await msg.channel.send( "[!gif] command error 'missing second argument' :sad:" )
    
    #  if error happend we will send it as messages
    except Exception as err:
        await msg.channel.send("[!gif]  command error missing second argument")
        await msg.channel.send("```[ERROR] " + str(err)+"```")


# when bot ready for work
@client.event
async def on_ready():
    print("bot {0.user} is online now".format(client))

# when someone send message
@client.event
async def on_message(msg):

    # get user name only without #....
    username = str(msg.author).split("#")[0]
    # get user message
    message  = str(msg.content).split(" ")
    # get channel when user send this message
    channel  = str(msg.channel.name)

    # just print message in console as & "log"
    print(f"[{channel}] {username} : {message}")

    # if response comming from this bot it's self don't response "just skip"
    if( msg.author == client.user):
        return

    ### __chat__💬 channel ###

    # response to specific channel
    # if msg.channel.name == "__chat__💬":
        #
        # *** here where answers of messages & commands ***
        #

    # example : send a joke using jokes API
    if message[0].lower() == "!joke":
        j = await Jokes() # Initialise the class
        joke = await j.get_joke() # Retrieve a random joke
        if joke["type"] == "single": 
            # send joke
            await msg.channel.send(joke["joke"])
        else:
            await msg.channel.send(joke["setup"])
            await msg.channel.send(joke["delivery"])


    # help message 
    if message[0].lower() == "!help":
        await msg.channel.send("""
            !help           : display commands
            !help command   : display help & examples for specific commands
            !nasa           : display photo of the day from nasa + article
            !gif target     : display random gif about topic
            !random         : display random number between range
            !joke           : display random joke
            !react          : let bot react last message
            hello sara      : let bot say hello for you
        """)

    ### general channel ###

    # send gif's using gif api 'tenor'
    # if msg.channel.name == "general":

    if message[0].lower() == "!gif":
        # send_gif function it's the handler for this task
        await send_gif(message , msg)

    ### for all channels ###

    # get random number between min & max
    if message[0].lower() == "!random":
        try: 
            # convert min & max to int's
            min = int(message[1]) or 0 
            max = int(message[2]) or 0
            await msg.channel.send( random.randint(min , max) )

        except Exception as err:
            await msg.channel.send(f"error : {err}")


    # example if user sayed hello
    if msg.content == "hello" or msg.content == "hi" or  msg.content == "salam" or msg.content == "slm": 
        # sara say hello + his name
        await msg.channel.send(f"OH ! Hi There , {username}")
        return

    #send random reaction sometimes
    if(random.randint(1,100) % 2 == 0): 
        await msg.add_reaction(get_reaction("empty"))

    # example : using nasa API to get Photo Of the Day
    if message[0].lower() == "!nasa":
        try:
            await msg.channel.send("Nasa : Photo of The Day")
            await msg.channel.send(nasa.get_photo(nasa_url,nasa_key))
            await msg.channel.send(nasa.get_description(nasa_url,nasa_key))

        except Exception as err :
            await msg.channel.send(err)


# run bot
client.run(discord_key)
