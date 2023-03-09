import datetime
from dataclasses import dataclass


@dataclass
class User:
    id: int
    email: str
    date_create: datetime.datetime
    is_admin: bool
    token: str

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'date_create': self.date_create.strftime('%d-%m-%Y'),
            'is_admin': self.is_admin,
            'token': self.token
        }


def user_from_select(user_id, email, date_create_unix, is_admin):
    return User(
        id=user_id,
        email=email,
        date_create=datetime.datetime.fromtimestamp(date_create_unix),
        is_admin=bool(is_admin),
        token=''
    )
