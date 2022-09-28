import time


class User:
    def __init__(self, _id=''):
        self._id = _id
        self.username = ''
        self.password = ''
        self.jwt = ''

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'password': self.password,
            'jwt': self.jwt
        }

    def from_dict(self, json_dict: dict):
        self._id = json_dict.get('_id', self._id)
        self.username = json_dict.get('username', '')
        self.password = json_dict.get('password', '')
        self.jwt = json_dict.get('jwt', '')
        return self


create_user_json_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['username', 'password']
}
