CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, password TEXT, address TEXT, paymethod TEXT, admin BOOLEAN);
CREATE TABLE restaurants (id SERIAL PRIMARY KEY, name TEXT, area TEXT, views INTEGER);
CREATE TABLE menu (id SERIAL PRIMARY KEY, food TEXT, price INTEGER, res_id INTEGER REFERENCES restaurants);
CREATE TABLE orders (id SERIAL PRIMARY KEY, pricesum INTEGER, res_id INTEGER REFERENCES restaurants, address TEXT, paymethod TEXT, extras TEXT, user_id INTEGER REFERENCES users);
CREATE TABLE order_menu (id SERIAL PRIMARY KEY, food_id INTEGER REFERENCES menu, x INTEGER, order_id INTEGER REFERENCES orders);
CREATE TABLE reviews (id SERIAL PRIMARY KEY, stars INTEGER, content TEXT, user_id INTEGER REFERENCES users, res_id INTEGER REFERENCES restaurants);


INSERT INTO restaurants (name, area, views) VALUES ('Pizzeria', 'Helsinki', 1);

INSERT INTO restaurants (name, area, views) VALUES ('Grilli', 'Turku', 1);
INSERT INTO menu (food, price, res_id) VALUES ('Americano', 7, 1)

INSERT INTO menu (food, price, res_id) VALUES ('Quattro Stagione', 9, 1)

INSERT INTO menu (food, price, res_id) VALUES ('Hawaii', 8, 1)

INSERT INTO menu (food, price, res_id) VALUES ('Kebab ranskalaisilla', 8, 2)

INSERT INTO menu (food, price, res_id) VALUES ('Juustohampurilainen', 4, 2)

INSERT INTO menu (food, price, res_id) VALUES ('Kanapihvi', 12, 2)

