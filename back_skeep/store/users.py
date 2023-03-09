import sqlite3

from back_skeep.models.user import User, user_from_select
from back_skeep.store.db import get_db

select_users_query = """
SELECT id,
       email,
       date_create,
       is_admin
FROM users
ORDER BY date_create DESC;
"""
select_user_by_id_query = """
SELECT id,
       email,
       date_create,
       is_admin
FROM users
WHERE id = ?;
"""
select_user_by_login_query = """
SELECT id,
       email,
       date_create,
       is_admin
FROM users
WHERE email = ?
  AND password = ?;
"""
delete_user_by_id_query = """
DELETE
FROM users
WHERE id = ?;
"""
insert_user_query = """
INSERT INTO users(email, password)
VALUES (?, ?)
RETURNING id;
"""


def get_users() -> list[User]:
    db = get_db()
    users: list[User] = list()
    try:
        cur = db.execute(select_users_query)
        for user in cur:
            users.append(user_from_select(*user))
    except sqlite3.Error as err:
        print(err)

    db.commit()
    return users


def get_user_by_id(user_id) -> list[User]:
    db = get_db()
    users = list()
    try:
        cur = db.execute(select_user_by_id_query, (user_id,))
        for user in cur:
            users.append(user_from_select(*user))
    except sqlite3.Error as err:
        print(err)

    db.commit()
    return users


def get_user_by_login(user_login, user_pass) -> list[User]:
    db = get_db()
    users = list()
    try:
        cur = db.execute(select_user_by_login_query, (user_login, user_pass))
        for user in cur:
            users.append(user_from_select(*user))
    except sqlite3.Error as err:
        print(err)

    db.commit()
    return users


def delete_user_by_id(user_id):
    db = get_db()
    try:
        db.execute(delete_user_by_id_query, (user_id,))
    except sqlite3.Error as err:
        print(err)

    db.commit()


def add_new_user(user_email, user_password):
    db = get_db()
    users_id = list()
    try:
        cur = db.execute(insert_user_query, (user_email, user_password))
        for user in cur:
            users_id.append(user[0])
    except sqlite3.Error as err:
        print(err)

    db.commit()
    return users_id
