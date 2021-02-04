import os
import discord

from utils import *
from asyncio import TimeoutError, gather
from discord.ext import commands
from dotenv import load_dotenv
from random import randint


CMD_PFX = "!"
THUMBSUP = "👍"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = discord.Client()


async def get_reaction_user(reacted_ids, emoji):
   try:
      _, user = await client.wait_for('reaction_add', timeout=60.0,
         check=lambda reaction, user:
         user.id != client.user.id and
         user.id not in reacted_ids and
         is_reaction_emoji(reaction, emoji))
   except TimeoutError:
      await channel.send('Timeout')
   else:
      reacted_ids.append(user.id)
      return user.id


async def handle_match_setup(message):
   channel = message.channel

   # Get captains mentions and decide Team A
   msg = await channel.send("Captains, please react to this message with %s"
      % THUMBSUP)
   await msg.add_reaction(THUMBSUP)

   captains = []
   await get_reaction_user(captains, THUMBSUP)
   await get_reaction_user(captains, THUMBSUP)

   team_a = randint(0, 1)

   await channel.send("<@!%s>'s team will choose the first map"
      % captains[team_a])


def main():
   @client.event
   async def on_message(message):
      if len(message.content) > 1 and message.content.startswith(CMD_PFX):
         command = message.content[1:]

         if command == "setup":
            await handle_match_setup(message)

   client.run(TOKEN)


if __name__ == "__main__":
   main()