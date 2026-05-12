import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

load_dotenv()
discord_token = str(os.getenv("DISCORD_BOT_TOKEN"))
guild_id = os.getenv("Server_ID")
admin_roll = os.getenv("AdminRoll_ID")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('ログインしました')
    await tree.sync(guild=discord.Object(id=int(guild_id)))

@tree.command(
    name = "start_roll_calc",
    description = "ロール人数からの計算を始めます。"
)
@app_commands.checks.has_role(int(admin_roll))
async def rolecalc(
    interaction: discord.Interaction,
    kane: int,
    role: discord.Role
    ):
    current_channel_id = interaction.channel_id
    await interaction.response.send_message("実行確認。埋め込み出力します。", ephemeral=True)
    def umekomi(kane,role):
        count = len(role.members)
        one_money = kane / count
        zatsu_one_money = kane // count

        embed = discord.Embed(
            title = "割り勘計算",
            color = 0x586eb3
        )
        embed.add_field(name="現時点参加予定人数", value=f"{count}人", inline=False)
        embed.add_field(name="精密計算", value=f"{one_money}円/1人", inline=False)
        embed.add_field(name="整数計算", value=f"{zatsu_one_money}円/1人", inline=False)
    my_embed = umekomi(kane,role)
    await interaction.edit_original_response(content=None, embed=my_embed)
    message = await interaction.original_response()
    msg_id = message.id
    

def save_data(ch_id,ms_id):
    data = {
        "message_id": ms_id,
        "channel_id": ch_id
    }
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


client.run(discord_token)