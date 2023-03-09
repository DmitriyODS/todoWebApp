from dataclasses import dataclass


@dataclass
class Keep:
    id: int
    title: str

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title
        }


def keep_from_select(user_id, title):
    return Keep(
        id=user_id,
        title=title,
    )
