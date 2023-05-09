delete from products;
insert into products (product_id, product_name)
values ('1', 'product_1'),
		('2', 'product_2'),
		('3', 'product_3');


delete from stores;
insert into stores (store_name, product_id, product_price)
values ( 'store_1', '1',  '5.0'),
        ('store_2', '1',  '4.0'),
        ('store_3', '1', '7.0'),
        ('store_4', '1', '7.0'),
        ('store_1', '2', '4.5'),
        ('store_2', '2',  '5.0'),
        ('store_3', '2',  '6.0'),
        ('store_4', '2',  '3.5'),
        ('store_1', '3', '5.0'),
        ('store_2', '3', '5.0'),
        ('store_3', '3', '5.0'),
        ('store_4', '3', '1.0');


