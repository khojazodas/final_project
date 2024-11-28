import duckdb
import pandas as pd

#Подключение к DuckDB
con = duckdb.connect('my.duckdb')

#Создание и добавление таблицы 'pizzas'
data = con.execute("""
    SELECT *
    FROM read_csv_auto('source/pizzas.csv')
""").fetchall()
columns = ['pizza_id', 'pizza_type_id', 'size', 'price']
df = pd.DataFrame(data, columns=columns)
con.execute("""
    CREATE TABLE IF NOT EXISTS pizzas AS
    SELECT * FROM df
""")

#Создание и добавление таблицы 'pizza_types'
data1 = con.execute("""
    SELECT *
    FROM read_csv_auto('source/pizza_types.csv')
""").fetchall()
columns1 = ['pizza_type_id', 'name', 'category', 'ingredients']
df1 = pd.DataFrame(data1, columns=columns1)
con.execute("""
    CREATE TABLE IF NOT EXISTS pizza_types AS
    SELECT * FROM df1
""")

#Создание и добавление таблицы 'orders'
data2 = con.execute("""
    SELECT *
    FROM read_csv_auto('source/orders.csv')
""").fetchall()
columns2 = ['order_id', 'date', 'time']
df2 = pd.DataFrame(data2, columns=columns2)
con.execute("""
    CREATE TABLE IF NOT EXISTS orders AS
    SELECT * FROM df2
""")

#Создание и добавление таблицы 'order_details'
data3 = con.execute("""
    SELECT *
    FROM read_csv_auto('source/order_details.csv')
""").fetchall()
columns3 = ['order_details_id', 'order_id', 'pizza_id', 'quantity']
df3 = pd.DataFrame(data3, columns=columns3)
con.execute("""
    CREATE TABLE IF NOT EXISTS order_details AS
    SELECT * FROM df3
""")

con.close()