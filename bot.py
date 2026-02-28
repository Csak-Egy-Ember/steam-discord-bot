import discord
import requests
import sqlite3
from discord.ext import tasks
from datetime import datetime

TOKEN = "IDE_A_BOT_TOKEN"
CHANNEL_ID = 123456789012345678

intents = discord.Intents.default()
client = discord.Client(intents=intents)

db = sqlite3.connect("sent_games.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sent (id INTEGER)")
db.commit()

def get_discount_expiration(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=hu&l=hu"
    response = requests.get(url).json()

    try:
        price_info = response[str(app_id)]["data"]["price_overview"]
        expiration_timestamp = price_info.get("discount_expiration")

        if expiration_timestamp:
            dt = datetime.fromtimestamp(expiration_timestamp)
            return dt.strftime("%Y-%m-%d %H:%M")
        else:
            return "Ismeretlen"
    except:
        return "Ismeretlen"

@tasks.loop(minutes=15)
async def check_free_games():
    print("Ellenőrzés...")
    url = "https://store.steampowered.com/api/featuredcategories"
    data = requests.get(url).json()

    for game in data["specials"]["items"]:
        if game["discount_percent"] == 100 and game["original_price"] > 0:

            cursor.execute("SELECT id FROM sent WHERE id=?", (game["id"],))
            if cursor.fetchone() is None:

                expiration = get_discount_expiration(game["id"])

                embed = discord.Embed(
                    title=game["name"],
                    description="🔥 Ideiglenesen INGYENES a Steamen!",
                    color=0x1b2838
                )

                embed.add_field(
                    name="Eredeti ár",
                    value=f"{game['original_price'] / 100} Ft",
                    inline=True
                )

                embed.add_field(
                    name="Ingyenes eddig",
                    value=expiration,
                    inline=True
                )

                embed.add_field(
                    name="Link",
                    value=f"https://store.steampowered.com/app/{game['id']}",
                    inline=False
                )

                embed.set_image(
                    url=f"https://cdn.akamai.steamstatic.com/steam/apps/{game['id']}/header.jpg"
                )

                channel = client.get_channel(CHANNEL_ID)

                # 🔔 @everyone ping
                await channel.send("@everyone", embed=embed)

                cursor.execute("INSERT INTO sent VALUES (?)", (game["id"],))
                db.commit()

@client.event
async def on_ready():
    print(f"Bejelentkezve mint {client.user}")
    check_free_games.start()

client.run(TOKEN)