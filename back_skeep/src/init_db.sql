BEGIN;

CREATE TABLE IF NOT EXISTS users
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    email       TEXT UNIQUE NOT NULL,
    password    TEXT        NOT NULL,
    date_create INTEGER     NOT NULL DEFAULT (CAST(strftime('%s', 'now') as INTEGER)),
    is_admin    INTEGER     NOT NULL DEFAULT 0 CHECK ( is_admin >= 0 and is_admin < 2 )
);

INSERT INTO users(id, email, password, is_admin)
VALUES (1, 'admin', 'admin', 1)
ON CONFLICT (id) DO UPDATE SET id=excluded.id,
                               email=excluded.email,
                               password=excluded.password,
                               is_admin=excluded.is_admin;

UPDATE sqlite_sequence
SET seq = (SELECT MAX(id) FROM users)
WHERE name = 'users';

CREATE TABLE IF NOT EXISTS keeps
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    date_create INTEGER NOT NULL DEFAULT (CAST(strftime('%s', 'now') as INTEGER)),
    user_id     INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
);

COMMIT;