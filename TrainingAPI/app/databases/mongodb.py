from pymongo import MongoClient

from app.constants.mongodb_constants import MongoCollections
from app.models.book import Book
from app.models.user import User
from app.utils.logger_utils import get_logger
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None):
        if connection_url is None:
            #connection_url = f'mongodb://localhost:27017/'
            connection_url = f'mongodb://{MongoDBConfig.USERNAME}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}'

        self.connection_url = connection_url.split('@')[-1]
        self.client = MongoClient(connection_url)
        self.db = self.client[MongoDBConfig.DATABASE]

        self._books_col = self.db[MongoCollections.books]
        self._users_col = self.db[MongoCollections.users]

    def get_books(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._books_col.find(filter_, projection=projection)
            data = []
            for doc in cursor:
                data.append(Book().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []

    def add_book(self, book: Book):
        try:
            inserted_doc = self._books_col.insert_one(book.to_dict())
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
        return None

    # TODO: write functions CRUD with books

    def delete_book(self, _filter):
        if not _filter:
            return None
        try:
            deleted_doc = self._books_col.delete_one(_filter)
            return deleted_doc
        except Exception as ex:
            logger.exception(ex)
        return None

    def put_book(self, _filter, data):
        if not _filter:
            return None
        try:
            change_data = self._books_col.find_one_and_update(_filter, {"$set": data})
            return change_data
        except Exception as ex:
            logger.exception(ex)
        return None

    def get_users(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._users_col.find(filter_, projection=projection)
            data = []
            for doc in cursor:
                data.append(User().from_dict(doc))
            return data
        except Exception as ex:
            logger.exception(ex)
        return []

    def add_user(self, user: User):
        try:
            inserted_user_doc = self._users_col.insert_one(user.to_dict())
            return inserted_user_doc
        except Exception as ex:
            logger.exception(ex)
        return None

    def get_user(self, filter_=None, projection=None):
        try:
            if not filter_:
                filter_ = {}
            cursor = self._users_col.find(filter_, projection=projection)
            data = []
            for doc in cursor:
                data.append(User().from_dict(doc))
            return data[0]
        except Exception as ex:
            logger.exception(ex)
        return None

    def update_user_jwt(self, _filter, data):
        if not _filter:
            return None
        try:
            change_user_data = self._users_col.find_one_and_update(_filter, {"$set": data})
            return change_user_data
        except Exception as ex:
            logger.exception(ex)
        return None

