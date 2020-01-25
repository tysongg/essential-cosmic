import pytest
import os
import sys

# Workaround so we don't have to create a setup.py file for the project and
# install an editable version
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from essential_cosmic.core.topic import Topic
from essential_cosmic.core.message import Message
from essential_cosmic.core.manager import TopicManager


@pytest.fixture()
def topic():
    manager = TopicManager()
    topic = Topic("test topic", manager=manager)

    return topic


def test_new_message(topic):

    message = topic.new_message("Test Message")

    assert type(message) == Message
    assert len(topic._messages) == 1


def test_get_messages(topic):

    [topic.new_message("Test message") for _ in range(3)]

    assert len(topic._messages) == 3

    assert len(topic.get_messages()) == 3
    assert len(topic.get_messages(offset=1)) == 2
    assert len(topic.get_messages(count=2)) == 2
    assert len(topic.get_messages(offset=1, count=1)) == 1


def test_as_json(topic):

    topic_json = topic.as_json()
    assert topic_json == {
        "id": topic.id,
        "title": topic.title,
        "message_count": topic.count,
    }


def test_generate_id():

    assert Topic.generate_id() != Topic.generate_id()


def test_str(topic):

    assert str(topic) == topic.id
