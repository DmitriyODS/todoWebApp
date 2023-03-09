import http

from flask import (
    Blueprint, render_template, request, session, url_for, redirect
)

from front_skeep.api_client import api_get_keeps, api_add_new_keep, api_del_keep
from front_skeep.models.keep import Keep
from front_skeep.models.request import get_request_data_from_dict_keep
from front_skeep.models.response import make_err_response, make_response_ok
from front_skeep.utils import check_auth

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET'])
@check_auth
def promo_handler():
    user_email = session.get('email', '')
    ok, data = api_get_keeps(session.get('user_id', 0), session.get('token', ''))
    err_info = ''

    if not ok:
        err_info = 'Ошибка связи с сервером, попробуйте ещё раз позже'
        return render_template('home.html', user_email=user_email, keeps_lst=[], err_info=err_info)

    if not data['ok']:
        if data['err_code'] == 401:
            session.clear()
            return redirect('/promo', 302)

        err_info = data['description']
        return render_template('home.html', user_email=user_email, keeps_lst=[], err_info=err_info)

    keeps_lst: [Keep] = []
    for keep in data['data']:
        keeps_lst.append(Keep(keep_id=keep['id'], title=keep['title']))

    return render_template('home.html', user_email=user_email, keeps_lst=keeps_lst, err_info=err_info)


@bp.route('/addNewKeep', methods=['POST'])
@check_auth
def add_new_keep():
    if request.method != 'POST':
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Вызываемый метод не соответствует: POST')

    res = request.json
    if res is None:
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Тело запроса пусто')

    res_keep = get_request_data_from_dict_keep(res)
    ok, data = api_add_new_keep(session.get('user_id', 0), session.get('token', ''), res_keep.title)
    if not ok:
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Ошибка сервера, попробуйте ещё раз позже')
    if not data['ok']:
        return make_err_response(http.HTTPStatus.BAD_REQUEST, data['description'])

    return make_response_ok()


@bp.route('/delKeep:<keep_id>', methods=['DELETE'])
@check_auth
def del_keep(keep_id):
    if request.method != 'DELETE':
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Вызываемый метод не соответствует: DELETE')

    ok, data = api_del_keep(session.get('user_id', 0), session.get('token', ''), keep_id)
    if not ok:
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Ошибка сервера, попробуйте ещё раз позже')
    if not data['ok']:
        return make_err_response(http.HTTPStatus.BAD_REQUEST, data['description'])

    return make_response_ok()
