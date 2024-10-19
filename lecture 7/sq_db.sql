CREATE TABLE IF NOT EXISTS main_menu (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT  NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT  NULL,
    text text NOT NULL,
    time integer NOT NULL
);