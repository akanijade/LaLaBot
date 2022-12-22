import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

from discord.ext import commands
from discord import app_commands
import youtube_dl
import asyncio

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
    "heartbroken", "upset", " bad ", "worried", "sorry", "dissapointed",
    "shoot my head", "cut my life into pieces", "kill me", "suicide", 
    "my dick is small", "i want to die", "suicidal"
]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
 
    msg = message.content

    if msg == '/test':
        await message.channel.send('ping pong!')
        
    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg.lower() for word in sad_words):
            await message.channel.send(random.choice(options))

        if msg.startswith("/new"):
            encouraging_message = msg.split("/new ", 1)[1]
            update_encouragements(encouraging_message)
            await message.channel.send("New encouraging message added.")

        if msg.startswith("/del"):
            encouragements = []
            if "encouragements" in db.keys():
                index = int(msg.split("!del", 1)[1])
                delete_encouragement(index)
                encouragements = db["encouragements"]
            await message.channel.send(encouragements)

    if msg.startswith("/list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("/responding"):
        value = msg.split("!responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")
    

@tree.command()
async def slash(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.send_message(f'{number=} {string=}', ephemeral=True)
  


@tree.command(name = "quote", description = "Generate a random quote")
async def quote(interaction: discord.Interaction):
    quote = get_quote()
    await interaction.response.send_message(quote, ephemeral=False)


@tree.command(name = "dm", description = "Send a personal message to a user")
async def dm(interaction: discord.Interaction, member: discord.Member, *, message: str):
    await member.send(message)
    await interaction.response.send_message(":white_check_mark: Sent!")


@tree.command(name = "help", description = "Help Box")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help Box",
                          description="Command lines that might work")
    embed.set_thumbnail(url="https://i.imgur.com/9wkETOh.jpeg")
    embed.set_image(
        url=
        "https://i.pinimg.com/originals/73/76/34/73763429c9f1adcdf7512338edecdad1.jpg"
    )
    embed.add_field(name="/quote",
                    value="gives you a random quote",
                    inline=False)
    embed.add_field(name="if you say sad, depressed things",
                    value="Bot will try to cheer you up",
                    inline=False)
    embed.add_field(name="/new [quote]",
                    value="Add inspiring quotes",
                    inline=False)
    embed.add_field(name="/del [index]",
                    value="Delete inspiring quotes",
                    inline=False)
    embed.add_field(name="/list ",
                    value="see all added inspiring quotes",
                    inline=False)
    embed.add_field(name="/dm @user <message>",
                   value="Personally message a user",
                   inline=False)
    embed.set_footer(
        text=
        "Hope it works, you can add new inspiring quotes by using /new [quote]"
    )
    await interaction.response.send_message(embed=embed)


keep_alive()
client.run(os.environ["TOKEN"])
