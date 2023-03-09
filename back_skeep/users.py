from flask_restful import Resource
from flask import request

from back_skeep.models.response import make_response_with_data, make_response_with_err
from back_skeep.store.users import get_users, get_user_by_id, delete_user_by_id, add_new_user
from back_skeep.utils import auth_admin_check, new_jwt


class UserList(Resource):
    method_decorators = {'get': [auth_admin_check]}

    def get(self):
        users = get_users()
        res_users = list()

        for user in users:
            res_users.append(user.to_dict())

        return make_response_with_data(res_users)

    def post(self):
        req = request.json
        if req is None:
            return make_response_with_err(0, 'Запрос не верен')

        users_id = add_new_user(req.get('email', ''), req.get('password', ''))

        if len(users_id) == 0:
            return make_response_with_err(0, 'Не удалось добавить пользователя')

        new_user = get_user_by_id(users_id[0])[0]
        new_user.token = new_jwt(new_user)

        return make_response_with_data(new_user.to_dict())


class User(Resource):
    method_decorators = [auth_admin_check]

    def get(self, user_id):
        users = get_user_by_id(user_id)

        if len(users) == 0:
            return make_response_with_err(0, 'Пользователь не найден')

        return make_response_with_data(users[0].to_dict())

    def delete(self, user_id):
        delete_user_by_id(user_id)
        return make_response_with_data(user_id)
