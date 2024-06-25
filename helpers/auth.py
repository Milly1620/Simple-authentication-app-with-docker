from datetime import datetime, timedelta, timezone
import json
from graphql import GraphQLError
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
import os
from dotenv import load_dotenv

load_dotenv()

secret = os.getenv('SECRET_KEY')
algorithms = os.getenv('ALGORITHM')
user_authentication = 'User is not authenticated'
user_action = 'Cannot perform this action'
user_login = 'Token is expired. Login again'
invalid_token = 'Invalid token'


def is_admin(info):
    req = info.context["request"]
    token_string = req.headers.get('Authorization')
    if token_string is None:
        raise GraphQLError(user_authentication)
    try:
        token = token_string.split(" ")[1]
        if not isinstance(token, str):  # ensure that token is a string
            token = str(token)
        payload = jwt.decode(token, secret, algorithms)
        # now we should update 'exp' for 5 seconds again
        payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(seconds=5)
        
        if "role" in payload and payload["role"] == ['super admin']:
            ...
        else:
            raise GraphQLError(user_action)
    except ExpiredSignatureError:
        raise GraphQLError(user_login)
    except DecodeError:
        raise GraphQLError(invalid_token)
    except IndexError:
        raise GraphQLError(user_authentication)


def is_authenticated(info):
    req = info.context["request"]
    token_string = req.headers.get('Authorization')
    if token_string is None:
        raise GraphQLError(user_authentication)
    try:
        token = token_string.split(" ")[1]
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        if payload:
            return token
        else:
            raise GraphQLError(user_authentication)
    except ExpiredSignatureError:
        raise GraphQLError(user_login)
    except DecodeError:
        raise GraphQLError(invalid_token)
    except IndexError:
        raise GraphQLError(user_authentication)


# Gateway authentication
def auth(info):
    req = info.context["request"]
    token = req.headers.get('token')
    if token == "undefined":
        raise GraphQLError(user_authentication)
    user_header = json.loads(req.headers.get('user'))
    if not user_header:
        raise GraphQLError('User not authenticated')
    elif "JsonWebTokenError" in user_header.values():
        raise GraphQLError(invalid_token)
    elif "role" in user_header:
        if user_header["role"] == "admin":
            ...
    elif "TokenExpiredError" in user_header.values():
        raise GraphQLError(user_login)
    else:
        raise GraphQLError(user_action)
