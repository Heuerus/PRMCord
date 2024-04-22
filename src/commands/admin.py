from db import db, cursor
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="refill")
    async def refill(ctx):  
        user_id = ctx.author.id
        if user_id == 284347406420803596 or user_id == 574953391705292801 or user_id == 262646553506873345:
            cursor.execute("UPDATE fantasy SET pulls = 10")
            db.commit()
            cursor.execute("UPDATE fantasy SET pulls = pulls + 5 ORDER BY elo DESC LIMIT 5")
            db.commit()
            cursor.execute("UPDATE fantasy SET pulls = pulls + 4 WHERE liga = 1")
            cursor.execute("UPDATE fantasy SET pulls = pulls + 3 WHERE liga = 2")
            cursor.execute("UPDATE fantasy SET pulls = pulls + 2 WHERE liga = 3")
            cursor.execute("UPDATE fantasy SET pulls = pulls + 1 WHERE liga = 4")
            db.commit()
        else:
            await ctx.send("Du hast keine Berechtigung dazu")

def setup(client):
    client.add_cog(Admin(client))
    return client