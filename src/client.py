import discord
from discord.ext import commands
from commands import setup
import os
from dotenv import load_dotenv
from commands.admin import Admin
import asyncio

load_dotenv()

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client.remove_command("help")


#setup(client)


def main(): 
    loop = asyncio.new_event_loop()
    loop.run_until_complete(client.add_cog(Admin(client)))

    
    client.run(os.getenv("DC_token"))


if __name__ == "__main__":
    asyncio.run(main())
    #print(client.commands)

