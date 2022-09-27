import time


class Book:
    def __init__(self, _id=''):
        self._id = _id
        self.username = ''
        self.password = ''
        self.roles = []
        self.mechanisms = []

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'password': self.password,
            'roles': self.roles,
            'mechanisms': self.mechanisms,
        }

    def from_dict(self, json_dict: dict):
        self._id = json_dict.get('_id', self._id)
        self.username = json_dict.get('username', '')
        self.password = json_dict.get('password', '')
        self.roles = json_dict.get('roles', [])
        self.mechanisms = json_dict.get('mechanisms', [])
        return self


create_book_json_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'roles': {'type': 'array', 'items': {'role' : {'type': 'string'}}},
        'publisher': {'type': 'string'},
        'description': {'type': 'string'},
    },
    'required': ['title', 'authors', 'publisher']
}
