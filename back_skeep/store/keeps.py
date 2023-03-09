import sqlite3

from back_skeep.models.keep import Keep, keep_from_select
from back_skeep.store.db import get_db

select_keeps_query = """
SELECT id,
       title
FROM keeps
WHERE user_id = ?
ORDER BY date_create DESC;
"""
select_keep_by_id_query = """
SELECT id,
       title
FROM keeps
WHERE id = ?;
"""
delete_keep_by_id_query = """
DELETE
FROM keeps
WHERE id = ?
RETURNING id;
"""
insert_keep_query = """
INSERT INTO keeps(title, user_id)
VALUES (?, ?)
RETURNING id;
"""


def get_keeps(user_id: int) -> list[Keep]:
    db = get_db()
    keeps: list[Keep] = list()
    try:
        cur = db.execute(select_keeps_query, (user_id,))
        for keep in cur:
            keeps.append(keep_from_select(*keep))
    except sqlite3.Error as err:
        print(err)

    db.commit()
    return keeps


def get_keep_by_id(keep_id):
    db = get_db()
    keeps: list[Keep] = list()
    try:
        cur = db.execute(select_keep_by_id_query, (keep_id,))
        for keep in cur:
            keeps.append(keep_from_select(*keep))
    except sqlite3.Error as err:
        print(err)

    db.commit()
    return keeps


def delete_keep_by_id(keep_id):
    db = get_db()
    keeps_id = list()
    try:
        cur = db.execute(delete_keep_by_id_query, (keep_id,))
        for keep in cur:
            keeps_id.append(keep[0])
    except sqlite3.Error as err:
        print(err)

    db.commit()
    return keeps_id


def add_new_keep(user_id, title):
    db = get_db()
    keeps_id = list()
    try:
        cur = db.execute(insert_keep_query, (title, user_id))
        for keep in cur:
            keeps_id.append(keep[0])
    except sqlite3.Error as err:
        print(err)

    db.commit()
    return keeps_id
