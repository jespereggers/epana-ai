/*
 Setup:
        1. Click 'Configure data source'
        2. Press '+'
        3. Select 'SQLite'
        4. Enter 'epana' as the name
        5. Press the '+' button next to 'File' field and create a db file in the epanaFlask folder
        6. Press OK
        7. Run Current File
        8. Press the '+' at 'target data source' to add the newly created data source
 */

create table input_files
(
    id       integer                                   not null
        constraint input_files_pk
            primary key autoincrement,
    owner_id integer                                   not null,
    name     TEXT                                      not null,
    date     REAL            default CURRENT_TIMESTAMP not null,
    size     INTEGER,
    tokens   integer INTEGER default 0                 not null,
    constraint input_files_pk2
        unique (owner_id, name)
);

create table models
(
    id       integer not null
        primary key,
    owner_id integer not null,
    model_id TEXT    not null,
    name     TEXT    not null
        constraint models_pk
            unique
);

create table output_files
(
    id       integer not null
        constraint output_files_pk
            primary key autoincrement,
    owner_id integer not null,
    type     TEXT    not null,
    name     TEXT    not null,
    date     TEXT default CURRENT_TIMESTAMP,
    constraint output_files_pk2
        unique (owner_id, name)
);


create table tiers
(
    id    INTEGER not null
        constraint tiers_pk
            primary key autoincrement,
    name  TEXT    not null,
    price INTEGER default 0
);

create table users
(
    id            INTEGER
        primary key autoincrement,
    email         VARCHAR(255)                           not null
        unique,
    password_hash VARCHAR(255)                           not null,
    tier          VARCHAR(255) default 'free'            not null,
    created_at    TIMESTAMP    default CURRENT_TIMESTAMP not null
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


