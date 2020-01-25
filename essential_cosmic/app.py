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

app = web.Application(middlewares=[topic_or_404])
app.add_routes(consumer.routes)
app.add_routes(producer.routes)

# Sample data
topic_manager = TopicManager()
topic = topic_manager.new_topic("test_topic")
topic.new_message('{"Foo": "Bar"}')
topic.new_message('{"Fizz": "Bizz"}')
topic.new_message('{"Key": "Value"}')

app["topic_manager"] = topic_manager

logger.info("Created app")

if __name__ == "__main__":
    logger.info("Starting App")
    web.run_app(app)
