import json
from typing import Union, Optional

from telebot import types

from .languages import Language

NONE_ID = -1


class DatabaseUsersMockUp:
    id: int
    name: str
    username: str
    lang: str
    bot_can_message: bool


class TGUser:
    __slots__ = ('id', 'first_name', 'username', 'lang', 'bot_can_message')

    id: int
    first_name: str
    username: str
    lang: Language
    bot_can_message: Optional[bool]

    def __init__(self, data: Optional[Union[str, dict, types.User, DatabaseUsersMockUp]] = None):
        if not data:
            self.id = NONE_ID
            self.first_name = '?'
            self.username = ''
            self.lang = Language()
            self.bot_can_message = False
            return

        if isinstance(data, str):
            data = json.loads(data)
            self.id = data['id']
            self.first_name = data['first_name']
            self.username = data['username']
            language_code = data['language_code']
            self.bot_can_message = data['bot_can_message']
        elif isinstance(data, types.User):
            self.id = data.id
            self.first_name = data.first_name
            self.username = data.username
            language_code = data.language_code
            self.bot_can_message = None
        else:  # database.Users, cannot import due to recursive import
            self.id = data.id
            self.first_name = data.name
            self.username = data.username
            language_code = data.lang
            self.bot_can_message = data.bot_can_message

        self.lang = Language(language_code or 'en')

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.first_name,
            username=self.username,
            lang=self.lang.code,
            bot_can_message=self.bot_can_message,
        )

    def __repr__(self):
        return str(self.to_dict())

    def __str__(self):
        return self.first_name

    def __bool__(self):
        return self.id != NONE_ID

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id
