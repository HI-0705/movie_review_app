CREATE TABLE IF NOT EXISTS base_entity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reviews (
    base_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    review TEXT,
    rating INTEGER,
    FOREIGN KEY (base_id) REFERENCES base_entity(id)
);

CREATE TABLE IF NOT EXISTS watchlist (
    base_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    FOREIGN KEY (base_id) REFERENCES base_entity(id)
);

CREATE TABLE IF NOT EXISTS subscriptions (
    base_id INTEGER PRIMARY KEY,
    provider_id INTEGER NOT NULL UNIQUE,
    provider_name TEXT NOT NULL,
    FOREIGN KEY (base_id) REFERENCES base_entity(id)
);

CREATE TABLE IF NOT EXISTS movie_stills (
    base_id INTEGER PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    still_url TEXT NOT NULL,
    FOREIGN KEY (base_id) REFERENCES base_entity(id)
);
