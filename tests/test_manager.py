import pytest
import os
import sys

# Workaround so we don't have to create a setup.py file for the project and
# install an editable version
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from essential_cosmic.core.errors import TopicExistsError
from essential_cosmic.core.manager import TopicManager
from essential_cosmic.core.topic import Topic


class TestTopicManager:
    @pytest.fixture()
    def manager(self):
        manager = TopicManager()

        return manager

    def test_new_topic(self, manager):

        topic = manager.new_topic("Test Topic")

        assert type(topic) == Topic
        assert topic.title == "Test Topic"

        assert len(manager._topics) == 1
        assert manager._topics[topic.id] == topic

    def test_new_topic_duplicate(self, manager):

        manager.new_topic("Test Topic")
        manager.new_topic("Test Topic Two")

        with pytest.raises(TopicExistsError):
            manager.new_topic("Test Topic")

    def test_get_topic(self, manager):

        topic = manager.new_topic("Test Topic")

        assert manager.get_topic(topic.id) == topic
        assert manager.get_topic("") == None

    def test_get_topics(self, manager):

        topics = manager.get_topics()
        assert type(topics) == list
        assert len(topics) == 0

        manager.new_topic("Test Topic")
        topics = manager.get_topics()
        assert len(topics) == 1
