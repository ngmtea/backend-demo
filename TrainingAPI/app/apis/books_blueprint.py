import uuid

from sanic import Blueprint
from sanic.response import json
from app.decorators.auth import protected
from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
from app.databases.redis_cached import get_cache, set_cache
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiInternalError, ApiBadRequest
from app.models.book import create_book_json_schema, Book

books_bp = Blueprint('books_blueprint', url_prefix='/books')

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
@protected  # TODO: Authenticate
@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def create_book(request, username):
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

@books_bp.route('/<book_id>', methods={'DELETE'})
@protected  # TODO: Authenticate
#@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def delete_book(request, book_id, username):

    filter_ = {"_id": book_id}

    book_objs = _db.get_books(filter_)
    if (len(book_objs)==0):
        return json({
            "status": "Cannot find this book"
        })
    book = book_objs[0].to_dict()

    if book['owner'] != username:
        raise ApiBadRequest("You cannot have changes to this book")

    deleted = _db.delete_book(filter_)
    if not deleted:
        raise ApiInternalError('Fail to delete book')

    return json({'status': 'deleted successfully'})


@books_bp.route('/<book_id>/', methods={'GET'})
async def get_book(request, book_id):
    _filter = {"_id": book_id}
    print(_filter)
    book_objs = _db.get_books(_filter)
    if (len(book_objs)==0):
        return json({
            "status": "Cannot find this book"
        })
    book = book_objs[0].to_dict()
    #for book in book_objs:
    #    books = book.to_dict()
    #books = book_objs.to_dict()
    return json({
        'thisbook': book
    })

@books_bp.route('/<book_id>/', methods={'PUT'})
@protected
async def put_book(request, book_id, username):
    changed_data = request.json
    _filter = {"_id": book_id}
    print(_filter)
    book_objs = _db.get_books(_filter)
    if (len(book_objs)==0):
        return json({
            "status": "Cannot find this book"
        })
    book = book_objs[0].to_dict()

    if book['owner'] != username:
        raise ApiBadRequest("You cannot have changes to this book")

    changed = _db.put_book(_filter, changed_data)
    if not changed:
        raise ApiInternalError('Fail to change this book')

    # TODO: Update cache

    return json({'status': 'data changed successfully'})

