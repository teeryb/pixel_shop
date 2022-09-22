import sqlite3
from tkinter import *
from tkinter import messagebox
import string
import math
from datetime import datetime

#python fun_insert.py
def connectDB():
    conn = sqlite3.connect('pixel.db')
    cursor = conn.cursor()
    return conn,cursor

def get_time_now():
    now = datetime.now()
    dt_date = now.strftime("%d/%m/%Y")
    dt_time = now.strftime("%H:%M")
    return dt_date, dt_time

def fetch_column(table_name=''):
    conn,cursor = connectDB()
    #ดึงชื่อ column เก็บไว้ column_in_database
    sql = "PRAGMA table_info("+table_name+")"
    cursor.execute(sql)
    result=cursor.fetchall()
    conn.commit()
    if len(result)>0:
        column_in_database = []
        for x in result:
            column_in_database.append(x[1])
    conn.close()
    return column_in_database
    

def searchID_in_DB(table_name='',value_id=''):
    conn,cursor = connectDB()
    #เอา id ที่รับเข้ามา ไปค้นหาในฐานข้อมูล แล้วเก็บไว้ที่ result
    sql = "select * from "+table_name+" where id= '"+value_id+"'"
    cursor.execute(sql)
    result=cursor.fetchall()
    conn.commit()
    conn.close()
    return result
    

def has_special(check):
    return len(set(string.punctuation).intersection(check)) > 0


def insert_db(table_name="",values=[]):

    if table_name != '':
        #ดึงชื่อ column เก็บไว้ column_in_database
        column_in_database = fetch_column(table_name=table_name)

        #เช็คว่า id 'อักษรพิเศษ' และ 'ช่องว่าง' และ 'ค่าว่าง'
        if not has_special(values[0]) and " " not in values[0] and values[0] != '':
        
            #เช็ค column ใน DB กับค่า values มีขนาดเท่ากันหรือป่าว?
            if len(column_in_database)==len(values):

                #เอา id ที่รับเข้ามา ไปค้นหาในฐานข้อมูล แล้วเก็บไว้ที่ result
                result = searchID_in_DB(table_name=table_name,value_id=values[0])

                #เช็ค result หากมี id ในฐานข้อมูล len(result) จะมีค่ามากกว่า 0
                if len(result)>0:
                    messagebox.showwarning(title='Alert',message='invalid id')
                else :
                    #แปลงชื่อคอลัม ex. ['a','b','c'] ให้เป็น a, b, c
                    str_column_in_database = ', '.join(column_in_database)

                    #แปลงค่า value จาก ex. ['a','b','c'] ให้เป็น 'a', 'b', 'c'
                    value_to_sql = ''
                    count_value = len(values)
                    for i,x in enumerate(values):
                        if i+1 == count_value:
                            value_to_sql = value_to_sql+"'"+str(x)+"'"
                        else:
                            value_to_sql = value_to_sql+"'"+str(x)+"', "

                    #เพิ่มข้อมูลไปยังฐานข้อมูล
                    conn,cursor=connectDB()
                    sql = "insert into "+table_name+"("+str_column_in_database+") values("+value_to_sql+")"
                    cursor.execute(sql)
                    messagebox.showinfo(title='Alert', message='insert success')
                    conn.commit()
                    conn.close()

            else :
                x = list(enumerate(column_in_database))
                y = list(enumerate(values))
                print(f'>>> column_in_database : size[{len(column_in_database)}] != values : size[{len(values)}]')
                print(f'>>> column_in_database : {x}')
                print(f'>>> values : {y}')
        else:
            messagebox.showwarning('Alert','Incorrect information entered')
    else:
        print('!!!Please enter a table name.')

def update_db(table_name="",values=[]):

    if table_name != '':
        #ดึงชื่อ column เก็บไว้ column_in_database
        column_in_database = fetch_column(table_name=table_name)

        #เช็คว่า id 'อักษรพิเศษ' และ 'ช่องว่าง' และ 'ค่าว่าง'
        if not has_special(values[0]) and " " not in values[0] and values[0] != '':
        
            #เช็ค column ใน DB กับค่า values มีขนาดเท่ากันหรือป่าว?
            if len(column_in_database)==len(values):

                #เอา id ที่รับเข้ามา ไปค้นหาในฐานข้อมูล แล้วเก็บไว้ที่ result
                result = searchID_in_DB(table_name=table_name,value_id=values[0])

                #เช็ค result หากมี id ในฐานข้อมูล len(result) จะมีค่ามากกว่า 0
                if len(result)>0:

                    #Ex. แปลงค่า value
                    #column = ['a','b','c']
                    #value = ['1','2','3']
                    #result = a='1', b='2', c='3'
                    
                    value_to_sql = ''
                    max_values = len(values)
                    for i,x in enumerate(values):
                        if i+1 == max_values:
                            value_to_sql = value_to_sql+(f"{column_in_database[i]}='{values[i]}'")
                        else:
                            value_to_sql = value_to_sql+(f"{column_in_database[i]}='{values[i]}', ")

                    #เพิ่มข้อมูลไปยังฐานข้อมูล
                    conn,cursor=connectDB()
                    sql = "update "+table_name+" set "+value_to_sql+" where "+column_in_database[0]+"='"+values[0]+"'"
                    cursor.execute(sql)
                    messagebox.showinfo(title='Alert', message='update success')
                    conn.commit()
                    conn.close()
                else :
                    messagebox.showwarning(title='Alert',message='This ID does not exist in the database.')
            else :
                x = list(enumerate(column_in_database))
                y = list(enumerate(values))
                print(f'>>> column_in_database : size[{len(column_in_database)}] != values : size[{len(values)}]')
                print(f'>>> column_in_database : {x}')
                print(f'>>> values : {y}')
        else:
            print('!!!ID is null')
    else:
        print('!!!Please enter a table name.')


def delete_db(table_name="",values=[]):

    if table_name != '':
        #ดึงชื่อ column เก็บไว้ column_in_database
        column_in_database = fetch_column(table_name=table_name)

        #เช็คว่า id 'อักษรพิเศษ' และ 'ช่องว่าง' และ 'ค่าว่าง'
        if not has_special(values[0]) and " " not in values[0] and values[0] != '':
        
            #เช็ค column ใน DB กับค่า values มีขนาดเท่ากันหรือป่าว?
            if len(column_in_database)==len(values):

                #เอา id ที่รับเข้ามา ไปค้นหาในฐานข้อมูล แล้วเก็บไว้ที่ result
                result = searchID_in_DB(table_name=table_name,value_id=values[0])

                #เช็ค result หากมี id ในฐานข้อมูล len(result) จะมีค่ามากกว่า 0
                if len(result)>0:
                    
                    #หาตำแหน่ง status
                    index_status=''
                    for i,x in enumerate(column_in_database):
                        if 'status' == x :
                            index_status = i

                    #เพิ่มข้อมูลไปยังฐานข้อมูล
                    conn,cursor=connectDB()
                    sql = f"update {table_name} set {column_in_database[index_status]}='Disable' where {column_in_database[0]} = '{values[0]}'"
                    cursor.execute(sql)
                    messagebox.showinfo(title='Alert', message='delete success')
                    conn.commit()
                    conn.close()
                else :
                    messagebox.showwarning(title='Alert',message='This ID does not exist in the database.')
            else :
                x = list(enumerate(column_in_database))
                y = list(enumerate(values))
                print(f'>>> column_in_database : size[{len(column_in_database)}] != values : size[{len(values)}]')
                print(f'>>> column_in_database : {x}')
                print(f'>>> values : {y}')

        else:
            print('!!!ID is null')
    else:
        print('!!!Please enter a table name.')

def get_product_list(status='Enable'):
    conn,cursor=connectDB()
    sql = f"select * from products where status='{status}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    product_list = []
    for product_db in result:
        product = {
            'id' : product_db[0],
            'name' : product_db[1],
            'cost' : product_db[2],
            'price' : product_db[3],
            'inventory' : product_db[4],
            'image' : product_db[5]
        }
        product_list.append(product)
    conn.commit()
    conn.close()
    return product_list

def place_order(data={}):
    conn,cursor=connectDB()
    date, time = get_time_now()
    # insert order summary
    sql = f'''
        insert into orders (sub_total, discount, tax, grand_total, cash, change, employee_id, date, time, status)
        values ({data['sub_total']}, {data['discount']}, {data['tax']}, {data['grand_total']}, {data['cash']}, {data['change']}, {data['employee_code']}, '{date}', '{time}', 'Completed')
    '''
    cursor.execute(sql)

    # get order id - ตัวที่เพิ่ง insert ไป
    sql = 'select last_insert_rowid()'
    cursor.execute(sql)
    result = cursor.fetchone()
    order_id = result[0]

    # insert order products
    for product in data['products']:
        sql = f'''
            insert into order_products (order_id, product_id, quantity, cost, unit_price, total_price)
            values ({order_id}, '{product["id"]}', {product["quantity"]}, {product["cost"]}, {product["price"]}, {product["total_price"]})
        '''
        cursor.execute(sql)

    # decrease products inventory
    for product in data['products']:
        sql = f'''
            update products
            set inventory = inventory - {product['quantity']}
            where id = {product['id']}
        '''
        cursor.execute(sql)

    conn.commit()
    conn.close()

def get_order_list(page=1,items_per_page=20,order_id='',status=''):
    conn,cursor=connectDB()
    where_list = ['true']
    if status != '':
        where_list.append(f'status = "{status}"')
    if order_id != '':
        where_list.append(f'id = {order_id}')

    # get order list
    sql = f'''
        select *
        from orders
        where {' and '.join(where_list)}
        order by id desc
        limit {items_per_page} offset {(page - 1) * items_per_page}
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    order_list = []
    for order_db in result:
        order = {
            'order_id' : order_db[0],
            'date' : order_db[1],
            'time' : order_db[2],
            'discount' : order_db[4],
            'tax' : order_db[5],
            'total' : order_db[6],
            'cash' : order_db[7],
            'change' : order_db[8],
            'employee_code' : order_db[9]
        }
        order_list.append(order)
    
    # get total page
    sql = f'''
        select count(*)
        from orders
        where {' and '.join(where_list)}
    '''
    cursor.execute(sql)
    result = cursor.fetchone()
    total_page = math.ceil(result[0]/items_per_page)
    if total_page < 1:
        total_page = 1
    conn.commit()
    conn.close()
    return order_list, total_page

def get_order_detail(order_id):
    conn,cursor=connectDB()
    # fetch order detail
    sql = f'''
         select * 
         from orders
         where id = {order_id}
    '''
    cursor.execute(sql)
    result = cursor.fetchone()
    order_detail = {
        'date' : result[1],
        'time' : result[2],
        'discount' : result[4],
        'tax' : result[5],
        'total' : result[6],
        'cash' : result[7],
        'change' : result[8],
        'employee_code' : result[9],
        'status' : result[10]
    }

    # fetch order products
    sql = f'''
         select op.quantity, p.name, op.unit_price, op.total_price
         from order_products op, products p
         where op.order_id = {order_id} and op.product_id = p.id
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    product_list = []
    for product_db in result:
        product = {
            'quantity' : product_db[0],
            'name' : product_db[1],
            'unit_price' : product_db[2],
            'total_price' : product_db[3]
        }
        product_list.append(product)
    conn.commit()
    conn.close()
    return order_detail, product_list

def delete_order(order_id):
    conn,cursor=connectDB()
    sql = f'''
        update orders
        set status = 'Canceled'
        where id = {order_id}
    '''
    cursor.execute(sql)
    cursor.fetchall()
    conn.commit()
    conn.close()


def get_stock_list(page=1,items_per_page=20):
    conn,cursor=connectDB()

    # get stock list
    sql = f'''
        select *
        from stocks
        order by id desc
        limit {items_per_page} offset {(page - 1) * items_per_page}
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    stock_list = []
    for stock_db in result:
        stock = {
            'stock_id' : stock_db[0],
            'name' : stock_db[1],
            'grand_total' : stock_db[2],
            'company' : stock_db[3],
            'date' : stock_db[4],
            'time' : stock_db[5],
            'employee_code' : stock_db[6]
        }
        stock_list.append(stock)
    
    # get total page
    sql = f'''
        select count(*)
        from stocks
    '''
    cursor.execute(sql)
    result = cursor.fetchone()
    total_page = math.ceil(result[0]/items_per_page)
    if total_page < 1:
        total_page = 1
    conn.commit()
    conn.close()
    return stock_list, total_page

def get_stock_detail(stock_id):
    conn,cursor=connectDB()
    # fetch stock detail
    sql = f'''
         select * 
         from stocks
         where id = {stock_id}
    '''
    cursor.execute(sql)
    result = cursor.fetchone()
    stock_detail = {
        'stock_id' : result[0],
        'name' : result[1],
        'grand_total' : result[2],
        'company' : result[3],
        'date' : result[4],
        'time' : result[5],
        'employee_code' : result[6]
    }

    # fetch stock products
    sql = f'''
         select sp.inventory, sp.price, sp.product_id, p.name 
         from stock_products sp, products p
         where sp.stock_id = {stock_id} and sp.product_id = p.id
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    product_list = []
    for product_db in result:
        product = {
            'inventory' : product_db[0],
            'unit_price' : product_db[1],
            'product_id' : product_db[2],
            'product_name' : product_db[3]
        }
        product_list.append(product)
    conn.commit()
    conn.close()
    return stock_detail, product_list

def has_product_id(product_id):
    conn,cursor=connectDB()
    sql = f'''
         select id
         from products
         where id = '{product_id}'
    '''
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    if result is None:
        return False
    else:
        return True

def add_product_stock(data={}):
    conn,cursor=connectDB()
    date, time = get_time_now()
    # insert stock summary
    sql = f'''
        insert into stocks (name, grand_total, company, date, time, employee_id)
        values ("{data['stock_name']}", {data['grand_total']}, "{data['company_name']}", '{date}', '{time}', {data['employee_code']})
    '''
    cursor.execute(sql)

    # get stock id - ตัวที่เพิ่ง insert ไป
    sql = 'select last_insert_rowid()'
    cursor.execute(sql)
    result = cursor.fetchone()
    stock_id = result[0]

    # insert stock products
    for product in data['products']:
        sql = f'''
            insert into stock_products (stock_id, product_id, inventory, price)
            values ({stock_id}, '{product["id"]}', {product["inventory"]}, {product["unit_price"]})
        '''
        cursor.execute(sql)

    # increase products inventory
    for product in data['products']:
        sql = f'''
            update products
            set inventory = inventory + {product['inventory']}
            where id = {product['id']}
        '''
        cursor.execute(sql)

    conn.commit()
    conn.close()