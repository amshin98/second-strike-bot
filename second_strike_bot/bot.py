import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

CMD_PFX = "!"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = discord.Client()


async def handle_test_command(message):
   channel = message.channel
   await channel.send('Send me that 👍 reaction, mate')

   def check(reaction, user):
      return user == message.author and str(reaction.emoji) == '👍'

   try:
      reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
   except asyncio.TimeoutError:
      await channel.send('👎')
   else:
      await channel.send('👍')


def main():
   @client.event
   async def on_message(message):
      if message.content.startswith('%sthumb' % CMD_PFX):
         await handle_test_command(message)

   client.run(TOKEN)


if __name__ == "__main__":
   main()