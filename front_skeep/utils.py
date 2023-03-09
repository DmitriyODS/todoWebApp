from flask import session, redirect
from functools import wraps


def check_auth(handler):
    @wraps(handler)
    def checkers(*args, **kwargs):
        user_id = session.get('user_id', '')
        token = session.get('token', '')
        is_admin = session.get('is_admin', False)

        # достаточно проверить, что оно у нас есть, так как если
        # мы не имеем верного токена, сервер с АПИ нам это скажет
        # и не выполнит наш запрос
        if user_id == '' or token == '':
            return redirect('/promo', 302)

        if str(handler.__name__).startswith('admin'):
            if not is_admin:
                return redirect('/promo', 302)

        return handler(*args, **kwargs)

    return checkers
