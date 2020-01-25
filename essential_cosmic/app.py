import logging

from aiohttp import web

from .apis import consumer
from .apis import producer
from .core.manager import TopicManager
from .core.message import Message
from .core.topic import Topic
from .middleware.topic import topic_or_404

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

logger.info("Created app")


def make_app():
    app = web.Application(middlewares=[topic_or_404])
    app.add_routes(consumer.routes)
    app.add_routes(producer.routes)

    # Initalize Topic Manager
    topic_manager = TopicManager()

    app["topic_manager"] = topic_manager

    return app


app = make_app()

if __name__ == "__main__":
    logger.info("Starting App")
    web.run_app(make_app())
