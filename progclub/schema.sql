DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS labs;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    points DEFAULT 0,
    numsolutions DEFAULT 0
);


CREATE TABLE labs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    output TEXT NOT NULL,
    created TEXT NOT NULL,
    numsolutions DEFAULT 0
);

CREATE TABLE submissions (
    author_id INTEGER NOT NULL,
    author_username TEXT NOT NULL,
    lab_id INTEGER NOT NULL,
    submitted TEXT NOT NULL
);