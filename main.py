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

qotds = [
    {
        "question": "If you could instantly master any skill, what would it be?",
        "opinion": "My opinion: Being able to instantly master a skill would probably completely change someone’s future."
    },
    {
        "question": "What’s a food you could eat every single day?",
        "opinion": "My opinion: Comfort foods usually say a lot about someone because they connect to memories and routines."
    },
    {
        "question": "If money didn’t matter, where would you travel first?",
        "opinion": "My opinion: Most people probably already have a dream destination they think about all the time."
    },
    {
        "question": "What’s your biggest pet peeve?",
        "opinion": "My opinion: Pet peeves are funny because something tiny can completely annoy one person but not affect another."
    },
    {
        "question": "What’s one song you never skip?",
        "opinion": "My opinion: Everyone has at least one song that instantly changes their mood."
    },
    {
        "question": "What’s your dream car?",
        "opinion": "My opinion: Dream cars usually reflect personality more than people realize."
    },
    {
        "question": "What’s your most unpopular opinion?",
        "opinion": "My opinion: Unpopular opinions are entertaining as long as people keep things respectful."
    },
    {
        "question": "What’s the weirdest food combination you actually enjoy?",
        "opinion": "My opinion: Weird food combinations always sound disgusting until someone actually tries them."
    },
    {
        "question": "Would you rather have unlimited money or unlimited free time?",
        "opinion": "My opinion: Free time might actually be more valuable because you can never truly buy more time."
    },
    {
        "question": "What’s your favorite fast food spot?",
        "opinion": "My opinion: Fast food debates somehow become more serious than real arguments."
    }
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
        selected_qotd = random.choice(qotds)

        question = selected_qotd["question"]
        opinion = selected_qotd["opinion"]

        unix_timestamp = int(now.timestamp())

        message = f"""# ❔ LARP QOTD 🧭🌌

Hello <@&{ROLE_ID}>! Today is <t:{unix_timestamp}:D>, which means it’s time for today’s QOTD!

🌌⏱️ QOTD: {question}

📝💬 Drop your answer in the thread below!
👇✨
-# Powered by LARP Auto-QOTD Bot
"""

        sent_message = await channel.send(message)

        thread = await sent_message.create_thread(
            name="QOTD Discussion"
        )

        await thread.send(f"🤖 {opinion}")

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
