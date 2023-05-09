CREATE TABLE if not exists users(
    user_name VARCHAR(50) NOT NULL,
    user_password VARCHAR(50) NOT NULL
);


DROP TABLE if EXISTS products;
CREATE TABLE products(
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    product_image VARCHAR(200) NOT NULL
);


DROP TABLE if EXISTS stores;
CREATE TABLE stores(
    store_name VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    product_price VARCHAR(50) NOT NULL
);


DROP TABLE if EXISTS cart;
CREATE TABLE cart(
    user_name VARCHAR(50),
    product_id VARCHAR(50),
    quantity varchar(50)
);


