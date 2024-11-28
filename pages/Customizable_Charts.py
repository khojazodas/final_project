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

#Функция для создания датафрейма который используется для линейного графика под названием "Amount of Sales per Date"  
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

#Загрузка данных для дальнейшего использования
inv = load_data()
inv1 = load_data1()

#Заголовок страницы
st.write('## Customizable Charts📊')

#Создание фильтра для гистограммы
pizza_filter = st.selectbox(
    'Select the Pizza Type',
    options=inv['pizza_name']
)
filtered_pizza = inv[inv['pizza_name'] == pizza_filter]

#Гистограмма - Total Sales of Pizza by Size с наличием фильтра
fig = px.bar(
    data_frame=filtered_pizza,
    x='pizza_size',
    y='total',
    title='Total Sales of Pizza by Size🍕',
    labels={'total': 'Total Sales', 'pizza_size': 'Size of Pizza'}
)
st.plotly_chart(fig)

#Создание фильтра для линейного графика
date_filter_min = st.date_input(
    label='Select a Start-Date📅',
    key='start_date',
    min_value=inv1['date'].min(),
    max_value=inv1['date'].max(),
    value=pd.to_datetime('2015-11-1')
)
date_filter_max = st.date_input(
    label='Select an End-Date📅',
    key='end_date',
    min_value=inv1['date'].min(),
    max_value=inv1['date'].max(),
    value=pd.to_datetime('2015-11-30')
)
filtered_date = inv1[
    (inv1['date'] >= date_filter_min) & (inv1['date'] <= date_filter_max)
]

#Линейный график - Amount of Sales per Date с наличием фильтра
fig1 = px.line(
    data_frame=filtered_date,
    x='date',
    y='quantity',
    title='Amount of Sales per Date📆',
    labels={'date': 'Date', 'quantity': 'Amount of Sales'}
)
st.plotly_chart(fig1)