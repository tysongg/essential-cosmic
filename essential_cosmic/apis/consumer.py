import logging
from typing import Text

from aiohttp import web


logger = logging.getLogger("essential_cosmic.api.consumer")
routes = web.RouteTableDef()


@routes.get("/topic")
async def topic_index(request: web.Request) -> web.Response:
    return web.json_response(
        [topic.as_json() for topic in request.app["topic_manager"].get_topics()]
    )


@routes.get("/topic/{topic_id}")
async def topic_details(request: web.Request) -> web.Response:

    topic = request["topic"]

    return web.json_response(topic.as_json())


@routes.get("/topic/{topic_id}/message")
async def topic_message(request: web.Request) -> web.Response:

    message_offset = request.query.get("offset", None)
    message_count = request.query.get("count", None)

    topic = request["topic"]

    return web.json_response(
        [
            message.as_json()
            for message in topic.get_messages(message_offset, message_count)
        ]
    )
