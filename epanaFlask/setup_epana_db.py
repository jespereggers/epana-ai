import sqlite3


def create_tables():
    connection = sqlite3.connect('epana.db')
    cursor = connection.cursor()

    # Create tables
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS input_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        date REAL DEFAULT CURRENT_TIMESTAMP NOT NULL,
        size INTEGER,
        tokens INTEGER DEFAULT 0 NOT NULL,
        UNIQUE (owner_id, name)
    );

    CREATE TABLE IF NOT EXISTS models (
        id INTEGER PRIMARY KEY,
        owner_id INTEGER NOT NULL,
        model_id TEXT NOT NULL,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS finetuning_jobs (
        id TEXT PRIMARY KEY,
        owner_id INTEGER NOT NULL,
        input_file_name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS output_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        name TEXT NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (owner_id, name)
    );

    CREATE TABLE IF NOT EXISTS tiers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        tier VARCHAR(255) DEFAULT 'free' NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );

    INSERT INTO users (id, email, password_hash, tier)
    VALUES (1, 'felix.grenzing@gmail.com', 
            'scrypt:32768:8:1$nNsyMmoSmOsv4qDr$0d41a7b074bdeb6f3e7209f4bd3a54ac45a7d9c3a4df48e375e359d7ae21fae21e93d84c4943f7f1f726447e7f6a163b443ee4c0097ff8e410ccd169ab84942f', 
            'free');

    INSERT INTO users (id, email, password_hash, tier)
    VALUES (2, 'jesper.eggers@gmail.com', 
            'scrypt:32768:8:1$KwmdyvzwtBb069Qs$ab5270ccece3b366de7e8dc8c5929c4220c7a7071187030627a3bb3a59cd2650a33cdf25f10ff11a8881bfa38279860f20498904e102b3ba8f93e07870d9ef6a', 
            'free');

    INSERT INTO models (id, owner_id, model_id, name)
    VALUES (1, -1, 'ft:gpt-3.5-turbo-0613:personal::88BtAC5L', 'jesper_felix_chat (open to all)');

    INSERT INTO models (id, owner_id, model_id, name)
    VALUES (2, -1, 'ft:gpt-3.5-turbo-0613:personal::8D8XolsY', 'neues Modell (open to all)');

    INSERT INTO tiers (id, name, price)
    VALUES (1, 'free', 0);

    INSERT INTO tiers (id, name, price)
    VALUES (2, 'paid', 1000);
    ''')

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
