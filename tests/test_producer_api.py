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

    async def test_topic_create(self, cli):
        resp = await cli.post("/topic", json={"title": "Test Topic"})
        assert resp.status == 200

        resp_json = await resp.json()
        assert resp_json["title"] == "Test Topic"
        assert resp_json["message_count"] == 0

    async def test_topic_create_duplicate(self, cli):
        await cli.post("/topic", json={"title": "Test Topic"})
        resp = await cli.post("/topic", json={"title": "Test Topic"})
        assert resp.status == 400

        resp_json = await resp.json()
        assert resp_json["message"] == "Topic already exists"

    async def test_topic_create_missing_input(self, cli):
        resp = await cli.post("/topic")
        assert resp.status == 400

        resp_json = await resp.json()
        assert resp_json["message"] == "Invalid input"

    async def test_topic_create_no_title(self, cli):
        resp = await cli.post("/topic", json={"foo": "bar"})
        assert resp.status == 400

        resp_json = await resp.json()
        assert resp_json["message"] == "Title is a required input"

    async def test_message_create(self, cli, topic):
        resp = await cli.post(
            "/topic/%s/message" % topic["id"], json={"value": "Test Message"}
        )
        assert resp.status == 200

        resp_json = await resp.json()
        assert resp_json["value"] == "Test Message"
        assert resp_json["offset"] == 0
        assert resp_json["topic"] == topic["id"]

    async def test_message_create_missing_topic(self, cli):
        resp = await cli.post("/topic/missing/message")
        assert resp.status == 404

        resp_json = await resp.json()
        assert resp_json["message"] == "Topic does not exist"

    async def test_message_create_missing_input(self, cli, topic):
        resp = await cli.post("/topic/%s/message" % topic["id"])
        assert resp.status == 400

        resp_json = await resp.json()
        assert resp_json["message"] == "Invalid input"

    async def test_message_create_no_value(self, cli, topic):
        resp = await cli.post("/topic/%s/message" % topic["id"], json={"foo": "bar"})
        assert resp.status == 400

        resp_json = await resp.json()
        assert resp_json["message"] == "Value is a required input"
