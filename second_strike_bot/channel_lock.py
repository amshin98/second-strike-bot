from enum import Enum

# A helper file to keep track of what channels have a match setup being run. This is to prevent
# multiple match setups from being run in the same channel.


class UsageStatus(Enum):
    """Enum for representing usage status"""

    IN_USE = 1
    FREE = 2


# Dicitonary to map to channel.id to a UsageStatus enum
CHANNEL_ID_TO_USAGE_STATUS = {}


def is_channel_in_use(channel):
    """Checks if the given channel is in use"""
    if (
        channel.id in CHANNEL_ID_TO_USAGE_STATUS
        and CHANNEL_ID_TO_USAGE_STATUS[channel.id] == UsageStatus.IN_USE
    ):
        return True

    return False


def mark_channel_in_use(channel):
    """Marks the given channel as being in use"""
    CHANNEL_ID_TO_USAGE_STATUS[channel.id] = UsageStatus.IN_USE


def mark_channel_free(channel):
    """Marks the given channel as being free for use"""
    CHANNEL_ID_TO_USAGE_STATUS[channel.id] = UsageStatus.FREE
