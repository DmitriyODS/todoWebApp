import http
import json

import requests as requests

from front_skeep.models.request import RequestLogin

URL_SERVER = "http://127.0.0.1:8080"


def api_auth(request_login: RequestLogin) -> (bool, dict):
    url = f"{URL_SERVER}/auth"
    payload = json.dumps({
        "email": request_login.login,
        "password": request_login.password,
        "title": request_login.keep
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != http.HTTPStatus.OK:
        return False, None

    data = response.json()
    if data is None:
        return False, None

    return True, data


def api_register(request_login: RequestLogin) -> (bool, dict):
    url = f"{URL_SERVER}/users"
    payload = json.dumps({
        "email": request_login.login,
        "password": request_login.password,
        "title": request_login.keep
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != http.HTTPStatus.OK:
        return False, None

    data = response.json()
    if data is None:
        return False, None

    return True, data


def api_add_new_keep(user_id, token, title) -> (bool, dict):
    url = f"{URL_SERVER}/keeps"
    payload = json.dumps({
        "user_id": user_id,
        "token": token,
        "title": title
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != http.HTTPStatus.OK:
        return False, None

    data = response.json()
    if data is None:
        return False, None

    return True, data


def api_get_keeps(user_id, token) -> (bool, dict):
    url = f"{URL_SERVER}/keeps"
    payload = json.dumps({
        "user_id": user_id,
        "token": token,
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != http.HTTPStatus.OK:
        return False, None

    data = response.json()
    if data is None:
        return False, None

    return True, data


def api_del_keep(user_id, token, keep_id) -> (bool, dict):
    url = f"{URL_SERVER}/keeps/{keep_id}"
    payload = json.dumps({
        "user_id": user_id,
        "token": token,
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.request("DELETE", url, headers=headers, data=payload)
    if response.status_code != http.HTTPStatus.OK:
        return False, None

    data = response.json()
    if data is None:
        return False, None

    return True, data


def api_get_users(user_id, token) -> (bool, dict):
    url = f"{URL_SERVER}/users"
    payload = json.dumps({
        "user_id": user_id,
        "token": token,
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != http.HTTPStatus.OK:
        return False, None

    data = response.json()
    if data is None:
        return False, None

    return True, data


def api_del_user(user_id, token, user_del_id) -> (bool, dict):
    url = f"{URL_SERVER}/users/{user_del_id}"
    payload = json.dumps({
        "user_id": user_id,
        "token": token,
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.request("DELETE", url, headers=headers, data=payload)
    if response.status_code != http.HTTPStatus.OK:
        return False, None

    data = response.json()
    if data is None:
        return False, None

    return True, data
