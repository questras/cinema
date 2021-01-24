DROP TABLE IF EXISTS hall;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS order;
DROP TABLE IF EXISTS showing;
DROP TABLE IF EXISTS user;


CREATE TABLE hall (
    number int  NOT NULL PRIMARY KEY,
    places int  NOT NULL CHECK (places >= 0 AND places <= 400)
);

CREATE TABLE movie (
    id int  NOT NULL PRIMARY KEY,
    title varchar(256)  NOT NULL,
    director varchar(256)  NOT NULL,
    year_of_production int  NOT NULL CHECK (year_of_production >= 1888 AND year_of_production < 3000),
    type varchar(80)  NOT NULL,
    duration_in_minutes int  NOT NULL CHECK (duration_in_minutes >= 0 AND duration_in_minutes <= 600),
    description text  NOT NULL
);

CREATE TABLE showing (
    uuid uuid  NOT NULL PRIMARY KEY,
    "when" timestamp  NOT NULL,
    movie int  NOT NULL REFERENCES movie,
    hall int  NOT NULL REFERENCES hall
);

CREATE TABLE "user" (
    id int  NOT NULL PRIMARY KEY,
    email varchar(256)  NOT NULL UNIQUE,
    first_name varchar(256)  NOT NULL,
    last_name varchar(256)  NOT NULL,
    is_cashier boolean  NOT NULL,
    is_staff boolean  NOT NULL
);

CREATE TABLE "order" (
    uuid uuid  NOT NULL PRIMARY KEY,
    date timestamp  NOT NULL,
    tickets_amount int  NOT NULL CHECK (tickets_amount >= 1),
    accepted boolean  NOT NULL,
    showing uuid  NOT NULL REFERENCES showing,
    client int  NOT NULL REFERENCES "user",
    cashier_who_accepted int  NULL REFERENCES "user"
);
