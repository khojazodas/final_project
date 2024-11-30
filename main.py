import pandas as pd
import plotly.express as px
import streamlit as st
import duckdb

#Функция для создания датафрейма который используется для гистограммы под названием "Total Sales by Pizza Type"
@st.cache_data
def load_data():
    con = duckdb.connect('my.duckdb')
    query = """
    select
        pt.name as pizza_name
        , p.size as pizza_size
        , round(cast(count(od.quantity) * p.price as numeric), 2) as total
        , count(od.quantity) as quantity
    from pizzas p
    join pizza_types pt on p.pizza_type_id = pt.pizza_type_id
    join order_details od on p.pizza_id = od.pizza_id
    group by 
        pt.name
        , p.size
        , p.price
    order by
        total desc;
    """
    data = con.execute(query).fetchall()
    columns = ['pizza_name', 'pizza_size', 'total', 'quantity']
    df = pd.DataFrame(data, columns=columns)
    con.close()
    return df

#Функция для создания датафрейма который используется для линейного графика под названием "Amount of Sales by Date"
@st.cache_data
def load_data1():
    con = duckdb.connect('my.duckdb')
    query = """
    select
        o.date as date
        , count(od.quantity) as quantity
        from order_details od
        join orders o on od.order_id = o.order_id
        group by o.date
        order by o.date;
    """
    data = con.execute(query).fetchall()
    columns = ['date', 'quantity']
    df = pd.DataFrame(data, columns=columns)
    con.close()
    return df

#Функция для создания датафрейма который используется для гистограммы под названием "Amount of Pizzas Sold"
@st.cache_data
def load_data2():
    con = duckdb.connect('my.duckdb')
    query = """
    select
        pt.name as name
        , p.price as price
        , count(od.quantity) as quantity
    from pizza_types pt
    join pizzas p on pt.pizza_type_id = p.pizza_type_id
    join order_details od on p.pizza_id = od.pizza_id
    group by
        pt.name, p.price
    order by quantity desc;
    """
    data = con.execute(query).fetchall()
    columns = ['name', 'price', 'quantity']
    df = pd.DataFrame(data, columns=columns)
    con.close()
    return df
    
#Создание заголовка и загрузка кешированных данных
st.write('# Main Page')
inv = load_data()
inv1 = load_data1()
inv2 = load_data2()

st.write(inv) #Вывод данных для первой гистограммы
#Гистограмма - Total Sales by Pizza Type
fig = px.bar(
    data_frame=inv,
    x='pizza_name',
    y='total',
    hover_data={'quantity': True, 'pizza_size': True},
    title='Total Sales by Pizza Type',
    labels={'total': 'Total Sales', 'pizza_name': 'Pizza Type'}
)
st.plotly_chart(fig)


st.write(inv1) #Вывод данных для линейного графика
#Линейный График - Amount of Sales by Date
fig1 = px.line(
    data_frame=inv1,
    x='date',
    y='quantity',
    title='Amount of Sales by Date',
    labels={'date': 'Date', 'quantity': 'Amount of P'}
)
st.plotly_chart(fig1)

#Гистограмма - Amount of Pizzas Sold
fig2 = px.bar(
    data_frame=inv2,
    x='quantity',
    y='name',
    title='Amount of Pizzas Sold',
    labels={'name': 'Pizza Name', 'quantity': 'Sold Amount'},
    hover_data={'price': True}
)
st.plotly_chart(fig2)

#Круговая Диаграмма - Amount of Pizzas Sold by Size
fig3 = px.pie(
    data_frame=inv,
    names='pizza_size',
    values='quantity',
    title='Amount of Pizzas Sold by Size'
)
st.plotly_chart(fig3)
