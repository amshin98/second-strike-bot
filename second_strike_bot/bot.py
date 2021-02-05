import os
import discord

from io import *
from utils import *
from asyncio import TimeoutError, gather
from discord.ext import commands
from dotenv import load_dotenv
from random import randint, seed

seed(None)

CMD_PFX = "!"
THUMBSUP = "👍"

ONE = "1️⃣"
TWO = "2️⃣"
THREE = "3️⃣"
FOUR = "4️⃣"
FIVE = "5️⃣"

MAP_REACTS = [ONE, TWO, THREE, FOUR, FIVE]
MAP_POOL = ["Ascent", "Bind", "Haven", "Icebox", "Split"]

MAP_SELECT_PROMPT = "Please select a map from the following:"


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


async def get_reaction_num(captain_id):
   try:
      reaction, user = await client.wait_for('reaction_add', timeout=60.0,
         check=lambda reaction, user:
         user.id == captain_id and
         reaction.emoji in MAP_REACTS)
   except TimeoutError:
      await channel.send('Timeout')
   else:
      return MAP_REACTS.index(reaction.emoji)


async def handle_map_choice_response(captain_id, channel):
   send_string = "%s\n" % MAP_SELECT_PROMPT
   for i in range(len(MAP_POOL)):
      send_string += "> %s %s\n" % (MAP_REACTS[i], MAP_POOL[i])

   msg = await channel.send(send_string)
   for react in MAP_REACTS:
      await msg.add_reaction(react)

   return await get_reaction_num(captain_id)


async def get_map_choice(captain_id, channel, is_ban):
   await channel.send("<@!%s>'s team will choose the first map to **%s**. " %
      (captain_id, "ban" if is_ban else "play") +
      "Please choose from the following:")

   return await handle_map_choice_response(captain_id, channel)


async def handle_match_setup(message):
   cur_channel = message.channel

   # Get captains mentions and decide Team A
   msg = await cur_channel.send("Captains, please react to this message with %s"
      % THUMBSUP)
   await msg.add_reaction(THUMBSUP)


   captains = []
   await get_reaction_user(captains, THUMBSUP)
   await get_reaction_user(captains, THUMBSUP)

   team_a = randint(0, 1)
   team_b = 0 if team_a == 1 else 1

   map_ban_1 = await get_map_choice(captains[team_a], cur_channel, True)
   map_ban_2 = await get_map_choice(captains[team_b], cur_channel, True)


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