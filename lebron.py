import os
import requests
import json
import random
from dotenv import load_dotenv
from discord import Intents, Client, Message
from typing import Final
import giphy_client
from giphy_client.rest import ApiException

load_dotenv()

#BOT SETUP 
intents: Intents = Intents.default()
intents.message_content = True #NOQA
client: Client = Client(intents=intents)


#MESSAGE FUNCTIONALITY 
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty because intents were not enabled properly')
        return

#Get quote 
def get_quote():
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        return(quote)   

#Get NBA gif  

sent_memes = [] # list of sent memes

def get_gif(message, *, q="lebron james nba funny memes"):
    
    api_key = os.getenv('GIPHY_TOKEN')
    api_instance = giphy_client.DefaultApi()

    try:
        offset = random.randint(0, 100)
        api_response = api_instance.gifs_search_get(api_key, q, limit = 25, offset=offset, rating='g')
        lst = list(api_response.data)

        # Select a meme that hasn't been sent yet
        giff = random.choice(lst)
        while giff.embed_url in sent_memes and len(sent_memes) < len(lst):
            giff = random.choice(lst)

        # If all memes have been sent, clear the list of sent memes
        if len(sent_memes) >= len(lst):
            sent_memes.clear()

        sent_memes.append(giff.embed_url)    
        return giff.embed_url
        
    except ApiException as e:
        print("Exception when calling API")
    

# SAYS IF BOT IS RUNNING
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# HANDLING THE MESSAGE FOR THE BOT
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

# if the message is !goat, the bot will respond with a gif and a quote
    if message.content.startswith('!goat'):
        meme = get_gif(message)
        quote = get_quote()
        await message.channel.send(meme)
        await message.channel.send(quote)
    else:
        await message.channel.send("I'm sorry, I don't understand that command. Please type !goat for a random LeBron gif and inspirational quote.")

#RUNNING THE BOT
def main() -> None:
    token = os.getenv('DISCORD_TOKEN')  # replace with your actual token
    client.run(token=token)


if __name__ == '__main__':
    main()
