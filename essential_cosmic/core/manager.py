import logging
from typing import Dict, List, Optional, Text

from .errors import TopicExistsError
from .topic import Topic
from .websocket import WebsocketManager


class TopicManager:

    _topics: Dict[str, Topic]

    def __init__(self, websocket_manager: WebsocketManager):
        self.logger = logging.getLogger("essential_cosmic.topic_manager")

        self.websocket_manager = websocket_manager
        self._topics = {}

    async def new_topic(self, title: Text) -> Topic:

        # Refactor to be more efficent
        for topic in self._topics.values():
            if topic.title == title:
                raise TopicExistsError("%s topic already exists")

        new_topic = Topic(title, manager=self)
        self._topics[new_topic.id] = new_topic
        self.logger.debug("Added topic %s", new_topic)

        return new_topic

    async def get_topic(self, id: Text) -> Optional[Topic]:
        self.logger.debug("Retrieving topic %s", id)

        return self._topics.get(id, None)

    async def get_topics(self) -> List[Topic]:
        self.logger.debug("Retrieved topic list")

        return list(self._topics.values())
