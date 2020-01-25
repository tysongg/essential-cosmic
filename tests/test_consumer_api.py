import pytest
import asyncio
import os
import sys

# Workaround so we don't have to create a setup.py file for the project and
# install an editable version
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from essential_cosmic.app import make_app


class TestConsumer:
    @pytest.fixture(scope="function")
    async def cli(self, aiohttp_client):
        client = await aiohttp_client(make_app())

        return client

    @pytest.fixture(scope="function")
    async def topic(self, cli):
        resp = await cli.post("/topic", json={"title": "Test Topic"})
        topic = await resp.json()

        return topic

    @pytest.fixture(scope="function")
    async def messages(self, cli, topic):
        resps = await asyncio.gather(
            *[
                cli.post(
                    "/topic/%s/message" % topic["id"], json={"value": "Test Message"}
                )
                for _ in range(3)
            ]
        )
        messages = await asyncio.gather(*[resp.json() for resp in resps])

        return messages

    async def test_topic_list(self, cli, topic):
        resp = await cli.get("/topic")
        assert resp.status == 200

        body_json = await resp.json()
        assert type(body_json) == list
        assert len(body_json) == 1

    async def test_topic_detail(self, cli, topic):
        resp = await cli.get("/topic/%s" % topic["id"])
        assert resp.status == 200

        resp_json = await resp.json()
        assert resp_json == topic

    async def test_topic_detail_missing(self, cli):
        resp = await cli.get("/topic/missing")
        assert resp.status == 404

        resp_json = await resp.json()
        assert resp_json["message"] == "Topic does not exist"

    async def test_topic_message_empty(self, cli, topic):
        resp = await cli.get("/topic/%s/message" % topic["id"])
        assert resp.status == 200

        resp_json = await resp.json()
        assert type(resp_json) == list
        assert len(resp_json) == 0

    async def test_topic_message(self, cli, topic, messages):
        resp = await cli.get("/topic/%s/message" % topic["id"])
        assert resp.status == 200

        resp_json = await resp.json()
        assert resp_json == messages
        assert len(resp_json) == 3

    async def test_topic_message_offset(self, cli, topic, messages):
        resp = await cli.get("/topic/%s/message?offset=1" % topic["id"])
        assert resp.status == 200

        resp_json = await resp.json()
        assert resp_json == messages[1:]
        assert len(resp_json) == 2

    async def test_topic_message_count(self, cli, topic, messages):
        resp = await cli.get("/topic/%s/message?count=2" % topic["id"])
        assert resp.status == 200

        resp_json = await resp.json()
        assert resp_json == messages[:2]
        assert len(resp_json) == 2

    async def test_topic_message_offset_and_count(self, cli, topic, messages):
        resp = await cli.get("/topic/%s/message?offset=1&count=1" % topic["id"])
        assert resp.status == 200

        resp_json = await resp.json()
        assert resp_json == messages[1:2]
        assert len(resp_json) == 1
