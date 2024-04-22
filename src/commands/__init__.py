from .admin import setup as setup_admin

async def setup(client):
    client2 = await setup_admin(client)
    return client2
    