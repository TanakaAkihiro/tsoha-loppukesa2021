CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    topic TEXT,
    created_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    content TEXT,
    created_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE visits (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES threads,
    visited_at TIMESTAMP
);