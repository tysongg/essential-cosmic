from aiohttp import web

@web.middleware
async def topic_or_404(request: web.Request, handler) -> web.Response:
    
    topic_id = request.match_info.get('topic_id', None)

    if topic_id is not None:
        topic = request.app['topic_manager'].get_topic(topic_id)
        if topic is None:
            return web.json_response({
                "message": "Topic does not exist"
            }, status=404)
        else:
            request['topic'] = topic
    return await handler(request)
