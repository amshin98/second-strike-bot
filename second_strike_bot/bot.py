import discord
import channel_lock

from constants import *
from utils import *
from asyncio import TimeoutError, gather
from discord.ext import commands
from dotenv import load_dotenv
from random import randint, seed

seed(None)

client = discord.Client()


async def get_reaction_user(reacted_ids, emoji, cur_channel):
    """Validates a user reaction to a message before returning their user ID"""

    def check_user_reaction_valid(reaction, user):
        is_reaction_in_cur_channel = reaction.message.channel == cur_channel
        is_not_bot_reaction = user.id != client.user.id
        has_user_not_already_reacted = user.id not in reacted_ids
        is_correct_reaction_emoji = is_reaction_emoji(reaction, emoji)

        return (
            is_reaction_in_cur_channel
            and is_not_bot_reaction
            and has_user_not_already_reacted
            and is_correct_reaction_emoji
        )

    try:
        reaction, user = await client.wait_for(
            "reaction_add", timeout=60.0, check=check_user_reaction_valid
        )
    except TimeoutError:
        await cur_channel.send("Timeout")
        raise TimeoutError
    else:
        reacted_ids.append(user.id)
        return user.id


async def get_reaction_num(
    react_options, captain_id, cur_channel, unavailable_maps_idx=[]
):
    """Validates a user reaction to a message before returning the index of the map they selected"""

    def check_reaction_num_valid(reaction, user):
        is_reaction_in_cur_channel = reaction.message.channel == cur_channel
        is_user_current_captain = user.id == captain_id
        is_valid_reaction_emoji = reaction.emoji in react_options
        is_choice_available = (
            react_options.index(reaction.emoji) not in unavailable_maps_idx
        )

        return (
            is_reaction_in_cur_channel
            and is_user_current_captain
            and is_valid_reaction_emoji
            and is_choice_available
        )

    try:
        reaction, user = await client.wait_for(
            "reaction_add", timeout=60.0, check=check_reaction_num_valid
        )
    except TimeoutError:
        await cur_channel.send("Timeout")
        raise TimeoutError
    else:
        return react_options.index(reaction.emoji)


async def handle_map_choice_response(
    map_pool, map_reacts, unavailable_maps_idx, captain_id, channel
):
    """Prints the maps and waits for the user to pick one"""

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

    return await get_reaction_num(map_reacts, captain_id, channel, unavailable_maps_idx)


async def get_map_choice(
    map_pool, map_reacts, unavailable_maps_idx, captain_id, channel, is_ban
):
    """Sends a map choice prompt then handles a map emoji choice response"""

    await channel.send(
        "<@!%s>, choose a map to **%s**:" % (captain_id, "ban" if is_ban else "play")
    )

    return await handle_map_choice_response(
        map_pool, map_reacts, unavailable_maps_idx, captain_id, channel
    )


async def handle_side_choice_response(captain_id, channel):
    """Sends the actual side choices prompt then handles a side emoji choice response"""
    send_string = ""
    for i in range(len(SIDES)):
        send_string += "> %s %s\n" % (SIDE_REACTS[i], SIDES[i])

    msg = await channel.send(send_string)
    for react in SIDE_REACTS:
        await msg.add_reaction(react)

    return await get_reaction_num(SIDE_REACTS, captain_id, channel)


async def get_side_choice(captain_id, match_map, channel):
    """Sends a prompt for a captain to select their side for a map and then handles the response"""
    await channel.send(
        "<@!%s>, choose your starting side for **%s**:" % (captain_id, match_map)
    )

    return await handle_side_choice_response(captain_id, channel)


async def send_phase_banner(channel, is_ban):
    """Handles sending the phase (ban, pick, etc.) notification banner"""
    await channel.send(
        "**%s %s %s**"
        % (BANNER_DECO, BAN_PHASE_TEXT if is_ban else PICK_PHASE_TEXT, BANNER_DECO)
    )


async def send_map_choices(channel, maps, is_ban):
    """Sends an acknowledgement to a map choice (ban or pick)"""
    await channel.send(
        "%s maps: **%s** and **%s**"
        % ("Banned" if is_ban else "Chosen", maps[0], maps[1])
    )


async def send_games(channel, captain_ids, maps, attacker_ids, defender_ids):
    """Sends a list of the games (map and which team is on which side) after picks and bans are done"""
    send_string = ""
    for i in range(len(maps)):
        send_string += "Game %d: **%s** - %s <@!%s> vs. %s <@!%s>\n" % (
            i + 1,
            maps[i],
            DAGGER,
            attacker_ids[i],
            SHIELD,
            defender_ids[i],
        )

    await channel.send(send_string)


def get_sides_lists(
    side_choices, captain_ids, team_1, team_2, attacker_ids, defender_ids
):
    """Handles adding the captain ids to the attacker_ids and defender_ids lists. Index 0 in each list
    corresponds to the first game, index 1 the second game, etc. Used for displaying the final list of games.
    Remember that Team 2 chooses the side first"""

    on_team_2 = True
    for side in side_choices:
        # Attack
        if side == 0:
            attacker_ids.append(
                captain_ids[team_2] if on_team_2 else captain_ids[team_1]
            )
            defender_ids.append(
                captain_ids[team_1] if on_team_2 else captain_ids[team_2]
            )
        else:  # Defense
            defender_ids.append(
                captain_ids[team_2] if on_team_2 else captain_ids[team_1]
            )
            attacker_ids.append(
                captain_ids[team_1] if on_team_2 else captain_ids[team_2]
            )

        on_team_2 = not on_team_2


async def handle_match_setup(message):
    """The main match setup function"""
    cur_channel = message.channel

    # Get captains mentions and decide Team A
    msg = await cur_channel.send(
        "Captains, please react to this message with %s" % THUMBSUP
    )
    await msg.add_reaction(THUMBSUP)

    captains = []
    await get_reaction_user(captains, THUMBSUP, cur_channel)
    await get_reaction_user(captains, THUMBSUP, cur_channel)

    team_1 = randint(0, 1)
    team_2 = 0 if team_1 == 1 else 1

    # Ban phase
    await send_phase_banner(cur_channel, True)
    map_ban_1 = await get_map_choice(
        MAP_POOL, MAP_REACTS, [], captains[team_1], cur_channel, True
    )
    map_ban_2 = await get_map_choice(
        MAP_POOL, MAP_REACTS, [map_ban_1], captains[team_2], cur_channel, True
    )
    await send_map_choices(
        cur_channel, [MAP_POOL[map_ban_1], MAP_POOL[map_ban_2]], True
    )

    available_maps = []
    available_map_reacts = []
    for i in range(len(MAP_POOL)):
        if i != map_ban_1 and i != map_ban_2:
            available_maps.append(MAP_POOL[i])
            available_map_reacts.append(MAP_REACTS[i])

    # Pick and side phase
    await send_phase_banner(cur_channel, False)
    map_pick_1 = await get_map_choice(
        available_maps, available_map_reacts, [], captains[team_1], cur_channel, False
    )
    side_pick_2 = await get_side_choice(
        captains[team_2], available_maps[map_pick_1], cur_channel
    )
    map_pick_2 = await get_map_choice(
        available_maps,
        available_map_reacts,
        [map_pick_1],
        captains[team_2],
        cur_channel,
        False,
    )
    side_pick_1 = await get_side_choice(
        captains[team_1], available_maps[map_pick_2], cur_channel
    )

    chosen_maps = [available_maps[map_pick_1], available_maps[map_pick_2]]
    attacker_ids = []
    defender_ids = []
    get_sides_lists(
        [side_pick_2, side_pick_1], captains, team_1, team_2, attacker_ids, defender_ids
    )
    await send_games(cur_channel, captains, chosen_maps, attacker_ids, defender_ids)


async def handle_help_message(message):
    """Sends the help message"""
    await message.channel.send(HELP_TEXT)


def main():
    @client.event
    async def on_message(message):
        if len(message.content) > 1 and message.content.startswith(CMD_PFX):
            command = message.content[1:]

            if command == "setup" and not channel_lock.is_channel_in_use(
                message.channel
            ):
                # Mark the channel as free if any exception occurs during match setup
                try:
                    cur_channel = message.channel

                    channel_lock.mark_channel_in_use(cur_channel)
                    await handle_match_setup(message)
                    channel_lock.mark_channel_free(cur_channel)
                except Exception as exception:
                    channel_lock.mark_channel_free(cur_channel)
                    raise exception

            elif command == "help":
                await handle_help_message(message)

    client.run(TOKEN)


if __name__ == "__main__":
    main()
