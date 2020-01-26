import logging
import json

from .message import Message
from typing import List, Dict
from aiohttp.web import WebSocketResponse


class WebsocketManager:

    _watchers = Dict[str, List[WebSocketResponse]]

    def __init__(self):
        self.logger = logging.getLogger("essential_cosmic.websocket_manager")
        self._watchers = {}

    async def add_watcher(self, topic_id: str, watcher: WebSocketResponse):

        if not topic_id in self._watchers.keys():
            self._watchers[topic_id] = []

        if not watcher in self._watchers[topic_id]:
            self.logger.info("Subscribed %s to topic %s" % (watcher, topic_id))
            self._watchers[topic_id].append(watcher)

    async def remove_watcher_from_topic(
        self, topic_id: str, watcher: WebSocketResponse
    ):

        if topic_id in self._watchers.keys() and watcher in self._watchers[topic_id]:
            self._watchers[topic_id].remove(watcher)
            self.logger.debug("Unsubscribed %s from topic %s", watcher, topic_id)

    async def remove_watcher(self, watcher: WebSocketResponse):

        for topic_id in self._watchers.keys():
            await self.remove_watcher_from_topic(topic_id, watcher)

        self.logger.info("Unsubscribed %s from all topics" % watcher)

    async def new_message(self, message: Message):

        self.logger.debug("Message %s sent to websocket manager" % message)
        watchers = self._watchers.get(message.topic.id, None)

        if watchers is not None:
            for watcher in watchers:

                if not watcher.closed:
                    await watcher.send_str(json.dumps(message.as_json()))
                    self.logger.debug("Sent message %s to %s", message, watcher)
                else:
                    self.logger.debug("%s is closed.")

