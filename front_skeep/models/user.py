import dataclasses
import datetime


@dataclasses.dataclass
class User:
    user_id: int
    email: str
    date_create: datetime.datetime
