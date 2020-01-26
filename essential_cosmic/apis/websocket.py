import logging
import json
from typing import Dict
import asyncio

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
                message = json.loads(msg.data)
                logger.debug("Recieved message: %s", msg.data)

                action = message.get("action", None)
                if action == "join":

                    topic_manger = request.app["topic_manager"]
                    for topic_id in message.get("topics", []):
                        topic = topic_manger.get_topic(topic_id)
                        await ws.send_str(
                            json.dumps({"message": "joined %s" % topic_id})
                        )
                        if topic is not None:
                            logger.info("Subscribing websocket to topic %s" % topic)
                            await request.app[
                                "topic_manager"
                            ].websocket_manager.add_watcher(topic_id, ws)

                if action == "quit":
                    # TODO: Unsubscribe websocket from all topics
                    await ws.close()

            except (json.decoder.JSONDecodeError):
                logger.info("Recieved non-json message on websocket")

            except (asyncio.CancelledError):
                logger.info("Recieved cancellation error")
                break

        elif msg.type == WSMsgType.ERROR:
            logger.info("Websocket connection closed with exception %s", ws.exception())

    await request.app["topic_manager"].websocket_manager.remove_watcher(ws)
    logger.info("Websocket connection closed")
    return ws
