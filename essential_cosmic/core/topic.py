import logging
from typing import Text, List, Optional, Dict
from uuid import uuid4

from .message import Message


class Topic:

    _messages: List[Message]
    _next_index: int

    def __init__(self, title: Text, manager):
        self.logger = logging.getLogger("essential_cosmic.topic")

        self.manager = manager

        self.id = self.generate_id()
        self.title = title

        self._messages = []
        self._next_index = 0

    @property
    def count(self) -> int:
        return self._next_index

    def new_message(self, value: Text) -> Message:

        message = Message(self._next_index, value, topic=self)
        self._next_index += 1

        self._messages.append(message)
        self.logger.debug("Added message %s to topic %s", message, self)

        return message

    def get_messages(
        self, offset: Optional[int] = None, count: Optional[int] = None
    ) -> List[Message]:

        o: Optional[int]
        c: Optional[int]

        o, c = self._parse_offset_and_count(offset, count)

        return self._messages[o:c]

    def _parse_offset_and_count(
        offset: Optional[int] = None, count: Optional[int] = None
    ) -> List[Optional[int]]:
        o: Optional[int]
        c: Optional[int]

        o = int(offset) if offset is not None else None
        o = 0 if o is not None and o < 0 else o
        if o is not None:
            if count is not None:
                if count >= 0:
                    c = o + int(count)
                else:
                    c = None
            else:
                c = None
        elif count is not None:
            if count >= 0:
                c = int(count)
            else:
                c = None
        else:
            c = None

        return [o, c]

    def as_json(self) -> Dict:
        return {"title": self.title, "id": str(self.id), "message_count": self.count}

    @staticmethod
    def generate_id() -> Text:
        return str(uuid4())

    def __str__(self):
        return self.id
