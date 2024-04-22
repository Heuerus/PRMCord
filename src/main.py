import os
from client import client
from dotenv import load_dotenv
import asyncio

load_dotenv()

def main():
    client.run(os.getenv("DC_token"))

if __name__ == "__main__":
    main()
