import uuid
import hashlib

from sanic import Blueprint
from sanic.response import json
from app.decorators.auth import protected
from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
from app.databases.redis_cached import get_cache, set_cache
from app.decorators.json_validator import validate_with_jsonschema
from app.hooks.error import ApiInternalError, ApiBadRequest
from app.models.user import User, create_user_json_schema

from app.utils.jwt_utils import generate_jwt

users_bp = Blueprint('users_blueprint', url_prefix='/users')

_db = MongoDB()


@users_bp.route('/', methods={'GET'})
async def get_all_users(request):
    # # TODO: use cache to optimize api
    async with request.app.ctx.redis as r:
        users = await get_cache(r, CacheConstants.all_users)
        if users is None:
            user_objs = _db.get_users()
            users = [user.to_dict() for user in user_objs]
            await set_cache(r, CacheConstants.all_users, users)
    #user_objs = _db.get_users({})
    #users = [user.to_dict() for user in user_objs]
    number_of_users = len(users)
    return json({
        'n_users': number_of_users,
        'users': users
    })


@users_bp.route('/register', methods={'POST'})
# @protected  # TODO: Authenticate
@validate_with_jsonschema(create_user_json_schema)  # To validate request body
async def create_user(request):
    body = request.json
    check_username = _db.get_user(({"username": body['username']}))

    if check_username:
        raise ApiBadRequest(f"username {body['username']} existed")

    user_id = str(uuid.uuid4())
    user = User(user_id).from_dict(body)

    # # TODO: Save user to database
    inserted = _db.add_user(user)
    if not inserted:
        raise ApiInternalError('Fail to create user')

    # TODO: Update cache

    return json({'status': 'register success'})


@users_bp.route('/login', methods={'POST'})
@validate_with_jsonschema(create_user_json_schema)
async def login_user(request):
    body = request.json

    user_name = body["username"]
    user_password = body['password']
    account = _db.get_user({"username": user_name, "password": user_password})
    if not account:
        raise ApiBadRequest("Username or password incorrect")

    token_jwt = generate_jwt(user_name)
    change_jwt = _db.update_user_jwt({"username": user_name}, {"jwt": str(token_jwt)})
    if not change_jwt:
        raise ApiInternalError('Failed to login')

    return json({
        'status': "Login success",
    })


@users_bp.route('/now', methods={'GET'})
@protected
async def now_user(request, username):
    return json({
        'now login': username
    })

