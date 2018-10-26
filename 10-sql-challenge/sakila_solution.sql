use sakila;

select *
from actor;

-- 1a -- 
select a.first_name, a.last_name
from actor a;

-- 1b -- 
 select concat(a.first_name, ",", a.last_name) as "Actor Name"
 from actor a;
 
-- 2a --
select a.actor_id, a.first_name, a.last_name
from actor a
where first_name = "Joe";
 
-- 2b -- 
select a.actor_id, a.first_name, a.last_name
from actor a
where a.last_name like "%gen%";

-- 2c -- 
select a.last_name,  a.first_name
from actor a
where a.last_name like "%li%"
order by a.last_name asc;

-- 2d -- 
select c.country_id, c.country
from country c
where c.country in ("Afghanistan", "Bangladesh", "China");

-- 3a -- 
-- alter table using the settings -- 
ALTER TABLE `sakila`.`actor` 
ADD COLUMN `description` BLOB NULL AFTER `last_update`;

-- 3b -- 
alter table actor 
drop column description;

-- 4a -- 
select a.last_name, count(a.last_name) as "Similar Last Name"
from actor a
group by a.last_name;

-- 4b -- 
select a.last_name, count(a.last_name) as "Similar Last Name"
from actor a
group by a.last_name
having count(a.last_name) >=2;

-- 4c -- 
update actor a
set a.first_name = "Harpo"
where a.last_name = "Groucho";

select *
from actor
where actor.last_name = "Williams";

-- 4d -- 
update actor a
set a.first_name = "Groucho"
where a.first_name = "Harpo";

-- 5a -- 
-- I think I made it appear using show create database address? -- 
select *
from staff;

-- 6a -- 
select s.first_name, s.last_name, ad.address
from staff s
inner join address ad
using(address_id);

-- 6b -- 
select s.first_name, s.last_name, count(s.last_update) as "Total Amount Rung Up", s.last_update
from staff s
inner join address ad
using(address_id)
group by s.address_id;

-- 6c -- 
select f.title as "Movie Name", count(distinct(fa.actor_id)) as "Number of Actors"
from film f
inner join film_actor fa
using(film_id)
group by fa.film_id;

-- 6d -- 
select f.title as "Movie Name", count(f.title) as "Number of Hunchback Impossible"
from film f
inner join inventory i
using(film_id)
where f.film_id =  
(
select f.film_id
from film f
where f.title = "Hunchback Impossible"
);

-- 6e --
select c.last_name, c.first_name, sum(p.amount) as "Total Payment"
from payment p
inner join customer c
using (customer_id)
group by p.customer_id
order by c.last_name;

-- 7a --
select *
from film f
where 
left(f.title, 1) = "Q" 
OR left (f.title, 1) = "K"
and f.language_id = 1;

-- 7b --
select a.first_name as "Actor First Name", a.last_name as "Actor Last Name"
from actor a
where a.actor_id in

(
select fa.actor_id
from film f
inner join film_actor fa
using(film_id)
where f.title = "Alone Trip"

);

-- 7c --
select c.first_name as "Customer's First Name", c.last_name as "Customer's Last Name", c.email as "Email Address"
from customer c
where c.address_id in 

(
select ad.address_id
from address ad
where ad.city_id in 

	(
	select city.city_id
	from city
	where city.country_id = 

		(
		select co.country_id
		from country co
		where co.country = "Canada"
		)
	)
)
;

-- 7d --
select f.title as "Family Movies"
from film f
where f.film_id in

(
	select fcat.film_id
	from film_category fcat
	where fcat.category_id = 
    
		(
		select cat.category_id
		from category cat
		where cat.name = "Family"
		)
	)
;

-- 7e --
select f.title as "Movie Name", f.rental_duration as "Rental Rate"
from film f
order by f.rental_duration desc;

-- 7f --
select cus.store_id as "Store ID", sum(p.amount) as "Total Sales"
from payment p
inner join customer cus
using (customer_id)
group by cus.store_id;

-- 7g --
select s.store_id as "Store ID", city.city as "City Name", c.country as "Country"
from store s
inner join address ad
using(address_id)
inner join city
using (city_id)
inner join country c
using(country_id);

-- 7h --
select cat.name as "Movie Categories", count(i.film_id) as "Total Movies Sold", fcat.category_id as "Category ID", sum(p.amount) as "Gross Revenue"
from category cat
inner join film_category fcat
using (category_id)
inner join inventory i
using (film_id)
inner join rental r
using(inventory_id)
inner join payment p
using (rental_id)
group by cat.name
order by count(i.film_id) desc
limit 5;

-- 8a -- 
create view top_five_genres as 
select cat.name as "Movie Categories", count(i.film_id) as "Total Movies Sold", fcat.category_id as "Category ID", sum(p.amount) as "Gross Revenue"
from category cat
inner join film_category fcat
using (category_id)
inner join inventory i
using (film_id)
inner join rental r
using(inventory_id)
inner join payment p
using (rental_id)
group by cat.name
order by count(i.film_id) desc
limit 5;

-- 8b --
-- Answer -- 
-- Refresh the schema and right click on the view to alter view and get the SQL script

-- 8c --
drop view top_five_genres;