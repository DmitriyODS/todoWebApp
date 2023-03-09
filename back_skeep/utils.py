from functools import wraps

import jwt
from flask import request

from back_skeep.models.response import make_response_with_err
from back_skeep.models.user import User

# самый секретный секрет, так делать не надо, но для учебного проекта - можно
SECRET_KEY = "THE_MOST_SECRET_SECRET_THAT_CAN_BE"


def parse_jwt(token: str) -> (bool, dict):
    try:
        res = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return True, res
    except jwt.PyJWTError:
        return False, None


def new_jwt(user: User) -> str:
    encoded_jwt = jwt.encode({
        "user_id": user.id,
        "is_admin": user.is_admin
    }, SECRET_KEY, algorithm="HS256")

    return encoded_jwt


def auth_user_check(handler):
    @wraps(handler)
    def checkers(*args, **kwargs):
        req = request.json
        if req is None:
            return make_response_with_err(401, 'Не авторизован')

        ok, data = parse_jwt(req.get('token', ''))
        if not ok:
            return make_response_with_err(401, 'Не авторизован')

        return handler(*args, **kwargs)

    return checkers


def auth_admin_check(handler):
    @wraps(handler)
    def checkers(*args, **kwargs):
        req = request.json
        if req is None:
            return make_response_with_err(401, 'Не авторизован')

        ok, data = parse_jwt(req.get('token', ''))
        if not ok:
            return make_response_with_err(401, 'Не авторизован')

        if not data.get('is_admin', False):
            return make_response_with_err(403, 'Доступ запрещён')

        return handler(*args, **kwargs)

    return checkers
