select
    pt.name as pizza_name
    , p.size as pizza_size
    , round(cast(count(od.quantity) * p.price as numeric), 2) as total
    , count(od.quantity) as quantity
from pizzas.pizzas p
join pizzas.pizza_types pt on p.pizza_type_id = pt.pizza_type_id
join pizzas.order_details od on p.pizza_id = od.pizza_id
group by 
    pt.name
    , p.size
    , p.price
order by
    total desc;

select
    o.date as date
    , count(od.quantity) as quantity
from pizzas.order_details od
join pizzas.orders o on od.order_id = o.order_id
group by o.date
order by o.date;

select
    pt.name
    , p.price as price
    , count(od.quantity) as quantity
from pizzas.pizza_types pt
join pizzas.pizzas p on pt.pizza_type_id = p.pizza_type_id
join pizzas.order_details od on p.pizza_id = od.pizza_id
group by
    pt.name, p.price
order by quantity desc;

select * 
from pizzas.pizzas;

select * 
from pizzas.pizza_types;

select * 
from pizzas.orders;

select * 
from pizzas.order_details;