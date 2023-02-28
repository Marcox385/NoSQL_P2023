-- IS727272 - Cordero Hernández, Marco Ricardo
-- Creación de keyspace inicial y cambio
CREATE KEYSPACE cassandra_lab2
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

-- Asegurar que no existen las tablas (medida adicional)
DROP TABLE accounts_by_user;
DROP TABLE possitions_by_account;
DROP TABLE trades_by_a_d;
DROP TABLE trades_by_a_td;
DROP TABLE trades_by_a_std;
DROP TABLE trades_by_a_sd;

-- Creación de tablas requeridas
CREATE TABLE IF NOT EXISTS accounts_by_user (
    username text,
    account_number varint,
    cash_balance double,
    name text,
    PRIMARY KEY ((username), account_number)
);

CREATE TABLE IF NOT EXISTS possitions_by_account (
    account varint,
    symbol text,
    quantity float,
    PRIMARY KEY ((account), symbol)
);

CREATE TABLE IF NOT EXISTS trades_by_a_d (
    account varint,
    trade_id date,
    type boolean,
    symbol text,
    shares text,
    price double,
    amount float,
    PRIMARY KEY ((account), trade_id)
);

CREATE TABLE IF NOT EXISTS trades_by_a_td (
    account varint,
    trade_id date,
    type boolean,
    symbol text,
    shares text,
    price double,
    amount float,
    PRIMARY KEY ((account), type, trade_id)
);

CREATE TABLE IF NOT EXISTS trades_by_a_std (
    account varint,
    trade_id date,
    type boolean,
    symbol text,
    shares text,
    price double,
    amount float,
    PRIMARY KEY ((account), symbol, type, trade_id)
);

CREATE TABLE IF NOT EXISTS trades_by_a_sd (
    account varint,
    trade_id date,
    type boolean,
    symbol text,
    shares text,
    price double,
    amount float,
    PRIMARY KEY ((account), symbol, trade_id)
);

-- Inserción de datos
-- accounts_by_user | text, varint, double, text
INSERT INTO accounts_by_user (username, account_number, cash_balance, name)
VALUES ('MarCordero', 410, 27532.45, 'Marco Cordero');

INSERT INTO accounts_by_user (username, account_number, cash_balance, name)
VALUES ('AdriD', 777, 60000.9, 'Adriana Díaz');

INSERT INTO accounts_by_user (username, account_number, cash_balance, name)
VALUES ('MarCordero', 430, 5000, 'MarContingence plan');

INSERT INTO accounts_by_user (username, account_number, cash_balance, name)
VALUES ('MFDOOM', 31102020, 1000000, 'Daniel Dumile');

-- positions_by_account | varint, text, float
INSERT INTO possitions_by_account (account, symbol, quantity)
VALUES (410, 'MRVL1', 2);

INSERT INTO possitions_by_account (account, symbol, quantity)
VALUES (410, 'SPOTN', 3.4);

INSERT INTO possitions_by_account (account, symbol, quantity)
VALUES (31102020, 'KMD', 100);

INSERT INTO possitions_by_account (account, symbol, quantity)
VALUES (777, 'ORCL', 13.12);

-- trades_by_a_* | varint, date, boolean, text, text, double, float
-- Para type -> boolean : 0 = compra, 1 = venta
INSERT INTO trades_by_a_d (account, trade_id, type, symbol, shares, price, amount)
VALUES (410, '2023-02-09', false, 'SPOTN', 'Stock', 500, 3.4);

INSERT INTO trades_by_a_d (account, trade_id, type, symbol, shares, price, amount)
VALUES (410, '2023-02-01', false, 'MRVL1', 'MF', 1000, 2);

INSERT INTO trades_by_a_d (account, trade_id, type, symbol, shares, price, amount)
VALUES (777, '2023-01-09', true, 'ORCL', 'ETF', 2500, 0.88);

INSERT INTO trades_by_a_d (account, trade_id, type, symbol, shares, price, amount)
VALUES (31102020, '2020-01-01', true, 'KMD', 'Stock', 8003, 64);

INSERT INTO trades_by_a_td (account, trade_id, type, symbol, shares, price, amount)
VALUES (410, '2023-02-09', false, 'SPOTN', 'Stock', 500, 3.4);

INSERT INTO trades_by_a_td (account, trade_id, type, symbol, shares, price, amount)
VALUES (410, '2023-02-01', false, 'MRVL1', 'MF', 1000, 2);

INSERT INTO trades_by_a_td (account, trade_id, type, symbol, shares, price, amount)
VALUES (777, '2023-01-09', true, 'ORCL', 'ETF', 2500, 0.88);

INSERT INTO trades_by_a_td (account, trade_id, type, symbol, shares, price, amount)
VALUES (31102020, '2020-01-01', true, 'KMD', 'Stock', 8003, 64);

INSERT INTO trades_by_a_std (account, trade_id, type, symbol, shares, price, amount)
VALUES (410, '2023-02-09', false, 'SPOTN', 'Stock', 500, 3.4);

INSERT INTO trades_by_a_std (account, trade_id, type, symbol, shares, price, amount)
VALUES (410, '2023-02-01', false, 'MRVL1', 'MF', 1000, 2);

INSERT INTO trades_by_a_std (account, trade_id, type, symbol, shares, price, amount)
VALUES (777, '2023-01-09', true, 'ORCL', 'ETF', 2500, 0.88);

INSERT INTO trades_by_a_std (account, trade_id, type, symbol, shares, price, amount)
VALUES (31102020, '2020-01-01', true, 'KMD', 'Stock', 8003, 64);

INSERT INTO trades_by_a_sd (account, trade_id, type, symbol, shares, price, amount)
VALUES (410, '2023-02-09', false, 'SPOTN', 'Stock', 500, 3.4);

INSERT INTO trades_by_a_sd (account, trade_id, type, symbol, shares, price, amount)
VALUES (410, '2023-02-01', false, 'MRVL1', 'MF', 1000, 2);

INSERT INTO trades_by_a_sd (account, trade_id, type, symbol, shares, price, amount)
VALUES (777, '2023-01-09', true, 'ORCL', 'ETF', 2500, 0.88);

INSERT INTO trades_by_a_sd (account, trade_id, type, symbol, shares, price, amount)
VALUES (31102020, '2020-01-01', true, 'KMD', 'Stock', 8003, 64);

-- Queries
-- Q1. Consulta de cuentas de un usuario
SELECT name, account_number, cash_balance
FROM accounts_by_user
WHERE username = 'MarCordero';

-- Q2. Encontrar todas las posiciones en una cuenta, ordenar por símbolo (ASC)
SELECT symbol, quantity
FROM possitions_by_account
WHERE account = 410
ORDER BY symbol ASC;

/* Q3. Encontrar todas las transacciones de una cuenta (rango de fechas opcional),
*  tipo de transacción, símbolo; ordenar por fecha de transacción (DESC) */
SELECT trade_id, account, type, symbol
FROM trades_by_a_d
WHERE account = 410 AND trade_id < '2023-03-01' AND trade_id > '2023-01-01'
ORDER BY trade_id DESC;

-- Q3.1 Encontrar todas las transacciones de una cuenta; ordenar por fecha
SELECT trade_id, account, type, symbol
FROM trades_by_a_d
WHERE account = 410
ORDER BY trade_id;

/* Q3.2 Encontrar todas las transacciones de una cuenta y utilizar un rango de
*  fecha; ordenar por fecha */
SELECT trade_id, account, type, symbol
FROM trades_by_a_d
WHERE account = 410 AND trade_id < '2023-03-01' AND trade_id > '2023-02-08'
ORDER BY trade_id;

/* Q3.3 Encontrar todas las transacciones de una cuenta en un rango de fechas,
*  y tipo de transacción; ordenar por fecha */
SELECT trade_id, account, type, symbol
FROM trades_by_a_td
WHERE account = 410 AND type = false
AND trade_id < '2023-02-04' AND trade_id > '2023-01-01'
ORDER BY trade_id;

/* Q3.4 Encontrar todas las transacciones de una cuenta en un rango de fechas,
*  tipo de transacción y símbolo de instrumento; ordenar por fecha */
SELECT trade_id, account, type, symbol
FROM trades_by_a_std
WHERE account = 777 AND type = true AND symbol = 'ORCL'
AND trade_id < '2023-01-31' AND trade_id > '2023-01-01'
ORDER BY trade_id;

/* Q3.5 Encontrar todas las transacciones de una cuenta en un rango de fechas
*  y símbolo de instrumento; ordenar por fecha */
SELECT trade_id, account, type, symbol
FROM trades_by_a_sd
WHERE account = 31102020 AND symbol = 'KMD'
AND trade_id < '2020-10-31' AND trade_id > '1971-07-13'
ORDER BY trade_id;

-- UPDATE
UPDATE accounts_by_user SET cash_balance = 385
WHERE username = 'MarCordero' and account_number = 410;
SELECT * FROM accounts_by_user;

UPDATE possitions_by_account SET quantity = 3.14
WHERE account = 410 and symbol = 'SPOTN';
SELECT * FROM possitions_by_account;

UPDATE accounts_by_user SET name = 'King Geedorah'
WHERE username = 'MFDOOM' and account_number = 31102020;
SELECT * FROM accounts_by_user;

-- DELETE
DELETE name FROM accounts_by_user
WHERE username = 'MarCordero' AND account_number = 430;
SELECT * FROM accounts_by_user;

DELETE quantity FROM possitions_by_account
WHERE account = 410 and symbol = 'SPOTN';
SELECT * FROM possitions_by_account;

DELETE cash_balance FROM accounts_by_user
WHERE username = 'MFDOOM' AND account_number = 31102020;
SELECT * FROM accounts_by_user;