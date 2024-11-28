import pandas as pd
import streamlit as st
import duckdb

#Загрузка таблици 'pizzas'
@st.cache_data
def load_data():
    con = duckdb.connect('my.duckdb')
    query = """
    select *
    from pizzas;
    """
    data = con.execute(query).fetchall()
    columns = ['pizza_id', 'pizza_type_id', 'size', 'price']
    df = pd.DataFrame(data, columns=columns)
    con.close()
    return df

#Загрузка таблици 'pizza_types'
@st.cache_data
def load_data1():
    con = duckdb.connect('my.duckdb')
    query = """
    select *
    from pizza_types;
    """
    data = con.execute(query).fetchall()
    columns = ['pizza_type_id', 'name', 'category', 'ingredients']
    df = pd.DataFrame(data, columns=columns)
    con.close()
    return df

#Загрузка таблици 'orders'
@st.cache_data
def load_data2():
    con = duckdb.connect('my.duckdb')
    query = """
    select *
    from orders;
    """
    data = con.execute(query).fetchall()
    columns = ['order_id', 'date', 'time']
    df = pd.DataFrame(data, columns=columns)
    con.close()
    return df

#Загрузка таблици 'order_details'
@st.cache_data
def load_data3():
    con = duckdb.connect('my.duckdb')
    query = """
    select *
    from order_details;
    """
    data = con.execute(query).fetchall()
    columns = ['order_details_id', 'order_id', 'pizza_id', 'quantity']
    df = pd.DataFrame(data, columns=columns)
    con.close()
    return df

#Загрузка таблиц в Датафреймы
inv = load_data()
inv1 = load_data1()
inv2 = load_data2()
inv3 = load_data3()

#Заголовок Страницы
st.write('## Dataset Tables📃')

#Вывод таблиц
st.write("Pizzas' ingredients information")
st.write(inv1)
st.write("Pizzas' price and size information")
st.write(inv)

st.write('More order information and details')
col1, col2 = st.columns(2, gap='medium')
col1.write(inv2)
col2.write(inv3)