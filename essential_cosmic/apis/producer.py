import logging

from aiohttp import web


logger = logging.getLogger('essential_cosmic.api.producer')
routes = web.RouteTableDef()

@routes.post('/topic')
async def topic_create(request: web.Request) -> web.Response:

    topic_data = await request.json()
    topic = request.app['topic_manager'].new_topic(topic_data['title'])

    return web.json_response(topic.as_json())

@routes.post('/topic/{topic_id}/message')
async def message_create(request: web.Request) -> web.Response:

    topic = request['topic']

    message_data = await request.json()
    message = topic.new_message(message_data['value'])

    return web.json_response(message.as_json())