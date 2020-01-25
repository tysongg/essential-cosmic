import pytest
import os
import sys

# Workaround so we don't have to create a setup.py file for the project and
# install an editable version
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from essential_cosmic.core.message import Message
from essential_cosmic.core.topic import Topic
from essential_cosmic.core.manager import TopicManager


class TestMessage:
    @pytest.fixture()
    def topic(self):
        manager = TopicManager()
        topic = Topic("Test Topic", manager=manager)

        return topic

    @pytest.fixture()
    def message(self, topic):

        message = Message(offset=0, value="Test Message", topic=topic)

        return message

    def test_as_json(self, message):

        assert message.as_json() == {
            "topic": message.topic.id,
            "offset": message.offset,
            "id": message.id,
            "value": message.value,
        }

    def test_generate_id(self):

        assert Message.generate_id() != Message.generate_id()

    def test_str(self, message):

        assert str(message) == message.id
