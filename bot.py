import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1495881024201031793)
    if channel:
        await channel.send(f"Fakka {member.mention}!")

bot.run(os.getenv("DISCORD_TOKEN"))
