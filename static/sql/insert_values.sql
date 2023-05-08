delete from products;
insert into products (product_id, product_name, stores)
values ('1', 'product_1', '123'),
		('2', 'product_2', '123'),
		('3', 'product_3', '123');


delete from stores;
insert into stores (store_id ,store_name, product_id, product_price ,store_url)
values ('1', 'store_1', '1',  '5.0', ''),
        ('2', 'store_2', '1',  '4.0', ''),
        ('3', 'store_3', '1', '7.0', ''),
        ('4', 'store_4', '1', '7.0', ''),
        ('1', 'store_1', '2', '4.5', ''),
        ('2', 'store_2', '2',  '5.0', ''),
        ('3', 'store_3', '2',  '6.0', ''),
        ('4', 'store_4', '2',  '3.5', ''),
        ('1', 'store_1', '3', '5.0', ''),
        ('2', 'store_2', '3', '5.0', ''),
        ('3', 'store_3', '3', '5.0', ''),
        ('4', 'store_4', '3', '1.0', '');


