# setting.py

import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CATEGORY_ID = os.environ.get("MAKE_CHANNEL_CATEGORY_ID")
BOT_SEED = os.environ.get("BOT_SEED")