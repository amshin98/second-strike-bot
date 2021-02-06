import os
from dotenv import load_dotenv


CMD_PFX = "!"
THUMBSUP = "👍"

ASCENT = "🗑️"
BIND = "🍊"
HAVEN = "🏯"
ICEBOX = "☃️"
SPLIT = "🌓"

MAP_REACTS = [ASCENT, BIND, HAVEN, ICEBOX, SPLIT]
MAP_POOL = ["Ascent", "Bind", "Haven", "Icebox", "Split"]

DAGGER = "🗡️"
SHIELD = "🛡️"
SIDE_REACTS = [DAGGER, SHIELD]
SIDES = ["Attack", "Defense"]

BANNER_DECO = "================="
BAN_PHASE_TEXT = "BAN PHASE"
PICK_PHASE_TEXT = "PICK PHASE"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")