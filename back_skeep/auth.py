from flask import request
from flask_restful import Resource

from back_skeep.models.response import make_response_with_err, make_response_with_data
from back_skeep.store.users import get_user_by_login
from back_skeep.utils import new_jwt


class Auth(Resource):
    def get(self):
        req = request.json
        if req is None:
            return make_response_with_err(0, 'Запрос не верен')

        users = get_user_by_login(req.get('email', ''), req.get('password', ''))

        if len(users) == 0:
            return make_response_with_err(0, 'Логин, или пароль не верны')

        users[0].token = new_jwt(users[0])

        return make_response_with_data(users[0].to_dict())
