from asyncio import TimeoutError


def is_reaction_emoji(reaction, emoji):
    return reaction.emoji == emoji
