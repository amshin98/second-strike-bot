import os
import discord
from dotenv import load_dotenv


def setup():
   load_dotenv()
   TOKEN = os.getenv("DISCORD_TOKEN")
   GUILD = os.getenv("DISCORD_GUILD")

   client = discord.Client()

   @client.event
   async def on_ready():
      for guild in client.guilds:
         if guild.name == GUILD:
            break
      print(f'{client.user} has connected to {guild.name}')

   client.run(TOKEN)


def main():
   setup()


if __name__ == "__main__":
   main()