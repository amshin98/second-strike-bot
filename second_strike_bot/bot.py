import os
import discord

from constants import *
from utils import *
from asyncio import TimeoutError, gather
from discord.ext import commands
from dotenv import load_dotenv
from random import randint, seed

seed(None)

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


async def get_reaction_num(react_options, captain_id,
   unavailable_maps_idx = []):

   try:
      reaction, user = await client.wait_for('reaction_add', timeout=60.0,
         check=lambda reaction, user:
         user.id == captain_id and
         reaction.emoji in react_options and
         react_options.index(reaction.emoji) not in unavailable_maps_idx)
   except TimeoutError:
      await channel.send('Timeout')
   else:
      return react_options.index(reaction.emoji)


async def handle_map_choice_response(map_pool, map_reacts, unavailable_maps_idx,
   captain_id, channel):

   send_string = ""
   for i in range(len(map_pool)):
      cur_string = "%s %s" % (map_reacts[i], map_pool[i])
      if i in unavailable_maps_idx:
         cur_string = "~~%s~~" % cur_string
      cur_string = "> %s\n" % cur_string
      send_string += cur_string

   msg = await channel.send(send_string)
   for react in map_reacts:
      await msg.add_reaction(react)

   return await get_reaction_num(map_reacts, captain_id, unavailable_maps_idx)


async def get_map_choice(map_pool, map_reacts, unavailable_maps_idx,
   captain_id, channel, is_ban):
   
   await channel.send("<@!%s>, choose a map to **%s**:" %
      (captain_id, "ban" if is_ban else "play") )

   return await handle_map_choice_response(map_pool, map_reacts,
      unavailable_maps_idx, captain_id, channel)


async def handle_side_choice_response(captain_id, channel):
   send_string = ""
   for i in range(len(SIDES)):
      send_string += "> %s %s\n" % (SIDE_REACTS[i], SIDES[i])

   msg = await channel.send(send_string)
   for react in SIDE_REACTS:
      await msg.add_reaction(react)

   return await get_reaction_num(SIDE_REACTS, captain_id)


async def get_side_choice(captain_id, match_map, channel):
   await channel.send("<@!%s>, choose your starting side for **%s**:" %
      (captain_id, match_map))

   return await handle_side_choice_response(captain_id, channel)


async def send_phase_banner(channel, is_ban):
   await channel.send("**%s %s %s**" % 
      (BANNER_DECO, BAN_PHASE_TEXT if is_ban else PICK_PHASE_TEXT, BANNER_DECO))


async def send_map_choices(channel, maps, is_ban):
   await channel.send("%s maps: **%s** and **%s**" %
      ("Banned" if is_ban else "Chosen", maps[0], maps[1]))


async def send_games(channel, captain_ids, maps, attacker_ids, defender_ids):
   send_string = ""
   for i in range(len(maps)):
      send_string += "Game %d: **%s** - %s <@!%s> vs. %s <@!%s>\n" % (i + 1,
         maps[i], DAGGER, attacker_ids[i], SHIELD, defender_ids[i])

   await channel.send(send_string)


# Remember, team 2 chooses side first
def get_sides_lists(side_choices, captain_ids, team_1, team_2,
   attacker_ids, defender_ids):

   on_team_2 = True
   for side in side_choices:
      # Attack
      if side == 0:
         attacker_ids.append(captain_ids[team_2] if on_team_2
            else captain_ids[team_1])
         defender_ids.append(captain_ids[team_1] if on_team_2
            else captain_ids[team_2])
      else: # Defense
         defender_ids.append(captain_ids[team_2] if on_team_2
            else captain_ids[team_1])
         attacker_ids.append(captain_ids[team_1] if on_team_2
            else captain_ids[team_2])

      on_team_2 = not on_team_2


async def handle_match_setup(message):
   cur_channel = message.channel

   # Get captains mentions and decide Team A
   msg = await cur_channel.send("Captains, please react to this message with %s"
      % THUMBSUP)
   await msg.add_reaction(THUMBSUP)

   captains = []
   await get_reaction_user(captains, THUMBSUP)
   await get_reaction_user(captains, THUMBSUP)

   team_1 = randint(0, 1)
   team_2 = 0 if team_1 == 1 else 1

   # Ban phase
   await send_phase_banner(cur_channel, True)
   map_ban_1 = await get_map_choice(MAP_POOL, MAP_REACTS, [],
      captains[team_1], cur_channel, True)
   map_ban_2 = await get_map_choice(MAP_POOL, MAP_REACTS, [map_ban_1],
      captains[team_2], cur_channel, True)
   await send_map_choices(cur_channel,
      [MAP_POOL[map_ban_1], MAP_POOL[map_ban_2]], True)

   available_maps = []
   available_map_reacts = []
   for i in range(len(MAP_POOL)):
      if i != map_ban_1 and i != map_ban_2:
         available_maps.append(MAP_POOL[i])
         available_map_reacts.append(MAP_REACTS[i])

   # Pick and side phase
   await send_phase_banner(cur_channel, False)
   map_pick_1 = await get_map_choice(available_maps, available_map_reacts,
      [], captains[team_1], cur_channel, False)
   side_pick_2 = await get_side_choice(captains[team_2],
      available_maps[map_pick_1], cur_channel)
   map_pick_2 = await get_map_choice(available_maps, available_map_reacts,
      [map_pick_1], captains[team_2], cur_channel, False)
   side_pick_1 = await get_side_choice(captains[team_1],
      available_maps[map_pick_2], cur_channel)

   chosen_maps = [available_maps[map_pick_1], available_maps[map_pick_2]]
   attacker_ids = []
   defender_ids = []
   get_sides_lists([side_pick_2, side_pick_1], captains, team_1, team_2,
      attacker_ids, defender_ids)
   await send_games(cur_channel, captains, chosen_maps, attacker_ids,
      defender_ids)
   

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