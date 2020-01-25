import logging
import json
from typing import Dict

from aiohttp import web, WSMsgType


logger = logging.getLogger("essential_cosmic.api.websocket")
routes = web.RouteTableDef()


@routes.get("/ws")
async def websocket_topic(request: web.Request) -> web.WebSocketResponse:

    ws = web.WebSocketResponse(autoping=True, heartbeat=2.0)

    await ws.prepare(request)

    async for msg in ws:

        if msg.type == WSMsgType.TEXT:
            try:
                messsage = json.loads(msg.data)
                logger.debug("Recieved message: %s", msg.data)

                action = messsage.get("action", None)
                if action == "join":
                    ws.send_str("Joined!")

                if action == "quit":
                    ws.close()

            except (json.decoder.JSONDecodeError):
                logger.info("Recieved non-json message on websocket")

        elif msg.type == WSMsgType.ERROR:
            logger.info("Websocket connection closed with exception %s", ws.exception())

    logger.info("Websocket connection closed")
    return ws
