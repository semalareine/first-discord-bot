import discord
import os
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1495881024201031793)
    if not channel:
        return

    background = Image.open("background.png").convert("RGBA")

    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).resize((150, 150))

    mask = Image.new("L", (150, 150), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 150, 150), fill=255)
    avatar.putalpha(mask)

    background.paste(avatar, (43, 75), avatar)

    draw = ImageDraw.Draw(background)
   
    font = ImageFont.truetype("Montserrat-Bold.ttf", 45)

    text = f"{member.name}"
    draw.text((220, 110), text, font=font, fill=(255, 255, 255))

    subtext_font = ImageFont.truetype("Montserrat-Regular.ttf", 30)
    draw.text((220, 170), "Welcome to Chizusoro!", font=subtext_font, fill=(200, 200, 200))

    file_path = f"welcome_{member.id}.png"
    background.save(file_path)

    file = discord.File(file_path)

    await channel.send(
        content=f"Welcome {member.mention} to Chizusoro!\nHave fun and prove yourself in tryouts!",
        file=file
    )

    os.remove(file_path)

bot.run(os.getenv("DISCORD_TOKEN"))
