import os
import discord
from dotenv import load_dotenv


def setup():
   load_dotenv()
   TOKEN = os.getenv('DISCORD_TOKEN')

   client = discord.Client()

   @client.event
   async def on_ready():
      print(f'{client.user} has connected to Discord')

   client.run(TOKEN)

def main():
   setup()

if __name__ == "__main__":
   main()