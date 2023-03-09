def make_response_with_data(data):
    return {
        'ok': True,
        'err_code': 0,
        'description': '',
        'data': data
    }


def make_response_with_err(err_code, description):
    return {
        'ok': False,
        'err_code': err_code,
        'description': description,
        'data': None
    }
