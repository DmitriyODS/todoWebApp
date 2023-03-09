import http

from flask import (
    Blueprint, redirect, render_template, request, session
)

from front_skeep.api_client import api_auth, api_register, api_add_new_keep
from front_skeep.models.request import get_request_data_from_dict_login
from front_skeep.models.response import make_response_login, make_err_response, make_response_ok

bp = Blueprint('promo', __name__)


@bp.route('/promo', methods=['GET'])
def promo_handler():
    user_id = session.get('user_id', '')
    token = session.get('token', '')
    if user_id != '' and token != '':
        return redirect('/', 302)

    return render_template('promo.html')


@bp.route('/promo/auth', methods=['POST'])
def auth():
    if request.method != 'POST':
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Вызываемый метод не соответствует: POST')

    res = request.json
    if res is None:
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Тело запроса пусто')

    res_login = get_request_data_from_dict_login(res)

    if res_login.is_register:
        ok, data = api_register(res_login)
    else:
        ok, data = api_auth(res_login)

    if not ok:
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Ошибка запроса')

    if not data.get('ok', False):
        return make_err_response(http.HTTPStatus.BAD_REQUEST, data.get('description', 'Ошибка входа'))

    user_id = data['data'].get('id', '')
    token = data['data'].get('token', '')
    is_admin = data['data'].get('is_admin', False)

    if res_login.keep != '':
        api_add_new_keep(user_id, token, res_login.keep)

    session['user_id'] = user_id
    session['token'] = token
    session['is_admin'] = is_admin
    session['email'] = res_login.login

    return make_response_login(user_id, token, res_login.login, is_admin)


@bp.route('/promo/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/promo', 302)
