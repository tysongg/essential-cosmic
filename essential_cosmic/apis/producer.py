import logging
import json

from aiohttp import web

from ..core.errors import TopicExistsError


logger = logging.getLogger("essential_cosmic.api.producer")
routes = web.RouteTableDef()


@routes.post("/topic")
async def topic_create(request: web.Request) -> web.Response:

    try:
        topic_data = await request.json()
    except (json.decoder.JSONDecodeError):
        return web.json_response({"message": "Invalid input"}, status=400)

    if topic_data.get("title", None) is None:
        return web.json_response({"message": "Title is a required input"}, status=400)

    try:
        topic = request.app["topic_manager"].new_topic(topic_data["title"])
    except (TopicExistsError):
        return web.json_response({"message": "Topic already exists"}, status=400)

    return web.json_response(topic.as_json())


@routes.post("/topic/{topic_id}/message")
async def message_create(request: web.Request) -> web.Response:

    topic = request["topic"]

    try:
        message_data = await request.json()
    except (json.decoder.JSONDecodeError):
        return web.json_response({"message": "Invalid input"}, status=400)

    if message_data.get("value", None) is None:
        return web.json_response({"message": "Value is a required input"}, status=400)

    message = topic.new_message(message_data["value"])

    return web.json_response(message.as_json())
