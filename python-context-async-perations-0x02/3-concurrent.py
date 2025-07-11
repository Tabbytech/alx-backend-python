import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM users")
            return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM users WHERE age > ?", (40,))
            return await cursor.fetchall()

async def fetch_concurrently():
    results = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    all_users = results[0]
    older_users = results[1]
    print("All Users:", all_users)
    print("Users Older Than 40:", older_users)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
