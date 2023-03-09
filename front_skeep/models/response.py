def make_err_response(code_err, description):
    return {
        "ok": False,
        "code_err": code_err,
        "description": description,
        "data": None
    }


def make_response_login(user_id, token, email, is_admin):
    return {
        "ok": True,
        "code_err": 0,
        "description": '',
        "data": {
            "user_id": user_id,
            "is_admin": is_admin
        }
    }


def make_response_ok():
    return {
        "ok": True,
        "code_err": 0,
        "description": '',
        "data": {}
    }
