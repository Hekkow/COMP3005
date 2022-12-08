DROP TABLE IF EXISTS publishers, books, users, sales, orders CASCADE;
CREATE TABLE IF NOT EXISTS publishers
(
	publisher VARCHAR(100) PRIMARY KEY,
	address VARCHAR(100) NOT NULL,
	emailaddress VARCHAR(100) NOT NULL,
	phonenumber INT NOT NULL
);
CREATE TABLE IF NOT EXISTS books
(
    ISBN INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
	author VARCHAR(100)[] NOT NULL,
    genre VARCHAR(100)[] NOT NULL,
    pages INT NOT NULL,
    price NUMERIC(6, 2) NOT NULL,
    quantity INT NOT NULL,
	publisher VARCHAR(100) NOT NULL REFERENCES publishers (publisher),
	cut NUMERIC(5, 2) NOT NULL
);
CREATE TABLE IF NOT EXISTS users
(
	userid SERIAL PRIMARY KEY,
	username VARCHAR(100) NOT NULL,
	pass VARCHAR(100) NOT NULL,
	cardnumber INT NOT NULL,
	address VARCHAR(100) NOT NULL,
	isAdmin BOOLEAN NOT NULL,
	cart INT[] NOT NULL
);
CREATE TABLE IF NOT EXISTS orders
(
	ordernumber SERIAL PRIMARY KEY,
	cardnumber INT NOT NULL,
	address VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS sales
(
	ISBN INT NOT NULL,
	price NUMERIC(10, 2) NOT NULL,
	cut NUMERIC(10, 2) NOT NULL
);

ALTER TABLE users ALTER COLUMN cart SET DEFAULT '{}';
INSERT INTO publishers VALUES ('penguin', 'ur moms house haha', 'im@urmoms.house', 61313131);
INSERT INTO publishers VALUES ('not penguin', 'ur moms house haha', 'im@urmoms.house', 61313131);
INSERT INTO publishers VALUES ('bear', 'ur moms house haha', 'im@urmoms.house', 61313131);
INSERT INTO publishers VALUES ('lion', 'ur moms house haha', 'im@urmoms.house', 61313131);
INSERT INTO publishers VALUES ('hippo', 'ur moms house haha', 'im@urmoms.house', 61313131);
INSERT INTO publishers VALUES ('lizard', 'ur moms house haha', 'im@urmoms.house', 61313131);
INSERT INTO publishers VALUES ('butterlfy', 'ur moms house haha', 'im@urmoms.house', 61313131);
INSERT INTO publishers VALUES ('blue walhe', 'ur moms house haha', 'im@urmoms.house', 61313131);
INSERT INTO publishers VALUES ('killer shark', 'ur moms house haha', 'im@urmoms.house', 61313131);
INSERT INTO publishers VALUES ('jelyfish', 'ur moms house haha', 'im@urmoms.house', 61313131);

INSERT INTO books VALUES (123123, 'harweh potah', '{"ron wesles", "jeffry"}', '{"magical"}', 2312, 752.24, 5, 'penguin', 12);
INSERT INTO books VALUES (435486, 'the clok work sparow', '{"ron wesles"}', '{"magical", "historically"}', 213, 234.68, 9, 'not penguin', 32);
INSERT INTO books VALUES (182347, 'tale 2 suties', '{"ron wesles"}', '{"historically"}', 324, 234.54, 9, 'bear', 15);
INSERT INTO books VALUES (591982, 'lil prince', '{"ron wesles"}', '{"magical"}', 579, 976.59, 9, 'lion', 31);
INSERT INTO books VALUES (452373, 'n then aint non', '{"ron wesles"}', '{"historically"}', 753, 45.45, 9, 'hippo', 21);
INSERT INTO books VALUES (786371, 'hobbite', '{"jrr martinez"}', '{"magical"}', 42, 35.20, 9, 'lizard', 5);
INSERT INTO books VALUES (453783, 'barnia', '{"jrr martinez"}', '{"historically"}', 752, 34.35, 9, 'butterlfy', 7);
INSERT INTO books VALUES (373973, 'da vinc', '{"jrr martinez", "ron wesles"}', '{"magical"}', 152, 24.45, 9, 'blue walhe', 12);
INSERT INTO books VALUES (273979, 'charolotty', '{"jrr martinez"}', '{"historically"}', 384, 968.87, 9, 'killer shark', 4);
INSERT INTO books VALUES (254378, 'mockinbirds', '{"jrr martinez"}', '{"magical"}', 547, 453.45, 9, 'jelyfish', 46);