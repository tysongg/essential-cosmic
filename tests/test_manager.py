import pytest
import os
import sys

# Workaround so we don't have to create a setup.py file for the project and
# install an editable version
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from essential_cosmic.core.errors import TopicExistsError
from essential_cosmic.core.manager import TopicManager
from essential_cosmic.core.topic import Topic
from essential_cosmic.core.websocket import WebsocketManager


class TestTopicManager:
    @pytest.fixture()
    def manager(self):
        manager = TopicManager(WebsocketManager())

        return manager

    async def test_new_topic(self, manager):

        topic = await manager.new_topic("Test Topic")

        assert type(topic) == Topic
        assert topic.title == "Test Topic"

        assert len(manager._topics) == 1
        assert manager._topics[topic.id] == topic

    async def test_new_topic_duplicate(self, manager):

        await manager.new_topic("Test Topic")
        await manager.new_topic("Test Topic Two")

        with pytest.raises(TopicExistsError):
            await manager.new_topic("Test Topic")

    async def test_get_topic(self, manager):

        topic = await manager.new_topic("Test Topic")

        assert await manager.get_topic(topic.id) == topic
        assert await manager.get_topic("") == None

    async def test_get_topics(self, manager):

        topics = await manager.get_topics()
        assert type(topics) == list
        assert len(topics) == 0

        await manager.new_topic("Test Topic")
        topics = await manager.get_topics()
        assert len(topics) == 1
