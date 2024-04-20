import tkinter as tk
from tkinter import ttk
import mysql.connector

class Add:
    def __init__(self, db_connection, show_data, main_obj):
        self.db_connection = db_connection
        self.update_callback = show_data

        self.root = tk.Tk()
        self.root.title('Thêm sản phẩm')
        self.root.geometry('300x200')

        tk.Label(self.root, text='Mã sản phẩm:').grid(row=0, column=0)
        self.userid_entry = tk.Entry(self.root)
        self.userid_entry.grid(row=0, column=1)

        tk.Label(self.root, text='Tên sản phẩm:').grid(row=1, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self.root, text='Kích thước:').grid(row=2, column=0)
        self.size_entry = tk.Entry(self.root)
        self.size_entry.grid(row=2, column=1)

        tk.Label(self.root, text='Hãng:').grid(row=3, column=0)
        self.brand_entry = tk.Entry(self.root)
        self.brand_entry.grid(row=3, column=1)

        tk.Label(self.root, text='Giá:').grid(row=4, column=0)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=4, column=1)

        tk.Label(self.root, text='Số lượng:').grid(row=5, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=5, column=1)

        tk.Button(self.root, text='Thêm', command=self.add_product).grid(row=6, column=0, columnspan=2)

    def add_product(self):
        userid= self.userid_entry.get()
        name = self.name_entry.get()
        size = self.size_entry.get()
        brand = self.brand_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        cursor = self.db_connection.cursor()

        cursor.execute('INSERT INTO products (userid, name, size, brand, price) VALUES (%s,%s, %s, %s, %s, %s)', (userid,name, size, brand, price,quantity))
        self.db_connection.commit()

        cursor.close()

        self.update_callback()

        self.root.destroy()
