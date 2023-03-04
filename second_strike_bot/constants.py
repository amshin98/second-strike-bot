import os
from dotenv import load_dotenv


CMD_PFX = "/"
THUMBSUP = "👍"

ASCENT = "🎲"
BIND = "🏭"
BREEZE = "🏝️"
FRACTURE = "⚡"
HAVEN = "🏯"
ICEBOX = "☃️"
LOTUS = "🌷"
PEARL = "🦪"
SPLIT = "🌓"

MAP_REACTS = [ASCENT, BIND, BREEZE, FRACTURE, HAVEN, ICEBOX, LOTUS, PEARL, SPLIT]
MAP_POOL = [
    "Ascent",
    "Bind",
    "Breeze",
    "Fracture",
    "Haven",
    "Icebox",
    "Lotus",
    "Pearl",
    "Split",
]

DAGGER = "🗡️"
SHIELD = "🛡️"
SIDE_REACTS = [DAGGER, SHIELD]
SIDES = ["Attack", "Defense"]

BANNER_DECO = "================="
BAN_PHASE_TEXT = "BAN PHASE"
PICK_PHASE_TEXT = "PICK PHASE"

HELP_TEXT = "%ssetup\tStarts setup for a best of 3 game" % CMD_PFX

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
