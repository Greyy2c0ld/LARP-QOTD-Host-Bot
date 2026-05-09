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
START_DATE = datetime.now(NY_TIME).date()

questions = [
    "What department do you main in LARP?",
    "What is your favorite RP scene you've done?",
    "What update should LARP add next?",
    "Who is your favorite person to RP with?",
    "What makes a roleplay realistic?",
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

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    if not qotd_loop.is_running():
        qotd_loop.start()

@tasks.loop(minutes=1)
async def qotd_loop():
    global last_sent_date

    now = datetime.now(NY_TIME)
    current_date = now.date()

    if last_sent_date == current_date:
        return

    should_send = False

    # Today only: 6:00 PM EST/EDT
    if current_date == START_DATE and now.hour == 18 and now.minute == 0:
        should_send = True

    # After today: every day at 7:00 AM EST/EDT
    elif current_date > START_DATE and now.hour == 7 and now.minute == 0:
        should_send = True

    if should_send:
        channel = bot.get_channel(QOTD_CHANNEL_ID)

        if channel:
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
            last_sent_date = current_date

Thread(target=run_web).start()
bot.run(DISCORD_TOKEN)
