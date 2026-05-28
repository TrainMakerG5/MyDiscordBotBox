import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

count = 0
load_dotenv()
discord_token = str(os.getenv("DISCORD_BOT_TOKEN"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def spkAll(d):
    ans : str
    if d == 1:
        spk = list("ﾃﾞﾙｼﾞﾊﾞｾﾞﾖ")
    else:
        spk = ["ﾃﾞ","ﾙ","ｼﾞ","ﾊﾞ","ｾﾞ","ﾖ"]

    ans = "ｳｱｱ!ｽﾋﾟｷ"
    for _ in range(len(spk)):
        rn = random.randint(0,len(spk)-1)
        ans = ans + spk[rn]
    ans = ans + "!"
    return ans

def spkSin(d):
    ans : str
    if d == 1:
        spk = list("ﾃﾞﾙｼﾞﾊﾞｾﾞﾖ")
    else:
        spk = ["ﾃﾞ","ﾙ","ｼﾞ","ﾊﾞ","ｾﾞ","ﾖ"]

    ans = "ｳｱｱ!ｽﾋﾟｷ"
    for _ in range(len(spk)):
        rn = random.randint(0,len(spk)-1)
        ans = ans + spk.pop(rn)
    ans = ans + "!"
    return ans

@tree.command(
    name = "spk",
    description= "ｽﾋﾟｷ構文を発します。mode：1→重複あり,2→重複なし dakuten：1→区別,2→連結"
)
async def spk(
    interaction: discord.Interaction,
    mode: int,
    dakuten: int
):
    print(f"spk running mode:{mode} daku:{dakuten}")
    if mode == 1:
        speak = spkAll(dakuten)
    else:
        speak = spkSin(dakuten)
    await interaction.response.send_message(speak)

@client.event
async def on_ready():
    print('spk activate now!')
    await tree.sync()
    count = 0

client.run(discord_token)