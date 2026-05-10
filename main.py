import discord
from discord.ext import commands, tasks
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask
from threading import Thread
import os
import random

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.getenv("PORT", 10000))

QOTD_CHANNEL_ID = 1397263932300853368
ROLE_ID = 1397265374042656768

NY_TIME = ZoneInfo("America/New_York")

questions = [
    "What is one thing you enjoy most about roleplaying?",
    "What is your favorite memory you've made in LARP so far?",
    "What type of roleplay scenarios do you enjoy the most?",
    "What keeps you active within the community?",
    "What is one feature you would love to see added in the future?",
    "What is your favorite thing to do while in-game?",
    "What inspired you to join LARP?",
    "What makes a roleplay server enjoyable for you?",
    "What is your favorite vehicle in ER:LC?",
    "What department do you enjoy using the most?",
    "What is one goal you have while roleplaying?",
    "What is your favorite update added to ER:LC?",
    "What kind of events would you like to see more often?",
    "What is your favorite part about the community?",
    "What is one thing that improves realism in roleplay?",
]

app = Flask(__name__)

@app.route("/")
def home():
    return "LARP QOTD Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_sent_date = None
sent_startup_qotd = False

async def send_qotd():
    global last_sent_date

    channel = bot.get_channel(QOTD_CHANNEL_ID)

    if channel:
        now = datetime.now(NY_TIME)
        question = random.choice(questions)
        unix_timestamp = int(now.timestamp())

        message = f"""# <:questionmark:1474258261812318251> LARP QOTD 🧭🌌

Hello <@&{ROLE_ID}>! Today is <t:{unix_timestamp}:D>, which means it’s time for today’s QOTD!

🌌⏱️ QOTD: {question}

📝💬 Drop your answer in the thread below!
👇✨
-# Powered by LARP Auto-QOTD Bot
"""

        await channel.send(message)
        last_sent_date = now.date()

@bot.event
async def on_ready():
    global sent_startup_qotd

    print(f"Logged in as {bot.user}")

    if not sent_startup_qotd:
        await send_qotd()
        sent_startup_qotd = True

    if not qotd_loop.is_running():
        qotd_loop.start()

@tasks.loop(minutes=1)
async def qotd_loop():
    global last_sent_date

    now = datetime.now(NY_TIME)
    current_date = now.date()

    if last_sent_date == current_date:
        return

    if now.hour == 7 and now.minute == 0:
        await send_qotd()

Thread(target=run_web).start()
bot.run(DISCORD_TOKEN)
