DROP TABLE if EXISTS buyers;
CREATE TABLE buyers(
    buyer_id VARCHAR(50) PRIMARY KEY,
    buyer_name VARCHAR(50) NOT NULL,
    buyer_password VARCHAR(50) NOT NULL
);

DROP TABLE if EXISTS products;
CREATE TABLE products(
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    stores VARCHAR(300) NOT NULL
);


DROP TABLE if EXISTS stores;
CREATE TABLE  stores(
    store_id VARCHAR(50) NOT NULL,
    store_name VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    product_price VARCHAR(50),
    store_url varchar(50)
);


DROP TABLE if EXISTS cart;
CREATE TABLE cart(
    buyer_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity varchar(50)
);


