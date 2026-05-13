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

topics = [
    "food", "music", "movies", "travel", "school", "gaming", "cars",
    "childhood", "social media", "money", "dreams", "friendships",
    "weekends", "holidays", "summer", "pets", "sports", "shopping",
    "technology", "favorite memories", "funny moments", "life goals"
]

question_templates = [
    "What is your favorite thing about {topic}?",
    "What is one unpopular opinion you have about {topic}?",
    "If you could change one thing about {topic}, what would it be?",
    "What is your funniest memory involving {topic}?",
    "What is something about {topic} that people always debate?",
    "What is one thing you wish more people understood about {topic}?",
    "Would you rather give up {topic} forever or use it every day?",
    "What is your most memorable experience with {topic}?",
    "What is something related to {topic} that instantly makes you happy?",
    "What is one hot take you have about {topic}?",
    "If you had unlimited money for {topic}, what would you do first?",
    "What is something about {topic} that you think is overrated?",
    "What is something about {topic} that you think is underrated?",
    "What is your go-to choice when it comes to {topic}?",
    "What is one thing about {topic} that always makes people argue?"
]

opinion_templates = [
    "My opinion: This is a good question because everyone’s answer can be completely different.",
    "My opinion: Questions like this usually bring out funny, honest, and unexpected answers.",
    "My opinion: There’s really no wrong answer here, which makes it more fun to answer.",
    "My opinion: I feel like this kind of question helps people learn more about each other.",
    "My opinion: This is one of those topics where people always have strong opinions.",
    "My opinion: Sometimes the simplest questions create the best conversations.",
    "My opinion: I think answers to this can say a lot about someone’s personality.",
    "My opinion: This could definitely start a funny debate in the thread.",
    "My opinion: I like questions like this because they keep the conversation casual and active.",
    "My opinion: The best answers are usually the most honest ones."
]

used_questions = set()

def generate_qotd():
    global used_questions

    topic = random.choice(topics)
    template = random.choice(question_templates)
    question = template.format(topic=topic)

    if len(used_questions) >= 100:
        used_questions.clear()

    while question in used_questions:
        topic = random.choice(topics)
        template = random.choice(question_templates)
        question = template.format(topic=topic)

    used_questions.add(question)

    opinion = random.choice(opinion_templates)

    return question, opinion

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

async def send_qotd():
    global last_sent_date

    channel = bot.get_channel(QOTD_CHANNEL_ID)

    if channel:
        now = datetime.now(NY_TIME)

        question, opinion = generate_qotd()

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

    if now.hour == 7 and now.minute == 0:
        await send_qotd()

Thread(target=run_web).start()
bot.run(DISCORD_TOKEN)
