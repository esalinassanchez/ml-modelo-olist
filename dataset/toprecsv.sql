select * from public.olist_orders_dataset d

select distinct(seller_state) from public.olist_sellers_dataset d
	order by 1 desc
	where seller_city = '04482255'
	
	order by 1 asc

select seller_id, count(*) from public.olist_sellers_dataset d
	group by seller_id
	having count(*) > 1
	

select order_id, count(*) from public.olist_orders_dataset d
	group by order_id
	having count(*) > 1
	
select customer_id, count(*) from public.olist_orders_dataset d
	group by order_id
	having count(*) > 1
	
select customer_unique_id, count(*) from public.olist_customers_dataset d
	group by customer_unique_id
	having count(*) > 1

select product_category_name, count(*) from public.olist_products_dataset d
	group by product_id
	having count(*) > 1
	
select distinct(product_width_cm  ) from public.olist_products_dataset d
	order by 1 desc
	
select product_category_name_english, count(*) from public.product_category_name_translation pcnt 
	group by product_category_name_english
	having count(*) > 1
	where product_category_name = 'utilidades_domesticas'
	
	
select d.order_id, oi.order_item_id, d.customer_id, d.order_status , d.order_purchase_timestamp , d.order_approved_at , d.order_delivered_carrier_date , d.order_delivered_customer_date , d.order_estimated_delivery_date, 
		c.customer_city, c.customer_state  ,
		oi.order_item_id,
		oi.shipping_limit_date ,
		oi.price ,
		oi.freight_value ,
		s.seller_id, s.seller_city, s.seller_state,		
		p.product_id, p.product_category_name, t.product_category_name_english ,
		p.product_weight_g , p.product_length_cm, p.product_height_cm, p.product_width_cm
	from public.olist_orders_dataset d		
	left join public.olist_customers_dataset c on c.customer_id = d.customer_id
	join public.olist_order_items_dataset oi on oi.order_id = d.order_id
	join public.olist_sellers_dataset s on s.seller_id = oi.seller_id
	join public.olist_products_dataset p on p.product_id = oi.product_id
	join public.product_category_name_translation t on t.product_category_name = p.product_category_name
order by d.order_id, oi.order_item_id
	
--- aumentado campos>


select d.order_id, oi.order_item_id, d.customer_id, d.order_status , d.order_purchase_timestamp , d.order_approved_at , d.order_delivered_carrier_date , d.order_delivered_customer_date , d.order_estimated_delivery_date, 
		c.customer_unique_id , c.customer_zip_code_prefix , c.customer_city, c.customer_state  ,
		oi.shipping_limit_date ,
		oi.price ,
		oi.freight_value ,
		s.seller_id, s.seller_zip_code_prefix, s.seller_city, s.seller_state,		
		p.product_id, p.product_category_name,		
		p.product_weight_g , p.product_length_cm, p.product_height_cm, p.product_width_cm,		
		t.product_category_name_english,
		pay.payment_sequential, pay.payment_type , pay.payment_installments , pay.payment_value,
		rev.review_id, rev.review_score , rev.review_comment_title , rev.review_comment_message , rev.review_creation_date , rev.review_answer_timestamp  
	 into public.todo_pre
	from public.olist_orders_dataset d		
	left join public.olist_customers_dataset c on c.customer_id = d.customer_id
	join public.olist_order_items_dataset oi on oi.order_id = d.order_id
	join public.olist_sellers_dataset s on s.seller_id = oi.seller_id
	join public.olist_products_dataset p on p.product_id = oi.product_id
	join public.product_category_name_translation t on t.product_category_name = p.product_category_name
	join public.olist_order_payments_dataset pay on pay.order_id = oi.order_id  
	left join public.olist_order_reviews_dataset rev on rev.order_id = oi.order_id  
order by d.order_id, oi.order_item_id, pay.payment_sequential, rev.review_id  

	


select * from public.todo_pre tp 
	join olist_geolocation_dataset g on g.geolocation_zip_code_prefix = tp.customer_zip_code_prefix 


select distincT(ogd.geolocation_state)  from olist_geolocation_dataset ogd
select distinct  ogd.geolocation_city, ogd.geolocation_state  from olist_geolocation_dataset ogd 
order by 2
	

WITH numerados AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY ogd.geolocation_zip_code_prefix ORDER BY ogd.geolocation_state) AS rn
    FROM public.olist_geolocation_dataset ogd 
)
SELECT *
into public.geolocalizacion
FROM numerados
WHERE rn = 1;



create table public.geolocalizacion (
	id int not null primary key,
	geolocation_city varchar(100),
	geolocation_state varchar(100)	
)

insert into public.geolocalizacion(id, geolocation_city, geolocation_state )
select geolocation_zip_code_prefix, geolocation_city , geolocation_state   
	from olist_geolocation_dataset 
	
	
select tp.*, 
	gs.geolocation_zip_code_prefix as seller_geolocation_zip_code_prefix, gs.geolocation_city as seller_geolocation_city, gs.geolocation_state as seller_geolocation_state,
	gs.geolocation_lat  as seller_geolocation_lat, gs.geolocation_lng as seller_geolocation_lng,
	gc.geolocation_zip_code_prefix as customer_geolocation_zip_code_prefix, gc.geolocation_city as customer_geolocation_city, gc.geolocation_state as customer_geolocation_state,
	gc.geolocation_lat  as customer_geolocation_lat, gc.geolocation_lng as customer_geolocation_lng
	into public.to_csv
from public.todo_pre tp 
	left join public.geolocalizacion gs on gs.geolocation_zip_code_prefix = tp.seller_zip_code_prefix 
	left join public.geolocalizacion gc on gc.geolocation_zip_code_prefix = tp.customer_zip_code_prefix 