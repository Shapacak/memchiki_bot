CREATE TABLE IF NOT EXISTS mems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            img TEXT,
            name TEXT,
            tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE);


CREATE TABLE IF NOT EXISTS tags (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             tag_name TEXT UNIQUE);

