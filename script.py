import asyncio
import websockets
import json


async def test():
    uri = "ws://127.0.0.1:8000/ws/chat/room1/"
    async with websockets.connect(uri) as ws:
        await ws.send("hello")
        print(await ws.recv())

asyncio.run(test())
