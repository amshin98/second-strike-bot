import os
from dotenv import load_dotenv


CMD_PFX = "!"
THUMBSUP = "👍"

ONE = "1️⃣"
TWO = "2️⃣"
THREE = "3️⃣"
FOUR = "4️⃣"
FIVE = "5️⃣"

MAP_REACTS = [ONE, TWO, THREE, FOUR, FIVE]
MAP_POOL = ["Ascent", "Bind", "Haven", "Icebox", "Split"]

BANNER_DECO = "================="
BAN_PHASE_TEXT = "BAN PHASE"
PICK_PHASE_TEXT = "PICK PHASE"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")