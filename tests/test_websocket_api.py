import pytest
import asyncio
import os
import sys
import json
import logging

from aiohttp import web

# Workaround so we don't have to create a setup.py file for the project and
# install an editable version
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from essential_cosmic.apis import websocket


class TestWebsocket:
    def create_app(self, loop):
        app = web.Application()
        app.add_routes(websocket.routes)

        return app

    @pytest.fixture(scope="function")
    async def cli(self, test_client):
        client = await test_client(self.create_app)

        return client

    async def test_websocket(self, cli):
        async with cli.ws_connect("/ws") as ws:

            await ws.send_str(json.dumps({"action": "join", "topics": ["1234"]}))
            async for msg in ws:
                assert (msg.data) is not None
                print(msg)
