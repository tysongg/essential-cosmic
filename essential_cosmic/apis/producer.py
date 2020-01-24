import logging

from aiohttp import web

from ..core.errors import TopicExistsError


logger = logging.getLogger('essential_cosmic.api.producer')
routes = web.RouteTableDef()

@routes.post('/topic')
async def topic_create(request: web.Request) -> web.Response:

    topic_data = await request.json()

    try:
        topic = request.app['topic_manager'].new_topic(topic_data['title'])
    except(TopicExistsError):
        return web.json_response({'message': 'Topic already exists'}, status=400)

    return web.json_response(topic.as_json())

@routes.post('/topic/{topic_id}/message')
async def message_create(request: web.Request) -> web.Response:

    topic = request['topic']

    message_data = await request.json()
    message = topic.new_message(message_data['value'])

    return web.json_response(message.as_json())