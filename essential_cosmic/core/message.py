import logging
from uuid import uuid4
from typing import Text, Dict


class Message:
    def __init__(self, offset: int, value: Text, topic):
        self.logger = logging.getLogger("essential_cosmic.message")

        self.topic = topic
        self.offset = offset
        self.value = value
        self.id = self.generate_id()

    def as_json(self) -> Dict:
        return {
            "offset": self.offset,
            "id": self.id,
            "value": self.value,
            "topic": self.topic.id,
        }

    @staticmethod
    def generate_id() -> Text:
        return str(uuid4())

    def __str__(self) -> Text:
        return self.id
