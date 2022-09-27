import uuid

from sanic import Blueprint
from sanic.response import json

from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
from app.databases.redis_cached import get_cache, set_cache
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiInternalError
from app.models.book import create_book_json_schema, Book
from app.models.user import User

books_bp = Blueprint('books_blueprint', url_prefix='/books')
users_bp = Blueprint('users_blueprint', url_prefix='/users')

_db = MongoDB()


@books_bp.route('/', methods={'GET'})
async def get_all_books(request):
    # # TODO: use cache to optimize api
    async with request.app.ctx.redis as r:
        books = await get_cache(r, CacheConstants.all_books)
        if books is None:
            book_objs = _db.get_books()
            books = [book.to_dict() for book in book_objs]
            await set_cache(r, CacheConstants.all_books, books)
    #book_objs = _db.get_books({})
    #books = [book.to_dict() for book in book_objs]
    number_of_books = len(books)
    return json({
        'n_books': number_of_books,
        'books': books
    })


@books_bp.route('/', methods={'POST'})
# @protected  # TODO: Authenticate
@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def create_book(request, username=None):
    body = request.json

    book_id = str(uuid.uuid4())
    book = Book(book_id).from_dict(body)
    book.owner = username

    # # TODO: Save book to database
    inserted = _db.add_book(book)
    if not inserted:
        raise ApiInternalError('Fail to create book')

    # TODO: Update cache

    return json({'status': 'success'})


# TODO: write api get, update, delete book

@books_bp.route('/', methods={'DELETE'})
# @protected  # TODO: Authenticate
#@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def delete_book(request, username=None):
    filter_find = request.json

    # # TODO: Save book to database
    deleted = _db.delete_book(filter_find)
    if not deleted:
        raise ApiInternalError('Fail to delete book')

    # TODO: Update cache

    return json({'status': 'deleted successfully'})


@books_bp.route('/<book_id>/', methods={'GET'})
async def get_book(request, book_id):
    _filter = {"_id": book_id}
    print(_filter)
    book_objs = _db.get_books(_filter)
    books = [book.to_dict() for book in book_objs]
    return json({
        'books': books
    })

@users_bp.route('/', methods={'GET'})
async def get_all_users(request):
    async with request.app.ctx.redis as r:
        users = await get_cache(r, CacheConstants.all_users)
        if users is None:
            users_objs = _db.get_books({})
            users = [user.to_dict() for user in users_objs]
            await set_cache(r, CacheConstants.all_users, users)
    #book_objs = _db.get_books({})
    #books = [book.to_dict() for book in book_objs]
    number_of_users = len(users)
    return json({
        'n_users': number_of_users,
        'books': users
    })
