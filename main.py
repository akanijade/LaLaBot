import discord
#import music
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
#import nacl

#client = discord.Client()

# https://www.merriam-webster.com/thesaurus/unhappy
sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
    "heartbroken", "upset", "bad", "worried", "sorry", "dissapointed"
]

# https://memesbams.com/cheer-up-quotes/
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
# bot = commands.Bot(command_prefix = '/', intents=intents)
# bot = commands.Bot(intents=intents, command_prefix="!", help_command=None)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=691900717241335828))
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # await bot.process_commands(message)
    # doesn't work anymore??

    msg = message.content

    if msg == '/test':
        await message.channel.send('ping pong!')
    # if msg.startswith('!quote'):
    #     quote = get_quote()
    #     await message.channel.send(quote)

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
    

@tree.command(guild=discord.Object(id=691900717241335828))
async def slash(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.send_message(f'{number=} {string=}', ephemeral=True)
  # ephemeral = Only you can see this kind of message

# @client.command()
@tree.command(name = "quote", description = "Generate a random quote", guild=discord.Object(id=691900717241335828))
# @tree.command(name = "commandname", description = "My first application Command", guild=discord.Object(id=12417128931)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
# @app_commands.describe(attachment='The file to upload')
async def quote(interaction: discord.Interaction):
    # await member.send(message)
    quote = get_quote()
    await interaction.response.send_message(quote, ephemeral=False)
    # await message.channel.send(quote)
    # ctx.send(quote)

@tree.command(name = "dm", description = "Send a personal message to a user", guild=discord.Object(id=691900717241335828))
async def dm(interaction: discord.Interaction, member: discord.Member, *, message: str):
    await member.send(message)
    await interaction.response.send_message(":white_check_mark: Sent!")


@tree.command(name = "help", description = "Help Box", guild=discord.Object(id=691900717241335828))
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help Box",
                          description="Command lines that might work")
    # embed.set_author(name="akani", icon_url=ctx.author.avatar_url)
    # embed.set_author(name=client.user.name, icon=discord.Embed.Empty, icon_url=client.user.avatar_url)
    # embed.set_thumbnail(url="https://imgur.com/gallery/SwlZ2GC")
    # embed.set_image(
    #     "https://replit.com/@akanijade/Lala-Bot#This%20doggy%20just%20wants%20to%20cheer%20you%20up!%20-%20Imgur.jpg"
    # )
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
    # embed.add_field(name="!stream [link]", value="plays music", inline=False)
    # embed.add_field(name="!pause", value="pause music", inline=False)
    # embed.add_field(name="!resume", value="resume music", inline=False)
    # embed.add_field(name="!stop",
    #                 value="stop music and kicks bot ",
    #                 inline=True)
    embed.set_footer(
        text=
        "Hope it works, you can add new inspiring quotes by using !new [quote]"
    )
    await interaction.response.send_message(embed=embed)


#### Useful ctx variables ####
## User's display name in the server
#ctx.author.display_name

## User's avatar URL
#ctx.author.avatar_url

keep_alive()
# client.run(os.env("TOKEN"))
client.run(os.environ["TOKEN"])
