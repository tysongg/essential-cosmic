import aiohttp
import asyncio
import json


async def main():

    session = aiohttp.ClientSession()

    resp = await session.post(
        "http://localhost:8000/topic", json={"title": "Websocket Test"}
    )
    resp_json = await resp.json()
    print(resp_json)

    async with session.ws_connect("http://localhost:8000/ws") as ws:
        await ws.send_str(json.dumps({"action": "join", "topics": [resp_json["id"]]}))
        msg = await ws.receive_str()
        print(msg)

        await ws.send_str(json.dumps({"action": "quit"}))


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
