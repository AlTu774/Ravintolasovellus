CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, password TEXT);
CREATE TABLE restaurants (id SERIAL PRIMARY KEY, name TEXT, area TEXT, views INTEGER);
CREATE TABLE menu (id SERIAL PRIMARY KEY, food TEXT, res_id INTEGER REFERENCES restaurants);
CREATE TABLE extras (id SERIAL PRIMARY KEY, menu_id INTEGER REFERENCES menu, extra TEXT);

INSERT INTO restaurants (name, area, views) VALUES ('Pizzeria', 'Helsinki', 1);

INSERT INTO restaurants (name, area, views) VALUES ('Grilli', 'Turku', 1);

