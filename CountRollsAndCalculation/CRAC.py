import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

load_dotenv()
discord_token = str(os.getenv("DISCORD_BOT_TOKEN"))
guild_id = discord.Object(id=int(os.getenv("Server_ID")))
admin_role = os.getenv("AdminRole_ID")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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

@tree.command(
    name = "start_role_calc",
    description = "ロール人数からの計算を始めます。",
    guilds=[guild_id]
)
@app_commands.checks.has_role(int(admin_role))
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
        return embed
    my_embed = umekomi(kane,role)
    await interaction.followup.send(embed=my_embed, ephemeral=False)
    message = await interaction.original_response()
    msg_id = message.id
    save_data(current_channel_id,msg_id)

@tree.command(
    name = "update_rc_embed",
    description = "送信した埋め込みを更新します。",
    guilds = [guild_id]
)
@app_commands.checks.has_role(int(admin_role))
async def updaterolecalc(
    interaction: discord.Integration,
    kane: int,
    role: discord.Role
):
    await interaction.response.send_message("実行確認。埋め込みを更新します。", ephemeral=True)
    try:
        data = load_data()
        msg_id = data["message_id"]
        ch_id = client.get_channel(int(data["channel_id"]))
        target_message = await ch_id.fetch_message(int(msg_id))
        new_embed = umekomi(kane,role)
        await target_message.edit(embed=new_embed)
    except Exception as e:
        print(f"Error! {e}\nターゲットMSG:")

@client.event
async def on_ready():
    print('ログインしました')
    await tree.sync(guild=guild_id)

client.run(discord_token)