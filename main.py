from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from func_db import insert_db, update_db, delete_db, fetch_column, get_product_list, place_order, get_time_now, get_order_list, get_order_detail, delete_order, get_stock_list, get_stock_detail, has_product_id, add_product_stock
from style import *
import math
import string
import sqlite3
import time

def Page_sales(): #TODO [Page] sales
    reset_body_page()
    MenuBar(root,row=0, col=0,active='sales')
    Create_sales_page(row=0, col=0)

def Page_orders(status='Completed'): #TODO [Page] orders
    reset_body_page()
    MenuBar(root,row=0, col=0,active='orders')
    Create_order_page(row=0, col=0, status=status)
    
def Page_employee(): #TODO [Page] employee
    reset_body_page()
    MenuBar(root,row=0, col=0,active='employee')

def Page_stocks(): #TODO [Page] stocks
    reset_body_page()
    MenuBar(root,row=0, col=0,active='stocks')
    Create_stock_page(row=0, col=0)

def connectDB():
    conn= sqlite3.connect('pixel.db')
    cursor=conn.cursor()
    return conn,cursor

def create_body_page():
    global body_page
    body_page = Frame(root, bg='#ECF1F5', bd=0)
    body_page.grid(row=1,column=0,sticky='news')
    body_page.columnconfigure(0, weight=1)
    body_page.rowconfigure(0, weight=1)

def reset_body_page():
    global body_page
    body_page.destroy()
    create_body_page()

def resize_image(path,width,height):
    try:
        img = Image.open(path)
        img = img.resize((width,height),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
    except:
        img = Image.open('images/img.png')
        img = img.resize((width,height),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
    return img

def MenuBar(parent,row=0, col=0,active=""): # TODO [Def] MenuBar
    def gotoFunc(func):
        if func == 0 : Page_sales()
        if func == 1: Page_orders()
        if func == 2: Page_products()
        if func == 3: Page_stocks()
        if func == 4: Page_employees()

    #>>>>> set frame <<<<<
    fr_main_manu = Frame(parent, bg='#364860', bd=0)
    fr_main_manu.grid(column=col, row=row, sticky='news')

    #>>>>> seting variable <<<<<
    if account[0][-1] == 'Owner' or account[0][-1] == 'Manager':
        menuList = ['sales', 'orders', 'products','stocks', 'employees']
    else:
        menuList = ['sales', 'orders']
    btnList = [x for x in menuList]

    # เพิ่ม weight ช่อง exit ให้เต็มช่องเดียว
    fr_main_manu.columnconfigure(len(menuList)+1, weight=1)

    #>>>>> show menu <<<<<
    fr_logo = Label(fr_main_manu,bg='#364860',fg='#9199AC',font='Tahoma 16 bold',bd=0,pady=10)
    fr_logo.grid(column=0, row=0, sticky='news')
    logo_image = resize_image("images/icons/icon-small.png", 45, 45)
    logo_image_frame = Label(fr_logo,bg='#364860')
    logo_image_frame.image = logo_image
    logo_image_frame['image'] = logo_image_frame.image
    logo_image_frame.pack(padx=15)
    for i,x in enumerate(menuList):
        btnList[i] = Button(fr_main_manu,text=x.upper(),bg='#364860',fg='#9199AC',font='Tahoma 16 bold',bd=0,padx=10,pady=10 ,command=lambda x=i: gotoFunc(x))
        btnList[i].grid(column=i+1,row=0,sticky='news')
        if active.upper() == x.upper():
            btnList[i]['state'] = DISABLED
            btnList[i]['disabledforeground'] = '#FFFFFF'
    Label(fr_main_manu, text='', bg='#364860', fg='#9199AC', font='Tahoma 16 bold', bd=0, padx=10, pady=5,width=20).grid(column=i+2, row=0, sticky='news')
    Button(fr_main_manu, text='EXIT', bg='#364860', fg='#9199AC', font='Tahoma 16 bold', bd=0, command=root.quit).grid(column=i+3, row=0, sticky='news')

def Create_sales_page(row=1, col=0):
    # fetch product list & init variable
    products = get_product_list()
    order_product_list = []
    qty_list = [IntVar() for x in products]
    total_list = [DoubleVar() for x in products]
    sub_total = DoubleVar()
    tax_total = DoubleVar()
    discount_total = DoubleVar()
    grand_total = DoubleVar()

    sales_page = Frame(body_page)
    sales_page.columnconfigure(1,weight=1)
    sales_page.grid(column=col,row=row,sticky='news')

    window_width = root.winfo_width()
    product_grid_width = window_width * 0.65
    product_grid_height = 700

    def calculate_summary():
        sub_total = 0
        for i, qty_TK in enumerate(qty_list):
            qty = float(qty_TK.get())
            total = products[i]['price'] * qty
            total_list[i].set(total)
            sub_total = sub_total + total
        discount = float(discount_total.get())
        sub_total = sub_total - discount
        tax = sub_total * 7 / 100
        grand_total = sub_total + tax
        return sub_total, discount, tax, grand_total

    def create_order_products(parent,row=0,column=0):
        global order_products #Frame
        order_products = Frame(parent,bg='white')
        order_products.columnconfigure(0,weight=1)
        order_products.columnconfigure(1,weight=1)
        order_products.columnconfigure(2,weight=1)
        order_products.columnconfigure(3,weight=1)
        order_products.columnconfigure(4,weight=1)
        order_products.columnconfigure(5,weight=1)
        order_products.grid(row=row,column=column,sticky='news')

        order_product_titles = ['NO.','NAME','AMT.','PRICE','TOTAL',' ']
        for index,title in enumerate(order_product_titles):
            Label(order_products,text=title,font='Tahoma 10 bold',bg='#596782',fg='white',pady=8).grid(row=0,column=index,sticky='news')

    def create_order_product_list(parent,row_start=0):
        for index,product in enumerate(order_product_list):
            Label(parent,text=index+1,font='Tahoma 10',bg='white',fg='#596782',pady=5).grid(row=row_start+index,column=0,sticky='news')
            Label(parent,text=product['name'],font='Tahoma 10',bg='white',fg='#596782',pady=5).grid(row=row_start+index,column=1,sticky='w')
            Label(parent,textvariable=qty_list[product['original_index']],font='Tahoma 10',bg='white',fg='#596782',pady=5).grid(row=row_start+index,column=2,sticky='news')
            Label(parent,text=product['price'],font='Tahoma 10',bg='white',fg='#596782',pady=5).grid(row=row_start+index,column=3,sticky='news')
            Label(parent,textvariable=total_list[product['original_index']],font='Tahoma 10',bg='white',fg='#596782',pady=5).grid(row=row_start+index,column=4,sticky='news')
            Button(parent,text='X',bg='red',fg='white',width=1,bd=0,font='Tahoma 10',padx=0,command=lambda x=index: on_remove_order_product(x)).grid(row=row_start+index,column=5,padx=2,pady=2,sticky='news')
        
    def on_remove_order_product(index):
        original_index = order_product_list[index]['original_index']
        if qty_list[original_index].get() > 0:
            qty_list[original_index].set(0)
        on_change_qty(original_index)

    def on_clear_order(show_confirm=True):
        global order_products #Frame
        global discount_total_str
        result = True
        if show_confirm == True:
            result =  messagebox.askyesno('Confirm Deleting','Do you want to cancel this order?')
        if result == True:
            order_product_list.clear()
            for index in range(len(products)):
                qty_list[index].set(0)
            sub_total.set(0)
            tax_total.set(0)
            discount_total.set(0)
            discount_total_str.set('0')
            grand_total.set(0)
            order_products.destroy()
            create_order_products(parent=order_summary,row=1,column=0)
            create_order_product_list(order_products,1)
   
    def on_chang_discount(value):
        try :
            discount = int(value.get())
        except ValueError :
            discount = 0
        discount_total.set(discount)
        this_sub_total, this_discount, this_tax, this_grand_total = calculate_summary()
        sub_total.set(this_sub_total)
        tax_total.set(this_tax)
        discount_total.set(this_discount)
        grand_total.set(this_grand_total)

    def on_change_qty(index):
        global order_summary #Frame
        global order_products #Frame
        found_index = -1
        qty = qty_list[index].get()
        for order_index, order_product in enumerate(order_product_list) :
            if order_product['id'] == products[index]['id'] :
                found_index = order_index
                break
        if found_index == -1:
            if qty > 0:
                products[index]['original_index'] = index
                order_product_list.append(products[index])
                create_order_product_list(order_products,1)
        elif qty == 0:
            order_product_list.pop(found_index)
            order_products.destroy()
            create_order_products(parent=order_summary,row=1,column=0)
            create_order_product_list(order_products,1)
        qty = qty_list[index].get()
        total_price = float(qty) * float(products[index]['price'])
        total_list[index].set(total_price)
        this_sub_total, this_discount, this_tax, this_grand_total = calculate_summary()
        sub_total.set(this_sub_total)
        tax_total.set(this_tax)
        discount_total.set(this_discount)
        grand_total.set(this_grand_total)

    def on_open_payment_popup():
        def on_success(widget,cash,change):
            # แปลง format product เพื่อนำไป insert ลง db
            products_to_insert = []
            for product in order_product_list:
                qty = qty_list[product['original_index']].get()
                product['quantity'] = qty
                product['cost'] = product['cost'] * qty
                product['total_price'] = product['price'] * qty
                products_to_insert.append(product)
            data_to_place = {
                'sub_total' : sub_total.get(),
                'discount': discount_total.get(),
                'tax': tax_total.get(),
                'grand_total': grand_total.get(),
                'cash' : cash,
                'change' : change,
                'employee_code' : account[0][0],
                'products' : products_to_insert
            }
            place_order(data_to_place)
            widget.destroy()
            on_clear_order(show_confirm=False)
            messagebox.showinfo('Complete Order','This order is completed !')
            Page_sales()
        if len(order_product_list) > 0:
            display_payment(grand_total=grand_total, on_success=on_success)
        else:
            messagebox.showwarning('Warning','Please select some products!')
             
    def create_product_grid():
        products_per_row = 3

        # >>>>> set scrollable products grid <<<<<
        product_grid = Frame(sales_page)
        canvas = Canvas(product_grid,height=product_grid_height,width=product_grid_width)
        scrollbar = Scrollbar(product_grid,orient="vertical",command=canvas.yview)

        product_grid_scrollable = Frame(canvas)
        product_grid_scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0,0),window=product_grid_scrollable,anchor="nw",width=product_grid_width)
        canvas.configure(yscrollcommand=scrollbar.set)

        product_grid.grid(column=0,row=0,sticky='news')
        canvas.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")

        # >>>>> render products <<<<<
        for index in range(products_per_row):
            product_grid_scrollable.columnconfigure(index, weight=1)
        
        for index, product in enumerate(products):
            product_card = Frame(product_grid_scrollable,padx=15,pady=15,bg='white')
            product_card.columnconfigure(0, weight=1)
            product_card.grid(row=math.floor(index / products_per_row),column=index % products_per_row,padx=10,pady=10,sticky='news')
            
            Label(product_card,text=product['id'],font='Tahoma 12 bold',anchor='w',bg='white').grid(row=0,column=0,pady=5,sticky='news')
            
            product_image = resize_image(product['image'],150,150) 
            product_image_frame = Label(product_card,bg='white')
            product_image_frame.image = product_image
            product_image_frame['image'] = product_image_frame.image
            product_image_frame.grid(row=1,column=0,pady=5)

            Label(product_card,text=product['name'],font='Tahoma 10 bold',anchor='w',bg='white').grid(row=2,column=0,pady=5,sticky='news')
            Label(product_card,text='PRICE : ' + str(product['price']),font='Tahoma 10',bg='white').grid(row=3,column=0,pady=5,sticky='w')
            Label(product_card,text='Inventory : ' + str(product['inventory']),font='Tahoma 10',bg='white').grid(row=3,column=0,pady=5,sticky='e')
            if product['inventory'] > 0:
                product_qty = Spinbox(product_card,from_=0,to=product['inventory'],textvariable=qty_list[index],justify=CENTER,bg='white',font='Tahoma 14',command=lambda x=index: on_change_qty(x))
                product_qty.grid(row=4,column=0,pady=5,sticky='news')
            else:
                Label(product_card,text='SOLD OUT',font='Tahoma 12 bold',bg='white',fg='red').grid(row=4,column=0,pady=5)

    def create_order_summary():
        global order_products #Frame
        global order_summary #Frame
        global discount_total_str
        order_summary = Frame(sales_page,bg='white')
        order_summary.columnconfigure(0,weight=1)
        order_summary.rowconfigure(1,weight=1)
        order_summary.grid(column=1,row=0,sticky='news')

        basic_info = Frame(order_summary,bg='white')
        button_wrapper = Frame(order_summary,bg='white')
        summary = Frame(order_summary,bg='white')
        summary.columnconfigure(0,weight=1)
        summary.columnconfigure(1,weight=1)

        basic_info.grid(row=0,column=0,sticky='news')
        create_order_products(parent=order_summary,row=1,column=0)
        button_wrapper.grid(row=1,column=0,sticky='news')
        summary.grid(row=2,column=0,sticky='news')

        Label(basic_info,text='ORDER',font='Tahoma 16 bold',bg='#596782',fg='white',pady=10).pack(fill=BOTH)
        Label(basic_info,text='Employee ID : '+str(account[0][0]),font='Tahoma 10 bold',bg='white',fg='#596782',anchor='w').pack(fill=BOTH,padx=10,pady=(10,5))
        Label(basic_info,text='Employee Name : '+str(account[0][2]),font='Tahoma 10 bold',bg='white',fg='#596782',anchor='w').pack(fill=BOTH,padx=10,pady=(5,10))

        Label(summary,text='Sub-Total',font='Tahoma 10 bold',bg='white').grid(row=0,column=0,sticky='w',padx=10,pady=(10,5))
        Label(summary,text='Discount',font='Tahoma 10 bold',bg='white').grid(row=1,column=0,sticky='w',padx=10,pady=(5,5))
        Label(summary,text='Tax(7%)',font='Tahoma 10 bold',bg='white').grid(row=2,column=0,sticky='w',padx=10,pady=(5,5))
        Label(summary,text='Total Price :',font='Tahoma 14 bold',bg='white',fg='#24d180').grid(row=3,column=0,sticky='w',padx=10,pady=(5,10))

        Label(summary,textvariable=sub_total,font='Tahoma 10 bold',bg='white').grid(row=0,column=1,sticky='e',padx=10,pady=(10,5))
        discount_total_str = StringVar()
        discount_total_str.set('0')
        discount_total_str.trace("w", lambda name, index, mode, value=discount_total_str: on_chang_discount(value))
        discount_entry = Entry(summary,width=15,textvariable=discount_total_str,font='Tahoma 10 bold',bg='white',justify=CENTER)
        discount_entry.grid(row=1,column=1,sticky='e',padx=10,pady=(5,5))
        Label(summary,textvariable=tax_total,font='Tahoma 10 bold',bg='white').grid(row=2,column=1,sticky='e',padx=10,pady=(5,5))
        Label(summary,textvariable=grand_total,font='Tahoma 14 bold',bg='white',fg='#24d180').grid(row=3,column=1,sticky='e',padx=10,pady=(5,10))

        action_buttons = Frame(summary,bg='white')
        action_buttons.columnconfigure(0,weight=1)
        action_buttons.columnconfigure(1,weight=1)
        action_buttons.grid(row=4,columnspan=2,sticky='news')
        Button(action_buttons,text='Cancel',font='Tahoma 10 bold',bg='#1c7ee1',fg='white',bd=0,pady=10,command=on_clear_order).grid(row=0,column=0,sticky='news',padx=10,pady=(10,10))
        Button(action_buttons,text='Pay',font='Tahoma 10 bold',bg='#24d180',fg='white',bd=0,pady=10,command=on_open_payment_popup).grid(row=0,column=1,sticky='news',padx=10,pady=(10,10))
   
    create_product_grid()
    create_order_summary()

def display_payment(grand_total, on_success):
    payment_popup = Toplevel(root)
    payment_popup.title('Payment')
    payment_popup.geometry('600x400')
    payment_popup.option_add('*font','Tahoma 20 bold')
    payment_popup.columnconfigure(0,weight=1)
    payment_popup.columnconfigure(1,weight=1)

    cash_str = StringVar()
    change_total = DoubleVar()
    cash_str.set(str(0))
    change_total.set(-grand_total.get())

    def on_change_cash(value):
        try :
            cash = float(value.get())
        except ValueError :
            cash = 0
        change = cash - grand_total.get()
        change_str = float("{:.2f}".format(change))
        change = float(change_str)
        change_total.set(change)

    def on_confirm():
        if change_total.get() >= 0:
            cash = float(cash_str.get())
            on_success(widget=payment_popup,cash=cash,change=change_total.get())
        else:
            messagebox.showwarning('Warning','Cash is less than ฿' + str(grand_total.get()),parent=payment_popup)
        
    Label(payment_popup,text='TOTAL PRICE = ' + str(grand_total.get()),bg='#596782',fg='white',pady=20).grid(row=0,columnspan=2,sticky='news')
    Label(payment_popup,text='CASH',fg='#596782').grid(row=1,column=0,pady=(40,15))
    Label(payment_popup,text='CHANGE',fg='#596782').grid(row=2,column=0,pady=(15,20))
    cash_str.trace("w", lambda name, index, mode, value=cash_str: on_change_cash(value))
    Entry(payment_popup,textvariable=cash_str,fg='#596782',justify=CENTER).grid(row=1,column=1,pady=(40,15))
    Entry(payment_popup,textvariable=change_total,fg='#596782',justify=CENTER,state=DISABLED).grid(row=2,column=1,pady=(15,20))
    confirm_btn = Button(payment_popup,text='Confirm',bg='#24d180',fg='white',bd=0,padx=10,pady=10,command=on_confirm)
    confirm_btn.grid(row=3,columnspan=2)

#######################################################################################
####################################### PRODUCT #######################################
#######################################################################################
def Page_products():
    reset_body_page()
    create_body_page() #body_page == root

    ############# เมนู #############
    MenuBar(root,row=0,col=0,active='products')
    # #ดึงชื่อ column ที่มีอยู่ในตาราง products ทั้งหมด
    column_in_database = fetch_column(table_name='products')
    ############## สร้างตัวแปร ที่ใช้ทั่วหน้า page #############
    #ดึงชื่อ column ที่มีอยู่ในตาราง products ทั้งหมด
    #column_in_database = fetch_column(table_name='products')
    #เอาไว้เก็บข้อมูลที่มากจาก db และจะส่งไป db
    product_dict = {}
    for x in column_in_database:
        product_dict[x] = StringVar()
    
    #สร้าง page product
    create_product_page = Frame(body_page,bd=0)
    create_product_page.grid(row=0,column=0,sticky='news')
    create_product_page.columnconfigure(0, weight=1)
    #กำหนดให้ row ที่ 2 ขยายให้เต็มในพื้นที่ที่เหลือ
    create_product_page.rowconfigure(2, weight=1)

    ############# ฟังก์ชั่น #############
    def get_cursor(ev):
        cursor_row=table.focus()
        contents=table.item(cursor_row)
        value_in_database = contents['values']
        if len(value_in_database)>0:
            for i,x in enumerate(product_dict):
                product_dict[x].set(value_in_database[i])

            #หากเลือกค่า จะให้แสดงปุ่มที่กดได้
            if btn_edit['text']!='Close':
                btn_edit['state']=NORMAL
                btn_edit['bg']=color['warning']

    #แสดงข้อมูลทั้งหมดในตาราง
    def fetch_data():
        conn, cursor = connectDB()
        sql = 'select * from products'
        cursor.execute(sql)
        result=cursor.fetchall()
        if len(result)!=0:
            table.delete(*table.get_children())
            for row in result:
                table.insert('',END,values=row)
            conn.commit()
        conn.close()
        search_By.set('')
        search_var.set('')
    
    def btn_disable(btn_name):
        btn_name['state']=DISABLED
        btn_name['bg']=color['default']
        btn_name['disabledforeground']=color['white']

    def clear_var():
        for i,x in enumerate(product_dict):
            product_dict[x].set('')
    
    def add_product():
        clear_var()
        edit_from()
        
    def close_edit():
        clear_var()
        fr_edit.destroy()
        Page_products()
        
    
    def get_product_data(data):
        #data ต้องเป็นแบบ dictionary เท่านั้น
        global new_data
        new_data = []
        for x in data:
            new_data.append(data[x].get())
        return new_data

    def save_product():
        new_data = get_product_data(product_dict)
        if len(new_data)>0:
            if str(new_data[0])!="0":
                if new_data[-2]=='':
                    new_data[-2]='images/img.png'
                insert_db(table_name="products",values=new_data)
                fetch_data()
            else:
                messagebox.showwarning(title='Alert',message="D'not enter the first zero number")
               
    def update_product():
        new_data = get_product_data(product_dict)
        if len(new_data)>0:
            if str(new_data[0])!="0":
                update_db(table_name="products",values=new_data)
                fetch_data()
            else:
                messagebox.showwarning(title='Alert',message="D'not enter the first zero number")
        
    def delete_product():
        new_data = get_product_data(product_dict)
        if len(new_data)>0:
            if str(new_data[0])!="0":
                delete_db(table_name="products",values=new_data)
                fetch_data()
                clear_var()
            else:
                messagebox.showwarning(title='Alert',message="D'not enter the first zero number")

    def upload_product_image():
        try:
            time_now = int(time.time())
            path = filedialog.askopenfilename(initialdir="/",title="Select product image",filetypes=[('image files', ('.png', '.jpg'))])
            if path != '':
                new_path = 'images/' + str(time_now) + '.png'
                img = Image.open(path)
                # resize image แบบคงอัตราส่วน กว้างสุด 250px
                resize_width = 250
                wpercent = (resize_width/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = Image.open(path).resize((resize_width,hsize),Image.ANTIALIAS)
                img.save(new_path)
                product_dict['image'].set(new_path)
        except:
            messagebox.showinfo('Error', 'Something went wrong!, Please try agian.')
    
    ############# ช่องแก้ไขข้อมูล #############
    def edit_from():
        #เปลี่ยนจากปุ่ม edit เป็น close
        if btn_edit['text'] == 'Edit':
            for key in style_btn_close:
                btn_edit[key]=style_btn_close[key]
            btn_edit['state']=NORMAL
        btn_edit['command'] = close_edit
        btn_disable(btn_add_product)

        #------- สร้างเฟรม fr_edit ----------
        global fr_edit
        fr_edit = Frame(create_product_page,bd=0)
        fr_edit.grid(row=1, column=0, sticky='news')
        fr_edit.columnconfigure(0, weight=1)
        #------- สร้างเฟรม ในตัว fr_edit
        fr_edit_row0 = Frame(fr_edit, bg='#FFFFFF', bd=0)
        fr_edit_row0.grid(row=0, column=0, sticky='news')
        fr_edit_row0.rowconfigure(0, weight=1)
        fr_edit_row0.columnconfigure(0, weight=1)
        fr_edit_row1 = Frame(fr_edit, bg='#FFFFFF', bd=0)
        fr_edit_row1.grid(row=1, column=0, sticky='news')
        fr_edit_row2 = Frame(fr_edit, bg='#FFFFFF', bd=0)
        fr_edit_row2.grid(row=2, column=0, sticky='news')

        # >>>>> set variable <<<<<
        #ไม่ต้องการแสดง คอลัมใดโปรดใส่ ให้ใส่ตรง entry_hide
        entry_hide=[]
        #ไม่ต้องการให้แก้ไข คอลัมใดโปรดใส่ ให้ใส่ตรง entry_disible
        entry_disible=[]
        #ใน 1 แถวต้องการให้แสดงกี่คอลัม ให้ใส่ตรง limit_col
        limit_col = 3
        
        #ห้ามแก้ไข
        c_row = 0  # count row
        c_col = 0  # count_column
        edit_entry = [StringVar() for x in product_dict]
        #/ห้ามแก้ไข

        # >>>>> show from <<<<<<
        for i in range(limit_col * 2 + 1):
            fr_edit_row1.columnconfigure(i, weight=1)
        for i, key in enumerate(product_dict):
            if key not in entry_hide:
                if c_col < (limit_col * 2):
                    Label(fr_edit_row1, set_lbl,text=key.capitalize() + " : ").grid(row=c_row,column=c_col,sticky='e',pady=10,padx=10)
                    if key == 'image':
                        fr_update_image = Frame(fr_edit_row1, bg='#ffffff')
                        fr_update_image.grid(column=c_col + 1, row=c_row, sticky='news',pady=15)
                        edit_entry[i] = Entry(fr_update_image, textvariable=product_dict[key], font='Tahoma 12', bg='#ffffff', fg='#596782')
                        edit_entry[i].pack(side=LEFT)
                        Button(fr_update_image,text='Choose',bd=0,bg='#34495e',fg='#ffffff',padx=10,command=upload_product_image).pack(side=LEFT,padx=10)
                        edit_entry[i]['state']=DISABLED
                    elif key == 'status':
                        edit_entry[i] = ttk.Combobox(fr_edit_row1,textvariable=product_dict[key] ,width=10, font=('Tahoma 12 bold'),state='readonly')
                        edit_entry[i]['values'] = ['Enable','Disable']
                        product_dict[key].set('Enable')
                        edit_entry[i].grid(column=c_col + 1, row=c_row, sticky='news', pady=15)
                    else:
                        edit_entry[i] = Entry(fr_edit_row1, textvariable=product_dict[key], font='Tahoma 12', bg='#ffffff', fg='#596782')
                        edit_entry[i].grid(column=c_col + 1, row=c_row, sticky='news', pady=15)
                    c_col = c_col + 2
                else:
                    c_col = 0
                    c_row = c_row + 1
                    Label(fr_edit_row1, set_lbl,text=key.capitalize() + " : ").grid(row=c_row,column=c_col,sticky='e',pady=10,padx=10)
                    if key == 'image':
                        fr_update_image = Frame(fr_edit_row1, bg='#ffffff')
                        fr_update_image.grid(column=c_col + 1, row=c_row, sticky='news',pady=15)
                        edit_entry[i] = Entry(fr_update_image, textvariable=product_dict[key], font='Tahoma 12', bg='#ffffff', fg='#596782')
                        edit_entry[i].pack(side=LEFT)
                        Button(fr_update_image,text='Choose',bd=0,bg='#34495e',fg='#ffffff',padx=10,command=upload_product_image).pack(side=LEFT,padx=10)
                        edit_entry[i]['state']=DISABLED
                    elif key == 'status':
                        edit_entry[i] = ttk.Combobox(fr_edit_row1,textvariable=product_dict[key] ,width=10, font=('Tahoma 12 bold'),state='readonly')
                        edit_entry[i]['values'] = ['Enable','Disable']
                        edit_entry[i].grid(column=c_col + 1, row=c_row, sticky='news', pady=15)
                        product_dict[key].set('Enable')
                    else:
                        edit_entry[i] = Entry(fr_edit_row1, textvariable=product_dict[key], font='Tahoma 12', bg='#ffffff', fg='#596782')
                        edit_entry[i].grid(column=c_col + 1, row=c_row, sticky='news', pady=15)
                    c_col = c_col + 2
                if key in entry_disible:
                    edit_entry[i]['state'] = DISABLED

        def check_cost(*args):
            try:
                float(product_dict['cost'].get())
            except :
                if product_dict['cost'].get() != '':
                    messagebox.showwarning('Alert','Please enter numbers only.')
                    product_dict['cost'].set('')
        def check_price(*args):
            try:
                float(product_dict['price'].get())
            except :
                if product_dict['price'].get() != '':
                    messagebox.showwarning('Alert','Please enter numbers only.')
                    product_dict['price'].set('')
        def check_inventory(*args):
            try:
                float(product_dict['inventory'].get())
            except :
                if product_dict['inventory'].get() != '':
                    messagebox.showwarning('Alert','Please enter numbers only.')
                    product_dict['inventory'].set('')

        product_dict['cost'].trace('w',check_cost)
        product_dict['price'].trace('w',check_price)
        product_dict['inventory'].trace('w',check_inventory)
        # >>>>> btn action<<<<<
        for i in range(6):
            if not(i > 0 and i < 5):
                fr_edit_row2.columnconfigure(i, weight=1)
        lbl_null1 = Label(fr_edit_row2,text="" ,bd=0, bg='#FFFFFF')
        lbl_null1.grid(column=0, row=0, sticky='news')
        btn_save = Button(fr_edit_row2,style_btn_save,command=save_product)
        btn_save.grid(column=1,row=0,sticky='',pady=(10,20),padx=10)
        btn_update = Button(fr_edit_row2, style_btn_update,command=update_product)
        btn_update.grid(column=2, row=0, sticky='', pady=(10, 20), padx=10)
        btn_del = Button(fr_edit_row2, style_btn_delete,command=delete_product)
        btn_del.grid(column=3, row=0, sticky='',pady=(10,20),padx=10)
        btn_clear = Button(fr_edit_row2, style_btn_clear , command=clear_var)
        btn_clear.grid(column=4, row=0, sticky='',pady=(10,20),padx=10)
        lbl_null2 = Label(fr_edit_row2,text="" ,bd=0, bg='#FFFFFF')
        lbl_null2.grid(column=6, row=0, sticky='news')

        def state_btn(*args):
            pro_id = str(product_dict['id'].get())
            conn, cursor = connectDB()
            sql = f"select * from products where id = '{pro_id}'"
            cursor.execute(sql)
            result=cursor.fetchall()
            if len(result)>0:     
                #UPDATE DELETE      
                for i,x in enumerate(product_dict):
                    if x!= 'id':
                        product_dict[x].set(result[0][i]) 
                btn_save['state']=DISABLED
                btn_update['state']=NORMAL
                btn_del['state']=NORMAL
            else :
                #SAVE
                for i,x in enumerate(product_dict):
                    if x!= 'id':
                        product_dict[x].set('') 
                btn_save['state']=NORMAL
                btn_update['state']=DISABLED
                btn_del['state']=DISABLED
            conn.commit()
            conn.close()
        state_btn()
        product_dict['id'].trace('w',state_btn)
        
    def reset_edit_from():
        global fr_edit
        fr_edit.destroy()
        create_product_page.destroy()
        Page_products()
            
    def search_product(col_search, txt_search, column=[]):
        new_col_search = col_search.get()
        new_txt_search = txt_search.get()
        if col_search.get() != '' and txt_search.get() != '':
            table.delete(*table.get_children())
            conn, cursor = connectDB()
            sql = 'select * from products'
            cursor.execute(sql)
            result = cursor.fetchall()

            for i, x in enumerate(column):
                if new_col_search == x:
                    column_index = i

            for x in result:
                if str(new_txt_search).lower() in str(x[column_index]).lower():
                    table.insert('', END, values=x)
            conn.commit()
            conn.close()
        else:
            fetch_data()

    ############# ช่องค้นหา #############
    #------- สร้างเฟรม ----------
    fr_search = Frame(create_product_page,bd=0,bg=color['bg'])
    fr_search.grid(row=0,column=0,sticky='news')

    #-------- สร้างคอลัม ---------
    fr_search.columnconfigure(0, weight=1)
    fr_search.columnconfigure(1, weight=1)
    fr_search.columnconfigure(2, weight=1)
    fr_search.columnconfigure(3, weight=1)
    fr_search.columnconfigure(4, weight=1)
    fr_search.columnconfigure(5, weight=1)
    fr_search.columnconfigure(6, weight=1)
    fr_search.columnconfigure(7, weight=1)
 
    #------- สร้างปุ่ม + ช่องค้นหา ----------
    #ข้อความ 'search'
    lbl=Label(fr_search, bg='#ECF1F5', text='search'.upper(), font='Tahoma 12 bold', fg="#364860")
    #ช่องเลือก column
    search_By = StringVar()
    combo_search = ttk.Combobox(fr_search, textvariable=search_By, width=10, font=('Tahoma 12'),state='readonly')
    combo_search['values'] = column_in_database
    #ช่องค้นหา
    search_var = StringVar()
    search_entry = Entry(fr_search, textvariable=search_var, font='Tahoma 14', bg='#ffffff', fg='#596782')

    #ปุ่มค้นหา
    btn_search = Button(fr_search, style_btn_search, command=lambda x=column_in_database,i=search_By,txt=search_var:search_product(col_search=i,txt_search=txt,column=x))
    #ปุ่มแสดงข้อมูลทั้งหมด
    btn_fetch_all = Button(fr_search, style_btn_fetch_all, command = fetch_data)

    #ปุ่มเพิ่มสินค้า
    btn_add_product = Button(fr_search, style_btn_add, text='Add Product',command=add_product)
    
    #ปุ่มแก้ไข
    btn_edit = StringVar()
    btn_edit = Button(fr_search, style_btn_edit,command=edit_from)
    btn_disable(btn_edit)
    
    #กำหนดจุดวางของปุ่มต่างๆ
    lbl.grid(column=1, row=0, pady=20)
    combo_search.grid(column=2, row=0, pady=10)
    search_entry.grid(column=3, row=0, sticky='news', pady=15)
    btn_search.grid(column=4, row=0, pady=15)
    btn_fetch_all.grid(column=5, row=0, pady=15)
    btn_add_product.grid(column=6, row=0, pady=15)
    btn_edit.grid(column=7, row=0, pady=15)
    
    ############# ช่องตาราง #############
    #------- สร้างเฟรม ----------
    fr_table = Frame(create_product_page,bd=0,bg=color['bg'])
    fr_table.grid(row=2,column=0,sticky='news')

    #-------- สร้างคอลัม + แถว---------
    fr_table.columnconfigure(0, weight=1)
    fr_table.rowconfigure(0, weight=1)

    # Start Product Table
    scroll_x = Scrollbar(fr_table, orient=HORIZONTAL)
    scroll_y = Scrollbar(fr_table, orient=VERTICAL)
    table = ttk.Treeview(fr_table,column=column_in_database,xscrollcommand=scroll_x,yscrollcommand=scroll_y)
    
    #กำหนดจุดที่จะแสดง scroll
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=table.xview)
    scroll_y.config(command=table.yview)

    #กำหนดชื่อ column ที่ต้องการให้แสดง
    for x in column_in_database:
        table.heading(x,text=str(x).upper())
    table['show']='headings'

    #กำหนดขนาดของ column
    for x in column_in_database:
        if x in ['name','image']:
            table.column(x, width=100,anchor='w')
        else:
            table.column(x, width=100,anchor="center")
    table.pack(fill=BOTH,expand=1)
    table.bind("<ButtonRelease-1>",get_cursor)
    
    #แสดงข้อมูลทั้งหมดในตาราง
    fetch_data()

#######################################################################################
####################################### ORDER #########################################
#######################################################################################

def Create_order_page(row=1, col=0, status='Completed'):
    # fetch order list
    current_page = IntVar()
    total_page = IntVar()
    order_id_search = StringVar()
    current_page.set(1)
    total_page.set(1)
    order_id_search.set('')
    items_per_page = 15
    order_page = Frame(body_page)
    order_page.columnconfigure(0,weight=1)
    order_page.grid(column=col,row=row,sticky='news')

    def on_change_page(type='NEXT'):
        global order_details_list 
        page = current_page.get()
        if type == 'NEXT':
            page += 1
        elif type == 'PREV':
            page -= 1
        if page > 0 and page <= total_page.get():
            current_page.set(page)
            order_details_list.destroy()
            create_order_details(row=2)

    def on_search_order():
        current_page.set(1)
        order_details_list.destroy()
        create_order_details(row=2)

    def on_clear_search():
        current_page.set(1)
        order_id_search.set('')
        order_details_list.destroy()
        create_order_details(row=2)

    def on_remove_order(order_id):
        result = messagebox.askyesno('Delete order', 'Are you sure to delete order #'+str(order_id))
        if result == True:
            delete_order(order_id)
            order_details_list.destroy()
            create_order_details(row=2)

    def on_chang_status(status):
        Page_orders(status=status)

    def header(row=0,column=0):
        header = Frame(order_page)
        header.columnconfigure(0,weight=1)
        header.columnconfigure(1,weight=1)
        header.grid(row=row,column=column,padx=(10,0),pady=10,sticky='news')
        Label(header,text=status+' Orders',font='Tahoma 14 bold').grid(row=0,column=0,sticky='w',padx=5)
        status_wrapper = Frame(header)
        status_wrapper.grid(row=0,column=1,sticky='e')
        if account[0][-1] == 'Owner' or account[0][-1] == 'Manager':
            Label(status_wrapper,text='Status : ',font='Tahoma 10 bold').pack(side=LEFT)
            Button(status_wrapper,text='Completed',bg='#1abc9c',fg='white',bd=0,font='Tahoma 10',padx=10,command=lambda status='Completed': on_chang_status(status)).pack(side=LEFT,padx=10)
            Button(status_wrapper,text='Canceled',bg='#e74c3c',fg='white',bd=0,font='Tahoma 10',padx=10,command=lambda status='Canceled': on_chang_status(status)).pack(side=LEFT,padx=5)


    def create_order_top_bar(row=0,column=0,page=1):
        order_top_bar = Frame(order_page)
        order_top_bar.columnconfigure(0,weight=1)
        order_top_bar.grid(row=row,column=column,padx=(10,0),pady=10,sticky='news')

        order_search = Frame(order_top_bar)
        order_search.grid(row=0,column=0,sticky='w')
        Label(order_search,text='Order No. : ',font='Tahoma 10 bold',padx=5).pack(side=LEFT)
        Entry(order_search,textvariable=order_id_search,font='Tahoma 10').pack(side=LEFT,padx=10)
        Button(order_search,text='Search',bg='#5a8cef',fg='white',bd=0,font='Tahoma 10',padx=10,command=on_search_order).pack(side=LEFT,padx=10)
        Button(order_search,text='Clear',bg='#f12843',fg='white',bd=0,font='Tahoma 10',padx=10,command=on_clear_search).pack(side=LEFT,padx=5)

        pagination = Frame(order_top_bar)
        pagination.grid(row=0,column=1,sticky='news')
        Button(pagination,text='<',bg='#5a8cef',fg='white',bd=0,font='Tahoma 10',padx=5,command=lambda type='PREV': on_change_page(type)).pack(padx=10, side=LEFT)
        Label(pagination, textvariable=current_page,font='Tahoma 10 bold',padx=0).pack(side=LEFT)
        Label(pagination, text='/',font='Tahoma 10 bold',padx=3).pack(side=LEFT)
        Label(pagination, textvariable=total_page,font='Tahoma 10 bold',padx=0).pack(side=LEFT)
        Button(pagination,text='>',bg='#5a8cef',fg='white',bd=0,font='Tahoma 10',padx=5,command=lambda type='NEXT': on_change_page(type)).pack(padx=10, side=LEFT)

    def create_order_details(row=0,column=0):
        global order_details_list
        page = current_page.get()
        search_id = order_id_search.get()
        order_list, this_total_page = get_order_list(page=page,items_per_page=items_per_page,order_id=search_id,status=status)
        total_page.set(this_total_page)
        order_details_list = Frame(order_page)
        column_count = 10
        if status == 'Canceled':
            column_count = 9
        for index in range(column_count):
            order_details_list.columnconfigure(index,weight=1)
        order_details_list.grid(row=row,column=column,sticky='news')

        order_details_titles = ['NO.','ORDER ID','EMPLOYEE CODE','DATE','TIME','DISCOUNT','TAX','TOTAL','','']
        for index,title in enumerate(order_details_titles):
            Label(order_details_list,text=title,font='Tahoma 10 bold',bg='white',fg='#596782',pady=8).grid(row=0,column=index,sticky='news')

        row_start = 1
        for index,order in enumerate(order_list):
            Label(order_details_list,text=((page-1)*items_per_page)+index+1,font='Tahoma 10',fg='#596782',).grid(row=row_start+index,column=0,pady=(10,5),sticky='news')
            Label(order_details_list,text=order['order_id'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=1,pady=(10,5),sticky='news')
            Label(order_details_list,text=order['employee_code'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=2,pady=(10,5),sticky='news')
            Label(order_details_list,text=order['date'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=3,pady=(10,5),sticky='news')
            Label(order_details_list,text=order['time'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=4,pady=(10,5),sticky='news')
            Label(order_details_list,text=order['discount'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=5,pady=(10,5),sticky='news')
            Label(order_details_list,text=order['tax'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=6,pady=(10,5),sticky='news')
            Label(order_details_list,text=order['total'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=7,pady=(10,5),sticky='news')

            #>>>>> seting variable <<<<<
            
            detail_btn = Button(order_details_list,text='DETAIL',bg='#5a8cef',fg='white',bd=0,font='Tahoma 10',padx=0,command=lambda order_id=order['order_id']: display_order_receipt(order_id))
            detail_btn.grid(row=row_start+index,column=8,padx=5,pady=5,sticky='news')
            if account[0][-1] == 'Owner' or account[0][-1] == 'Manager':    
                if status == 'Completed':
                    delete_btn = Button(order_details_list,text='DELETE',bg='#f12843',fg='white',bd=0,font='Tahoma 10',padx=0,command=lambda order_id=order['order_id']: on_remove_order(order_id))
                    delete_btn.grid(row=row_start+index,column=9,padx=(5,10),pady=5,sticky='news')

    header(row=0)
    create_order_top_bar(row=1)
    create_order_details(row=2)

def display_order_receipt(order_id):
    order_detail, order_product_list = get_order_detail(order_id)
    order_receipt = Toplevel(root,bg='white')
    order_receipt.title('Receipt')
    order_receipt.geometry('450x680')
    order_receipt.option_add('*font','Tahoma 10')

    if order_detail['status'] == 'Canceled':
        Label(order_receipt,text='Canceled',font='Tahoma 16 italic bold',fg='#596782',bg='white',pady=10).pack()

    Label(order_receipt,text='ORDER #'+ str(order_id),font='Tahoma 16 bold',fg='#596782',bg='white',pady=10).pack()
    Label(order_receipt,text='Address : 55 หมู่ 5 ต.เมือง อ.เมือง จ.อุบลราชธานี 34170',fg='#596782',bg='white',wraplength=400).pack()
    Label(order_receipt,text='Tel : 06-1615-9990   VAT# 1000023456789',fg='#596782',bg='white',wraplength=400).pack()
    Label(order_receipt,text='Employee code : ' + str(order_detail['employee_code']) + '  Date ' + str(order_detail['date']) + '  Time ' + str(order_detail['time']),fg='#596782',bg='white',wraplength=400).pack()
    Label(order_receipt,text='★'*28,fg='#596782',bg='white',pady=10).pack()
    Label(order_receipt,text='CASH RECEIPT',font='Tahoma 14',fg='#596782',bg='white').pack()
    Label(order_receipt,text='★'*28,fg='#596782',bg='white',pady=10).pack()

    receipt_description = Frame(order_receipt,bg='white')
    receipt_description.columnconfigure(0,weight=1)
    receipt_description.columnconfigure(1,weight=1)
    receipt_description.columnconfigure(2,weight=1)
    receipt_description.columnconfigure(3,weight=1)
    receipt_description.pack(fill=BOTH)

    Label(receipt_description,text='Description',font='Tahoma 12 bold',fg='#596782',bg='white').grid(row=0,columnspan=2,padx=20,sticky='w')
    Label(receipt_description,text='Price',font='Tahoma 12 bold',fg='#596782',bg='white').grid(row=0,column=3,columnspan=2,padx=20,sticky='e')
    
    row_start = 1
    for index,product in enumerate(order_product_list):
        Label(receipt_description,text=product['quantity'],fg='#596782',bg='white').grid(row=row_start+index,column=0,padx=(20,0),sticky='w')
        Label(receipt_description,text=product['name'],fg='#596782',bg='white').grid(row=row_start+index,column=1,padx=(0,10),sticky='w')
        if product['quantity'] > 1:
            Label(receipt_description,text='@'+str(product['unit_price']),fg='#596782',bg='white').grid(row=row_start+index,column=2,padx=10,sticky='e')
        Label(receipt_description,text=product['total_price'],fg='#596782',bg='white').grid(row=row_start+index,column=3,padx=(10,20),sticky='e')
    
    Label(order_receipt,text='★'*28,fg='#596782',bg='white',pady=10).pack()

    receipt_summary = Frame(order_receipt,bg='white')
    receipt_summary.columnconfigure(0,weight=1)
    receipt_summary.columnconfigure(1,weight=1)
    receipt_summary.pack(fill=BOTH)

    Label(receipt_summary,text='Discount',fg='#596782',bg='white').grid(row=0,column=0,padx=20,sticky='w')
    Label(receipt_summary,text=order_detail['discount'],fg='#596782',bg='white').grid(row=0,column=1,padx=20,sticky='e')

    Label(receipt_summary,text='Tax',fg='#596782',bg='white').grid(row=1,column=0,padx=20,sticky='w')
    Label(receipt_summary,text=order_detail['tax'],fg='#596782',bg='white').grid(row=1,column=1,padx=20,sticky='e')

    Label(receipt_summary,text='Total',font='Tahoma 12 bold',fg='#596782',bg='white').grid(row=2,column=0,padx=20,sticky='w')
    Label(receipt_summary,text=order_detail['total'],font='Tahoma 12 bold',fg='#596782',bg='white').grid(row=2,column=1,padx=20,sticky='e')

    Label(receipt_summary,text='Cash',fg='#596782',bg='white').grid(row=3,column=0,padx=20,sticky='w')
    Label(receipt_summary,text=order_detail['cash'],fg='#596782',bg='white').grid(row=3,column=1,padx=20,sticky='e')

    Label(receipt_summary,text='Change',fg='#596782',bg='white').grid(row=4,column=0,padx=20,sticky='w')
    Label(receipt_summary,text=order_detail['change'],fg='#596782',bg='white').grid(row=4,column=1,padx=20,sticky='e')

    Label(order_receipt,text='★'*28,fg='#596782',bg='white',pady=10).pack()
    Label(order_receipt,text='THANK YOU!',font='Tahoma 14 bold',fg='#596782',bg='white').pack()

#######################################################################################
####################################### STOCKS ########################################
#######################################################################################

def Create_stock_page(row=0, col=0):
    # fetch stock list
    current_page = IntVar()
    total_page = IntVar()
    current_page.set(1)
    total_page.set(1)
    items_per_page = 15
    stock_page = Frame(body_page)
    stock_page.columnconfigure(0,weight=1)
    stock_page.grid(column=col,row=row,sticky='news')

    def on_change_page(type='NEXT'):
        global stock_details_list 
        page = current_page.get()
        if type == 'NEXT':
            page += 1
        elif type == 'PREV':
            page -= 1
        if page > 0 and page <= total_page.get():
            current_page.set(page)
            stock_details_list.destroy()
            create_stock_details(row=2)

    def on_add_stock():
        global stock_details_list
        def on_success(widget,stock_data={}):
            add_product_stock(stock_data)
            widget.destroy()
            stock_details_list.destroy()
            create_stock_details(row=2)
            messagebox.showinfo('Success','Stock was successfully added!')
        display_add_stock(on_success=on_success)

    def create_stock_top_bar(row=0,crow=0,column=0,page=1):
        stock_top_bar = Frame(stock_page)
        stock_top_bar.columnconfigure(0,weight=1)
        stock_top_bar.grid(row=row,column=column,padx=(10,0),pady=10,sticky='news')

        Button(stock_top_bar,text='ADD STOCK',font='Tahoma 12 bold',bg='#16a085',fg='white',bd=0,padx=10,pady=5,command=on_add_stock).grid(row=0,column=0,padx=10,pady=10,sticky='w')

        pagination = Frame(stock_top_bar)
        pagination.grid(row=0,column=1,sticky='news')
        Button(pagination,text='<',bg='#5a8cef',fg='white',bd=0,font='Tahoma 10',padx=5,command=lambda type='PREV': on_change_page(type)).pack(padx=10, side=LEFT)
        Label(pagination, textvariable=current_page,font='Tahoma 10 bold',padx=0).pack(side=LEFT)
        Label(pagination, text='/',font='Tahoma 10 bold',padx=3).pack(side=LEFT)
        Label(pagination, textvariable=total_page,font='Tahoma 10 bold',padx=0).pack(side=LEFT)
        Button(pagination,text='>',bg='#5a8cef',fg='white',bd=0,font='Tahoma 10',padx=5,command=lambda type='NEXT': on_change_page(type)).pack(padx=10, side=LEFT)

    def create_stock_details(row=0,column=0):
        global stock_details_list
        page = current_page.get()
        stock_list, this_total_page = get_stock_list(page=page,items_per_page=items_per_page)
        total_page.set(this_total_page)
        stock_details_list = Frame(stock_page)
        column_count = 8
        for index in range(column_count):
            stock_details_list.columnconfigure(index,weight=1)
        stock_details_list.grid(row=row,column=column,sticky='news')

        stock_details_titles = ['NO.','STOCK ID','NAME','GRAND TOTAL','COMPANY','DATE','TIME','EMPLOYEE CODE','']
        for index,title in enumerate(stock_details_titles):
            Label(stock_details_list,text=title,font='Tahoma 10 bold',bg='white',fg='#596782',pady=8).grid(row=0,column=index,sticky='news')

        row_start = 1
        for index,stock in enumerate(stock_list):
            Label(stock_details_list,text=((page-1)*items_per_page)+index+1,font='Tahoma 10',fg='#596782',).grid(row=row_start+index,column=0,pady=(10,5),sticky='news')
            Label(stock_details_list,text=stock['stock_id'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=1,pady=(10,5),sticky='news')
            Label(stock_details_list,text=stock['name'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=2,pady=(10,5),sticky='news')
            Label(stock_details_list,text=stock['grand_total'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=3,pady=(10,5),sticky='news')
            Label(stock_details_list,text=stock['company'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=4,pady=(10,5),sticky='news')
            Label(stock_details_list,text=stock['date'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=5,pady=(10,5),sticky='news')
            Label(stock_details_list,text=stock['time'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=6,pady=(10,5),sticky='news')
            Label(stock_details_list,text=stock['employee_code'],font='Tahoma 10',fg='#596782').grid(row=row_start+index,column=7,pady=(10,5),sticky='news')

            detail_btn = Button(stock_details_list,text='DETAIL',bg='#5a8cef',fg='white',bd=0,font='Tahoma 10',padx=5,command=lambda stock_id=stock['stock_id']: display_stock_receipt(stock_id))
            detail_btn.grid(row=row_start+index,column=8,padx=5,pady=5,sticky='news')
            
    create_stock_top_bar(row=0)
    create_stock_details(row=1)

def display_stock_receipt(stock_id):
    stock_detail, stock_product_list = get_stock_detail(stock_id)
    stock_receipt = Toplevel(root,bg='white')
    stock_receipt.title('Stock')
    stock_receipt.geometry('450x680')
    stock_receipt.option_add('*font','Tahoma 10')

    Label(stock_receipt,text='STOCK #'+ str(stock_id),font='Tahoma 16 bold',fg='#596782',bg='white',pady=10).pack()
    Label(stock_receipt,text='('+ stock_detail['name'] +')',fg='#596782',bg='white',wraplength=400).pack()
    Label(stock_receipt,text='Address : 55 หมู่ 5 ต.เมือง อ.เมือง จ.อุบลราชธานี 34170',fg='#596782',bg='white',wraplength=400).pack()
    Label(stock_receipt,text='Company : ' + stock_detail['company'],fg='#596782',bg='white',wraplength=400).pack()
    Label(stock_receipt,text='Employee code : ' + str(stock_detail['employee_code']) + '  Date ' + str(stock_detail['date']) + '  Time ' + str(stock_detail['time']),fg='#596782',bg='white',wraplength=400).pack()
    Label(stock_receipt,text='★'*28,fg='#596782',bg='white',pady=10).pack()

    receipt_description = Frame(stock_receipt,bg='white')
    receipt_description.columnconfigure(0,weight=1)
    receipt_description.columnconfigure(1,weight=1)
    receipt_description.columnconfigure(2,weight=1)
    receipt_description.columnconfigure(3,weight=1)
    receipt_description.columnconfigure(4,weight=1)
    receipt_description.pack(fill=BOTH)

    Label(receipt_description,text='Description',font='Tahoma 12 bold',fg='#596782',bg='white').grid(row=0,columnspan=2,padx=20,sticky='w')
    Label(receipt_description,text='Price',font='Tahoma 12 bold',fg='#596782',bg='white').grid(row=0,column=4,columnspan=2,padx=20,sticky='e')
    
    row_start = 1
    total_inventory = 0
    for index,product in enumerate(stock_product_list):
        total_inventory = total_inventory + product['inventory']
        Label(receipt_description,text=product['inventory'],fg='#596782',bg='white').grid(row=row_start+index,column=0,padx=(20,0),sticky='w')
        Label(receipt_description,text=product['product_id'],fg='#596782',bg='white').grid(row=row_start+index,column=1,padx=(20,0),sticky='w')
        Label(receipt_description,text=product['product_name'],fg='#596782',bg='white').grid(row=row_start+index,column=2,padx=(0,10),sticky='w')
        if product['inventory'] > 1:
            Label(receipt_description,text='@'+str(product['unit_price']),fg='#596782',bg='white').grid(row=row_start+index,column=3,padx=10,sticky='e')
        Label(receipt_description,text=product['unit_price']*product['inventory'],fg='#596782',bg='white').grid(row=row_start+index,column=4,padx=(10,20),sticky='e')
    
    Label(stock_receipt,text='★'*28,fg='#596782',bg='white',pady=10).pack()

    receipt_summary = Frame(stock_receipt,bg='white')
    receipt_summary.columnconfigure(0,weight=1)
    receipt_summary.columnconfigure(1,weight=1)
    receipt_summary.pack(fill=BOTH)

    Label(receipt_summary,text='Total Inventory',fg='#596782',bg='white').grid(row=0,column=0,padx=20,sticky='w')
    Label(receipt_summary,text=total_inventory,fg='#596782',bg='white').grid(row=0,column=1,padx=20,sticky='e')

    Label(receipt_summary,text='Total Price',font='Tahoma 12 bold',fg='#596782',bg='white').grid(row=2,column=0,padx=20,sticky='w')
    Label(receipt_summary,text=stock_detail['grand_total'],font='Tahoma 12 bold',fg='#596782',bg='white').grid(row=2,column=1,padx=20,sticky='e')

def display_add_stock(on_success):
    window_width = 680
    window_height = 720
    add_stock_fr = Toplevel(root)
    add_stock_fr.resizable(False, False)
    add_stock_fr.title('Add Stock')
    add_stock_fr.geometry(str(window_width)+'x'+str(window_height))
    add_stock_fr.option_add('*font','Tahoma 12')

    # innt variables
    product_list = []
    stock_name_input = StringVar()
    company_input = StringVar()
    product_id_input = StringVar()
    product_inventory_input = IntVar()
    product_price_input = DoubleVar()

    Label(add_stock_fr,text='ADD STOCK',font='Tahoma 16 bold',bg='#364860',fg='white',pady=20).pack(fill=BOTH)

    stock_info = Frame(add_stock_fr,pady=15)
    stock_info.columnconfigure(1,weight=1)
    stock_info.pack(fill=BOTH,padx=30)
    Label(stock_info,text='Stock Name : ',font='Tahoma 12 bold').grid(row=0,column=0,padx=10,pady=10,sticky='w')
    Entry(stock_info,textvariable=stock_name_input,font='Tahoma 12',width=40).grid(row=0,column=1,padx=10,pady=10,sticky='w')
    Label(stock_info,text='Company : ',font='Tahoma 12 bold').grid(row=1,column=0,padx=10,pady=10,sticky='w')
    Entry(stock_info,textvariable=company_input,font='Tahoma 12',width=40).grid(row=1,column=1,padx=10,pady=10,sticky='w')

    def on_add_product():
        global stock_details
        product_id = product_id_input.get()
        product_inventory = product_inventory_input.get()
        product_price = product_price_input.get()
        exist_product_index = find_product_index_by_id(product_id)
        if product_id == '':
            messagebox.showwarning('Warning','Please fill product ID',parent=add_stock_fr)
            return
        if product_inventory <= 0:
            messagebox.showwarning('Warning','Inventory must greater than 0',parent=add_stock_fr)
            return
        if exist_product_index != -1:
            messagebox.showwarning('Warning','Product ID '+ product_id + ' is already exists!',parent=add_stock_fr)
            return
        is_exist_product_id = has_product_id(product_id)
        if is_exist_product_id == False:
            messagebox.showwarning('Warning','There is no product ID '+ product_id + ' in system!',parent=add_stock_fr)
            return
        product = {
            'id' : product_id,
            'inventory' : product_inventory,
            'unit_price' : product_price
        }
        product_list.append(product)
        product_id_input.set('')
        product_inventory_input.set(0)
        product_price_input.set(0.0)
        stock_details.destroy()
        create_stock_details()

    def on_remove_product(product_index):
        global stock_details
        product_list.pop(product_index)
        stock_details.destroy()
        create_stock_details()
  
    def find_product_index_by_id(product_id):
        found_index = -1
        for index,product in enumerate(product_list):
            if product['id'] == product_id:
                found_index = index
                break
        return found_index

    def on_save_stock():
        stock_name = stock_name_input.get()
        company_name = company_input.get()
        if stock_name == '' or company_name == '':
            messagebox.showwarning('Warning','Please fill stock name and company name!',parent=add_stock_fr)
            return
        if len(product_list) == 0:
            messagebox.showwarning('Warning','Please add some products!',parent=add_stock_fr)
            return
        grand_total = 0
        for product in product_list:
            grand_total += product['inventory'] * product['unit_price']
        data = {
            'stock_name' : stock_name,
            'company_name' : company_name,
            'grand_total' : grand_total,
            'employee_code' : account[0][0],
            'products' : product_list
        }
        on_success(widget=add_stock_fr,stock_data=data)

    def create_stock_details():
        global stock_details
        stock_details = Frame(add_stock_fr)
        stock_details.columnconfigure(0,weight=1)
        stock_details.columnconfigure(1,weight=1)
        stock_details.columnconfigure(2,weight=1)
        stock_details.columnconfigure(3,weight=1)
        stock_details.pack(fill=BOTH)
        # stock details title
        Label(stock_details,text='Products',font='Tahoma 14 bold',bg='#8c929c',fg='white',pady=10).grid(row=0,columnspan=4,sticky='news')
        Label(stock_details,text='Product ID',font='Tahoma 12 bold').grid(row=1,column=0,padx=(40,10),pady=10,sticky='w')
        Label(stock_details,text='Inventory',font='Tahoma 12 bold').grid(row=1,column=1,padx=10,pady=10,sticky='w')
        Label(stock_details,text='Unit Price',font='Tahoma 12 bold').grid(row=1,column=2,padx=(10,40),pady=10,sticky='w')
        # add product input
        Entry(stock_details,textvariable=product_id_input).grid(row=2,column=0,padx=(40,10),pady=10,sticky='w')
        Entry(stock_details,textvariable=product_inventory_input).grid(row=2,column=1,padx=10,pady=10,sticky='w')
        Entry(stock_details,textvariable=product_price_input).grid(row=2,column=2,padx=10,pady=10,sticky='w')
        Button(stock_details,text='ADD',font='Tahoma 12 bold',fg='white',bg='#3498db',bd=0,padx=15,command=on_add_product).grid(row=2,column=3,padx=(10,40))
        # product list
        row_start = 3
        for index,product in enumerate(product_list):
            Label(stock_details,text=product['id']).grid(row=row_start+index,column=0,padx=(40,10),pady=(5,5),sticky='w')
            Label(stock_details,text=product['inventory']).grid(row=row_start+index,column=1,padx=10,pady=(5,5),sticky='w')
            Label(stock_details,text=product['unit_price']).grid(row=row_start+index,column=2,padx=10,pady=(5,5),sticky='w')
            Button(stock_details,text='X',font='Tahoma 10',fg='white',padx=5,bg='#e74c3c',bd=0,command=lambda product_index=index: on_remove_product(product_index)).grid(row=row_start+index,column=3,padx=(10,40),pady=(5,5))

    def create_save_button():
        fr_height = 50
        save_fr = Frame(add_stock_fr)
        save_fr.columnconfigure(0,weight=1)
        save_fr.place(x=0,y=window_height-fr_height,width=window_width,height=fr_height)

        Label(save_fr,text='*After saved, you will not able to edit stock !!',font='Tahoma 12 bold',fg='#e74c3c').grid(row=0,column=0,padx=10,pady=10,sticky='e')
        Button(save_fr,text='SAVE',font='Tahoma 12 bold',fg='white',bg='#1abc9c',bd=0,padx=15,command=on_save_stock).grid(row=0,column=1,padx=20,pady=10,sticky='e')

    create_stock_details()
    create_save_button()

#######################################################################################
####################################### employees #####################################
#######################################################################################

def Page_employees():
    ########### start page ############
    MenuBar(root,row=0,col=0,active='employees')

    ############# variable ############
    column_in_employee = fetch_column(table_name='employees')
    edit_entry = [StringVar() for x in column_in_employee]
    employee_var = [StringVar() for x in column_in_employee]

    ########## สร้าง page employee #########
    create_employee_page = Frame(body_page,bd=0)
    create_employee_page.grid(row=0,column=0,sticky='news')
    create_employee_page.columnconfigure(0, weight=1)
    #กำหนดให้ row ที่ 2 ขยายให้เต็มในพื้นที่ที่เหลือ
    create_employee_page.rowconfigure(2, weight=1)

    ############# function ############
    def values_employee():
        global values_employee_db
        global values_employee_show
        global values_employee_sand
        conn,cursor = connectDB()
        sql = "select * from employees"
        cursor.execute(sql)
        values_employee_db = cursor.fetchall()
        values_employee_show = []
        values_employee_sand = []
        for x in values_employee_db:
            if account[0][-1] == 'Owner':
                values_employee_show.append(list(x))
            if account[0][-1] == 'Manager':
                if account[0][0] == x[0]:
                    values_employee_show.append(list(x))
                if x[-4] == "Cashier":
                    values_employee_show.append(list(x))
        conn.commit()
        conn.close()
    values_employee()

    def fetch_data():
        values_employee()
        if len(values_employee_show)>0:
            table.delete(*table.get_children())
            for i,x in enumerate(values_employee_show):
                    new_x = x
                    new_x[2] = '*'*len(new_x[2])
                    table.insert('',END,values=new_x,text=new_x)
        else:
            table.delete(*table.get_children())

    def get_cursor(ev):
        values_employee()
        cursor_row=table.focus()
        contents=table.item(cursor_row)
        get_select = contents['values']
        if len(get_select) >0:
            index_value = ''
            for i,x in enumerate(values_employee_show):
                if get_select[0]==x[0]:
                    index_value = i
            for i,x in enumerate(values_employee_show[index_value]):
                employee_var[i].set(x)
        btn_edit['state']=NORMAL

    def clear_var():
        for i,x in enumerate(employee_var):
            employee_var[i].set('')
        fetch_data()
        search_By.set('')
        search_var.set('')
        employee_var[-4].set('Cashier')
        employee_var[-1].set('Enable')
        create_id_employee()

    def create_id_employee():
        values_employee()
        id_now = 0
        for x in values_employee_db:
            if id_now < int(x[0]):
                id_now = int(x[0])
        employee_var[0].set(str(id_now+1))

    def save_employee():
        msg = messagebox.askquestion('Alert','Do you want to add more employees?',icon = 'warning')
        if msg == 'yes':
            values_employee()
            for i,x in enumerate(employee_var):
                values_employee_sand.append(employee_var[i].get())
            if employee_var[0].get() != '':
                if employee_var[1].get() != '':
                    if employee_var[2].get() != '':
                        if employee_var[3].get() != '':
                            conn,cursor = connectDB()
                            sql=f"""
                                select * from employees where username = '{values_employee_sand[1]}'
                            """
                            cursor.execute(sql)
                            result=cursor.fetchall()
                            if len(result)>0:
                                messagebox.showwarning('Alert','This username is already taken.')
                            else:
                                insert_db(table_name='employees',values=values_employee_sand)
                        else:
                            messagebox.showwarning('Alert','Please enter first name.')
                    else:
                        messagebox.showwarning('Alert','Please enter password.')
                else:
                    messagebox.showwarning('Alert','Please enter username.')
            else:
                messagebox.showwarning('Alert','Please enter your id.')
            clear_var()

    def update_employee():
        msg = messagebox.askquestion('Alert','Do you want to update employee data?',icon = 'warning')
        if msg == 'yes':
            values_employee()
            for i,x in enumerate(employee_var):
                values_employee_sand.append(employee_var[i].get())
            if employee_var[0].get() != '':
                if employee_var[1].get() != '':
                    if employee_var[2].get() != '':
                        if employee_var[3].get() != '':
                            conn,cursor = connectDB()
                            sql=f"""
                                select * from employees where username = '{values_employee_sand[1]}'
                            """
                            cursor.execute(sql)
                            result=cursor.fetchall()
                            if len(result)>0:
                                if str(result[0][0])==str(values_employee_sand[0]):
                                    update_db(table_name='employees',values=values_employee_sand)
                                else:
                                    messagebox.showwarning('Alert','An error has occurred Please try again.')
                            else:
                                update_db(table_name='employees',values=values_employee_sand)
                        else:
                            messagebox.showwarning('Alert','Please enter first name.')
                    else:
                        messagebox.showwarning('Alert','Please enter password.')
                else:
                    messagebox.showwarning('Alert','Please enter username.')
            else:
                messagebox.showwarning('Alert','Please enter your id.')
            clear_var()

    def delete_employee():
        msg = messagebox.askquestion('Alert','Do you want to delete employee data?',icon = 'warning')
        if msg == 'yes':
            values_employee()
            for i,x in enumerate(employee_var):
                values_employee_sand.append(employee_var[i].get())
            if employee_var[0].get() != '':
                if employee_var[1].get() != '':
                    if employee_var[2].get() != '':
                        if employee_var[3].get() != '':
                            delete_db(table_name='employees',values=values_employee_sand)
                        else:
                            messagebox.showwarning('Alert','Please enter first name.')
                    else:
                        messagebox.showwarning('Alert','Please enter password.')
                else:
                    messagebox.showwarning('Alert','Please enter username.')
            else:
                messagebox.showwarning('Alert','Please enter your id.')
            clear_var()
    def close_edit():
        clear_var()
        create_employee_page.destroy()
        Page_employees()

        

    def add_employee():
        clear_var()
        edit_from()

    def get_form_title(key):
        titles = {
            'id' : 'Id',
            'username' : 'Username',
            'password' : 'Password',
            'firstname' : 'Firstname',
            'lastname' : 'Lastname',
            'personal_id' : 'Personal ID',
            'age' : 'Age',
            'tel' : 'Tel.',
            'gender' : 'Gender',
            'birthday' : 'Birthday',
            'address' : 'Address',
            'district' : 'District',
            'province' : 'Province',
            'zip_code' : 'Zip code',
            'job_position' : 'Job position',
            'job_start_date' : 'Job started date',
            'salary' : 'Salary',
            'status' : 'Status',
        }
        if key in titles:
            return titles[key]
        return key.capitalize()
    
        
    def edit_from():
        #เปลี่ยนจากปุ่ม edit เป็น close
        if btn_edit['text'] == 'Edit':
            for key in style_btn_close:
                btn_edit[key]=style_btn_close[key]
            btn_edit['state']=NORMAL
        btn_edit['command'] = close_edit
        btn_add_employee['state']=DISABLED
        ############# edit frame ##########
        #------- สร้างเฟรม fr_edit ----------
        global fr_edit
        fr_edit = Frame(create_employee_page,bd=0)
        fr_edit.grid(row=1, column=0, sticky='news')
        fr_edit.columnconfigure(0, weight=1)
        #------- สร้างเฟรม ในตัว fr_edit
        #กำหนดให้เฉพาะ fr_edit_row0 เพื่อใช้ใน func create_id
        global fr_edit_row0
        fr_edit_row0 = Frame(fr_edit, bg='#FFFFFF', bd=0)
        fr_edit_row0.grid(row=0, column=0, sticky='news')
        fr_edit_row0.rowconfigure(0, weight=1)
        fr_edit_row0.columnconfigure(0, weight=1)
        fr_edit_row1 = Frame(fr_edit, bg='#FFFFFF', bd=0)
        fr_edit_row1.grid(row=1, column=0, sticky='news')
        fr_edit_row2 = Frame(fr_edit, bg='#FFFFFF', bd=0)
        fr_edit_row2.grid(row=2, column=0, sticky='news')

        entry_disable=['id']
        #ใน 1 แถวต้องการให้แสดงกี่คอลัม ให้ใส่ตรง limit_col
        limit_col = 3

        #ห้ามแก้ไข
        c_row = 0  # count row
        c_col = 0  # count_column
        #/ห้ามแก้ไข

        if account[0][-1] == 'Owner':
            job=['Owner','Manager','Cashier']
        else :
            job=['Cashier']
        # >>>>> edit form <<<<<<
        for i in range(limit_col * 2 + 1):
            fr_edit_row1.columnconfigure(i, weight=1)
        for i, key in enumerate(column_in_employee):
            title = get_form_title(key)
            if c_col < (limit_col * 2):
                Label(fr_edit_row1, set_lbl,text=title + " : ").grid(row=c_row,column=c_col,sticky='e',pady=10,padx=10)
                if key == 'status':
                    edit_entry[i] = ttk.Combobox(fr_edit_row1,textvariable=employee_var[i] ,width=10, font=('Tahoma 12 bold'),state='readonly')
                    edit_entry[i]['values'] = ['Enable','Disable']
                elif key == 'job_position':
                    edit_entry[i] = ttk.Combobox(fr_edit_row1,textvariable=employee_var[i] ,width=10, font=('Tahoma 12 bold'),state='readonly')
                    edit_entry[i]['values'] = job
                elif key == 'gender':
                    edit_entry[i] = ttk.Combobox(fr_edit_row1,textvariable=employee_var[i] ,width=10, font=('Tahoma 12'),state='readonly')
                    edit_entry[i]['values'] = ['Male','Female']
                else:
                    edit_entry[i] = Entry(fr_edit_row1, textvariable=employee_var[i], font='Tahoma 12', bg='#ffffff', fg='#596782')
                edit_entry[i].grid(column=c_col + 1, row=c_row, sticky='news', pady=15)
                c_col = c_col + 2
            else:
                c_col = 0
                c_row = c_row + 1
                Label(fr_edit_row1, set_lbl,text=title + " : ").grid(row=c_row,column=c_col,sticky='e',pady=10,padx=10)
                if key == 'status':
                    edit_entry[i] = ttk.Combobox(fr_edit_row1,textvariable=employee_var[i] ,width=10, font=('Tahoma 12 bold'),state='readonly')
                    edit_entry[i]['values'] = ['Enable','Disable']
                elif key == 'job_position':
                    employee_var[i] = StringVar()
                    edit_entry[i] = ttk.Combobox(fr_edit_row1,textvariable=employee_var[i] ,width=10, font=('Tahoma 12 bold'),state='readonly')
                    edit_entry[i]['values'] = job
                elif key == 'gender':
                    employee_var[i] = StringVar()
                    edit_entry[i] = ttk.Combobox(fr_edit_row1,textvariable=employee_var[i] ,width=10, font=('Tahoma 12'),state='readonly')
                    edit_entry[i]['values'] = ['Male','Female']
                else:
                    edit_entry[i] = Entry(fr_edit_row1, textvariable=employee_var[i], font='Tahoma 12', bg='#ffffff', fg='#596782')
                edit_entry[i].grid(column=c_col + 1, row=c_row, sticky='news', pady=15)
                c_col = c_col + 2
            if key in entry_disable:
                edit_entry[i]['state'] = DISABLED
            if key=="password":
                edit_entry[i]['show']='*'
        
    
        # >>>>> btn action<<<<<
        for i in range(6):
            if not(i > 0 and i < 5):
                fr_edit_row2.columnconfigure(i, weight=1)
        lbl_null1 = Label(fr_edit_row2,text="" ,bd=0, bg='#FFFFFF')
        lbl_null1.grid(column=0, row=0, sticky='news')
        btn_save = Button(fr_edit_row2,style_btn_save,command=save_employee)
        btn_save.grid(column=1,row=0,sticky='',pady=(10,20),padx=10)
        btn_update = Button(fr_edit_row2, style_btn_update,command=update_employee)
        btn_update.grid(column=2, row=0, sticky='', pady=(10, 20), padx=10)
        btn_del = Button(fr_edit_row2, style_btn_delete,command=delete_employee)
        btn_del.grid(column=3, row=0, sticky='',pady=(10,20),padx=10)
        btn_clear = Button(fr_edit_row2, style_btn_clear,command=clear_var)
        btn_clear.grid(column=4, row=0, sticky='',pady=(10,20),padx=10)
        lbl_null2 = Label(fr_edit_row2,text="" ,bd=0, bg='#FFFFFF')
        lbl_null2.grid(column=6, row=0, sticky='news')

        def state_btn(*args):
            conn, cursor = connectDB()
            sql = f"select * from employees where id = '{employee_var[0].get()}'"
            cursor.execute(sql)
            result=cursor.fetchall()
            if len(result)>0:            
                btn_save['state']=DISABLED
                btn_update['state']=NORMAL
                btn_del['state']=NORMAL
            else :
                btn_save['state']=NORMAL
                btn_update['state']=DISABLED
                btn_del['state']=DISABLED
            conn.commit()
            conn.close()
        state_btn()
        employee_var[0].trace('w',state_btn)

    ############# ช่องค้นหา #############
    def search_employee():
        values_employee()
        search_result = []
        if search_By.get() != '' and search_var.get() != '' :
            index_column = column_in_employee.index(search_By.get())
            for i,x in enumerate(values_employee_show):
                if str(search_var.get()).lower() in str(x[index_column]).lower():
                    search_result.append(x)
            if len(search_result)>0:
                table.delete(*table.get_children())
                for i,x in enumerate(search_result):
                    new_x = x
                    new_x[2] = '*'*len(new_x[2])
                    table.insert('',END,values=new_x,text=new_x)
            else:
                table.delete(*table.get_children())
        else :
            fetch_data()

    #------- สร้างเฟรม ----------
    fr_search = Frame(create_employee_page,bd=0,bg=color['bg'])
    fr_search.grid(row=0,column=0,sticky='news')

    #-------- สร้างคอลัม ---------
    fr_search.columnconfigure(0, weight=1)
    fr_search.columnconfigure(1, weight=1)
    fr_search.columnconfigure(2, weight=1)
    fr_search.columnconfigure(3, weight=1)
    fr_search.columnconfigure(4, weight=1)
    fr_search.columnconfigure(5, weight=1)
    fr_search.columnconfigure(6, weight=1)
    fr_search.columnconfigure(7, weight=1)

    #------- สร้างปุ่ม + ช่องค้นหา ----------
    #ข้อความ 'search'
    lbl=Label(fr_search, bg='#ECF1F5', text='search'.upper(), font='Tahoma 12', fg="#364860")

    #ช่องเลือก column ตัดช่องรหัสผ่านออก
    new_column = []
    for x in column_in_employee:
        new_column.append(x)
    pass_index = new_column.index('password')
    new_column.pop(pass_index)
    search_By = StringVar()
    combo_search = ttk.Combobox(fr_search, textvariable=search_By, width=10, font=('Tahoma 12'),state='readonly')
    combo_search['values'] = new_column

    #ช่องค้นหา
    search_var = StringVar()
    search_entry = Entry(fr_search, textvariable=search_var, font='Tahoma 14', bg='#ffffff', fg='#596782')

    #ปุ่มค้นหา
    btn_search = Button(fr_search, style_btn_search,command=search_employee)
    #ปุ่มแสดงข้อมูลทั้งหมด
    btn_fetch_all = Button(fr_search, style_btn_fetch_all,command=fetch_data)

    #ปุ่มเพิ่มพนักงาน
    btn_add_employee = Button(fr_search, style_btn_add, text='Add employee',command=add_employee)

    #ปุ่มแก้ไข
    btn_edit = StringVar()
    btn_edit = Button(fr_search, style_btn_edit,command=edit_from)
    btn_edit['state']=DISABLED

    #กำหนดจุดวางของปุ่มต่างๆ
    lbl.grid(column=1, row=0, pady=20)
    combo_search.grid(column=2, row=0, pady=10)
    search_entry.grid(column=3, row=0, sticky='news', pady=15)
    btn_search.grid(column=4, row=0, pady=15)
    btn_fetch_all.grid(column=5, row=0, pady=15)
    btn_add_employee.grid(column=6, row=0, pady=15)
    btn_edit.grid(column=7, row=0, pady=15)

    ############# ช่องตาราง #############
    #------- สร้างเฟรม ----------
    fr_table = Frame(create_employee_page,bd=0,bg=color['bg'])
    fr_table.grid(row=2,column=0,sticky='news')

    #-------- สร้างคอลัม + แถว---------
    fr_table.columnconfigure(0, weight=1)
    fr_table.rowconfigure(0, weight=1)

    # Start employee Table
    scroll_x = Scrollbar(fr_table, orient=HORIZONTAL)
    scroll_y = Scrollbar(fr_table, orient=VERTICAL)
    table = ttk.Treeview(fr_table,column=column_in_employee,xscrollcommand=scroll_x,yscrollcommand=scroll_y)

    #กำหนดจุดที่จะแสดง scroll
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=table.xview)
    scroll_y.config(command=table.yview)

    #กำหนดชื่อ column ที่ต้องการให้แสดง
    for x in column_in_employee:
        title = get_form_title(x)
        table.heading(x,text=title.upper())
    table['show']='headings'

    #กำหนดขนาดของ column
    for x in column_in_employee:
        if x in ['id','zip_code','age','status']:
            table.column(x, width=100,anchor='center')
        elif x in ['salary']:
            table.column(x, width=100,anchor='e')
        else :
            table.column(x, width=100,anchor='w')
    table.pack(fill=BOTH,expand=1)
    table.bind("<ButtonRelease-1>",get_cursor)

    #แสดงข้อมูลทั้งหมดในตาราง
    fetch_data()

def login():
    def gogogo():
        if username.get()!='':
            if password.get()!='':
                conn,cursor=connectDB()
                sql = f"""
                    select * from employees where username='{username.get()}'
                """
                cursor.execute(sql)
                result = cursor.fetchall()
                if len(result)>0:
                    if str(password.get()) == str(result[0][2]):
                        if result[0][-1]!='Disable':
                            global account
                            conn, cursor = connectDB()
                            sql=f"select id,username,firstname,job_position from employees where username = '{username.get()}'"
                            cursor.execute(sql)
                            account=cursor.fetchall()
                            conn.commit()
                            conn.close()
                            fr_login.destroy()
                            create_body_page()  
                            Page_sales()
                            root.geometry('1024x768+0+0')
                        else :
                            messagebox.showwarning('Alert','The username has been deleted.')
                    else:
                        messagebox.showwarning('Alert','Incorrect password')
                else:
                    messagebox.showwarning('Alert','This username does not exist in the system.')
            else:
                messagebox.showwarning('Alert','Please enter password.')
        else:
            messagebox.showwarning('Alert','Please enter username')

    fr_login = LabelFrame()
    fr_login.grid(row=0,rowspan=2,column=0,sticky='news')
    fr_login.columnconfigure(0, weight=1)
    fr_login.columnconfigure(1, weight=1)
    fr_login.rowconfigure(0, weight=1)

    fr1 = LabelFrame(fr_login,bd=0)
    fr1.grid(row=0,column=0,sticky="news")
    fr1.rowconfigure(0, weight=1)
    fr1.columnconfigure(0, weight=1)

    fr2 = LabelFrame(fr_login,bd=0)
    fr2.grid(row=0,column=1,sticky="news")
    fr2.rowconfigure(0, weight=1)
    fr2.rowconfigure(1, weight=1)
    fr2.rowconfigure(2, weight=1)
    fr2.columnconfigure(1, weight=1)

    fr2_line = LabelFrame(fr2,bg="#b05620",width=2,bd=0)
    fr2_line.grid(row=1,column=0,sticky="news")

    fr2_1 = LabelFrame(fr2,bd=0)
    fr2_1.grid(row=1,column=1,sticky="news")
    fr2_1.columnconfigure(0, weight=1)
    fr2_1.columnconfigure(1, weight=1)

    username = StringVar()
    password = StringVar()

    logo_image = resize_image("images/icons/shop.png", 350, 350)
    logo_image_frame = Label(fr1)
    logo_image_frame.image = logo_image
    logo_image_frame['image'] = logo_image_frame.image
    logo_image_frame.grid(row=0,column=0,sticky='news')

    Label(fr2_1, text="LOGIN", font='Tahoma 28 bold', fg='#b05620').grid(row=0, columnspan=3, pady=(50,10))

    Label(fr2_1, text="Username :", font='Tahoma 14 ', fg='#ce7435').grid(row=1, column=0, sticky='e', pady=20, padx=10)
    username_entry = Entry(fr2_1,textvariable=username, font='Tahoma 14 ')
    username_entry .grid(row=1, column=1, sticky='w', pady=20)

    Label(fr2_1, text="Password :", font='Tahoma 14 ', fg='#ce7435').grid(row=2, column=0, sticky='e', pady=2, padx=10)
    password_entry = Entry(fr2_1, textvariable=password, font='Tahoma 14 ', show="*")
    password_entry.grid(row=2, column=1, sticky='w', pady=2)
    Button(fr2_1, text="Login",font='Tahoma 12 bold',command=gogogo, width=15, height=0,bg="#b05620",fg="white",pady=5).grid(row=4, columnspan=2, pady=20)

root = Tk()
root.geometry('950x500')
root.resizable(False, False)
root.columnconfigure(0, weight=1)
root.title('Pixel Shop')
root.iconphoto(False, PhotoImage(file='images/icons/favicon.png'))
root.rowconfigure(1, weight=1)

account = []
login()

root.mainloop()