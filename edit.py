import tkinter as tk
from tkinter import ttk
import mysql.connector

class EditProduct:
    def __init__(self, db_connection, product_id, show_data):
        self.db_connection = db_connection
        self.product_id = product_id
        self.update_callback = show_data

        self.root = tk.Tk()
        self.root.title('Sửa sản phẩm')
        self.root.geometry('300x200')

        tk.Label(self.root, text='Tên sản phẩm mới:').grid(row=0, column=0)
        self.new_name_entry = tk.Entry(self.root)
        self.new_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text='Kích thước mới:').grid(row=1, column=0)
        self.new_size_entry = tk.Entry(self.root)
        self.new_size_entry.grid(row=1, column=1)

        tk.Label(self.root, text='Hãng mới:').grid(row=2, column=0)
        self.new_brand_entry = tk.Entry(self.root)
        self.new_brand_entry.grid(row=2, column=1)

        tk.Label(self.root, text='Giá mới:').grid(row=3, column=0)
        self.new_price_entry = tk.Entry(self.root)
        self.new_price_entry.grid(row=3, column=1)

        tk.Label(self.root, text='Số lượng mới:').grid(row=4, column=0)
        self.new_quantity_entry = tk.Entry(self.root)
        self.new_quantity_entry.grid(row=4, column=1)

        tk.Button(self.root, text='Sửa', command=self.edit_product).grid(row=5, column=0, columnspan=2)

    def edit_product(self):
        new_name = self.new_name_entry.get()
        new_size = self.new_size_entry.get()
        new_brand = self.new_brand_entry.get()
        new_price = self.new_price_entry.get()
        new_quantity = self.new_quantity_entry.get()

        cursor = self.db_connection.cursor()

        cursor.execute('UPDATE products SET name = %s, size = %s, brand = %s, price = %s, quantity = %s WHERE id = %s',
                       (new_name, new_size, new_brand, new_price, new_quantity, self.product_id))
        self.db_connection.commit()

        cursor.close()

        self.update_callback()

        self.root.destroy()
