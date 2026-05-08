import discord
from discord.ext import commands, tasks
from datetime import datetime
import os
import random

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

QOTD_CHANNEL_ID = 1397263932300853368

questions = [
    "What department do you main in LARP?",
    "What is your favorite RP scene you've done?",
    "What update should LARP add next?",
    "Who is your favorite person to RP with?",
    "What makes a roleplay realistic?",
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_sent_date = None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    if not qotd_loop.is_running():
        qotd_loop.start()

@tasks.loop(minutes=1)
async def qotd_loop():
    global last_sent_date

    now = datetime.now()

    current_date = now.date()

    # Prevent duplicate sends
    if last_sent_date == current_date:
        return

    hour = now.hour
    minute = now.minute

    should_send = False

    # TODAY ONLY → 6 PM EST
    if current_date.day == 8:
        if hour == 18 and minute == 0:
            should_send = True

    # EVERY DAY AFTER TODAY → 7 AM EST
    else:
        if hour == 7 and minute == 0:
            should_send = True

    if should_send:
        channel = bot.get_channel(QOTD_CHANNEL_ID)

        if channel:
            question = random.choice(questions)

            unix_timestamp = int(discord.utils.utcnow().timestamp())

            message = f"""# <:questionmark:1474258261812318251> LARP QOTD 🧭🌌

Hello <@&1397265374042656768>! Today is <t:{unix_timestamp}:D>, which means it’s time for today’s QOTD!

🌌⏱️ QOTD: {question}

📝💬 Drop your answer in the thread below!
👇✨
-# Powered by LARP Auto-QOTD Bot
"""

            await channel.send(message)

            last_sent_date = current_date

bot.run(DISCORD_TOKEN)
