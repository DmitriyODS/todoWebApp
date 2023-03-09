import dataclasses
import datetime

from front_skeep.models.keep import Keep


@dataclasses.dataclass
class RequestLogin:
    login: str
    password: str
    keep: str
    is_register: bool


def get_request_data_from_dict_login(data: dict[str: str]):
    return RequestLogin(login=data.get('login', ''),
                        password=data.get('password', ''),
                        keep=data.get('keep', ''),
                        is_register=data.get('is_register', ''))


def get_request_data_from_dict_keep(data: dict[str: str]):
    return Keep(title=data.get('keep_text', ''),
                keep_id=0)
