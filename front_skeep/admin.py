import http

from flask import (
    Blueprint, redirect, render_template, request, session
)

from front_skeep.api_client import api_get_users, api_del_user
from front_skeep.models.response import make_err_response, make_response_ok
from front_skeep.models.user import User
from front_skeep.utils import check_auth

bp = Blueprint('admin', __name__)


@bp.route('/admin', methods=['GET'])
@check_auth
def admin():
    ok, data = api_get_users(session.get('user_id', 0), session.get('token', ''))
    err_info = ''

    if not ok:
        err_info = 'Ошибка связи с сервером, попробуйте ещё раз позже'
        return render_template('home.html', users_lst=[], err_info=err_info)

    if not data['ok']:
        if data['err_code'] == 401:
            session.clear()
            return redirect('/promo', 302)
        if data['err_code'] == 403:
            session.clear()
            return redirect('/', 302)

        err_info = data['description']
        return render_template('home.html', users_lst=[], err_info=err_info)

    users_lst: [User] = []
    for user in data['data']:
        # не будем показывать текущего пользователя, зачем?
        if user['id'] == session.get('user_id', 0):
            continue

        users_lst.append(User(user_id=user['id'],
                              email=user['email'],
                              date_create=user['date_create']))

    return render_template('admin.html', users_lst=users_lst, err_info=err_info)


@bp.route('/delUser:<user_id>', methods=['DELETE'])
@check_auth
def admin_del_user(user_id):
    if request.method != 'DELETE':
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Вызываемый метод не соответствует: DELETE')

    ok, data = api_del_user(session.get('user_id', 0), session.get('token', ''), user_id)
    if not ok:
        return make_err_response(http.HTTPStatus.BAD_REQUEST, 'Ошибка сервера, попробуйте ещё раз позже')
    if not data['ok']:
        return make_err_response(http.HTTPStatus.BAD_REQUEST, data['description'])

    return make_response_ok()
