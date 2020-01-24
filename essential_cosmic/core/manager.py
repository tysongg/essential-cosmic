import logging
from typing import Dict, List, Optional, Text

from .errors import TopicExistsError
from .topic import Topic

class TopicManager:

    _topics: Dict[str, Topic]

    def __init__(self):
        self.logger = logging.getLogger('essential_cosmic.topic_manager')
        self._topics = {}
    
    def new_topic(self, title: Text) -> Topic:

        # Refactor to be more efficent
        for topic in self._topics.values():
            if topic.title == title:
                raise TopicExistsError('%s topic already exists')
        
        new_topic = Topic(title, manager=self)
        self._topics[new_topic.id] = new_topic
        self.logger.debug('Added topic %s', new_topic)

        return new_topic

    def get_topic(self, id: Text) -> Optional[Topic]:
        self.logger.debug('Retrieving topic %s', id)

        return self._topics.get(id, None)

    def get_topics(self) -> List[Topic]:
        self.logger.debug('Retrieved topic list')

        return list(self._topics.values())
