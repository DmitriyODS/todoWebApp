from flask import request
from flask_restful import Resource

from back_skeep.models.response import make_response_with_err, make_response_with_data
from back_skeep.store.keeps import get_keeps, add_new_keep, delete_keep_by_id, get_keep_by_id
from back_skeep.utils import auth_user_check


class KeepList(Resource):
    method_decorators = [auth_user_check]

    def get(self):
        req = request.json
        if req is None:
            return make_response_with_err(0, 'Запрос не верен')

        keeps = get_keeps(req.get('user_id', 0))
        res_keeps = list()

        for keep in keeps:
            res_keeps.append(keep.to_dict())

        return make_response_with_data(res_keeps)

    def post(self):
        req = request.json
        if req is None:
            return make_response_with_err(0, 'Запрос не верен')

        keeps_id = add_new_keep(req.get('user_id', ''), req.get('title', ''))

        if len(keeps_id) == 0:
            return make_response_with_err(0, 'Не удалось добавить запись')

        return make_response_with_data(keeps_id[0])


class Keep(Resource):
    method_decorators = [auth_user_check]

    def get(self, keep_id):
        keeps = get_keep_by_id(keep_id)

        if len(keeps) == 0:
            return make_response_with_err(0, 'Запись не найдена')

        return make_response_with_data(keeps[0].to_dict())

    def delete(self, keep_id):
        delete_keep_by_id(keep_id)
        return make_response_with_data(keep_id)
