import discord
import requests
import asyncio
from discord.ext import tasks
from datetime import datetime

TOKEN = ""
CHANNEL_ID = 1477215150258917438

intents = discord.Intents.default()
client = discord.Client(intents=intents)

already_sent = set()

async def check_free_games():
    url = "https://store.steampowered.com/api/featuredcategories"
    response = requests.get(url).json()

    specials = response["specials"]["items"]

    for game in specials:
        if game["final_price"] == 0:
            if game["id"] not in already_sent:
                already_sent.add(game["id"])

                embed = discord.Embed(
                    title=game["name"],
                    description=f"🎮 **Most INGYENES!**\n⏳ Meddig: Ismeretlen",
                    color=0x00ff00
                )

                embed.set_image(url=game["header_image"])
                embed.add_field(name="Eredeti ár", value=f"{game['original_price']/100} {game['currency']}", inline=True)
                embed.add_field(name="Link", value=f"https://store.steampowered.com/app/{game['id']}", inline=False)

                channel = client.get_channel(CHANNEL_ID)
                await channel.send("@everyone 🚨 ÚJ INGYENES JÁTÉK!", embed=embed)

@tasks.loop(minutes=15)
async def loop_check():
    await check_free_games()

@client.event
async def on_ready():
    print(f"Bot elindult: {client.user}")
    loop_check.start()
import requests
import asyncio
from discord.ext import tasks
from datetime import datetime

TOKEN = ""
CHANNEL_ID = 1477215150258917438

intents = discord.Intents.default()
client = discord.Client(intents=intents)

already_sent = set()

async def check_free_games():
    url = "https://store.steampowered.com/api/featuredcategories"
    response = requests.get(url).json()

    specials = response["specials"]["items"]

    for game in specials:
        if game["final_price"] == 0:
            if game["id"] not in already_sent:
                already_sent.add(game["id"])

                embed = discord.Embed(
                    title=game["name"],
                    description=f"🎮 **Most INGYENES!**\n⏳ Meddig: Ismeretlen",
                    color=0x00ff00
                )

                embed.set_image(url=game["header_image"])
                embed.add_field(name="Eredeti ár", value=f"{game['original_price']/100} {game['currency']}", inline=True)
                embed.add_field(name="Link", value=f"https://store.steampowered.com/app/{game['id']}", inline=False)

                channel = client.get_channel(CHANNEL_ID)
                await channel.send("@everyone 🚨 ÚJ INGYENES JÁTÉK!", embed=embed)

@tasks.loop(minutes=15)
async def loop_check():
    await check_free_games()

@client.event
async def on_ready():
    print(f"Bot elindult: {client.user}")
    loop_check.start()

client.run(TOKEN)

client.run(TOKEN)
