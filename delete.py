import tkinter as tk
from tkinter import ttk
import mysql.connector

class Delete:
    def __init__(self, db_connection, show_data):
        self.db_connection = db_connection
        self.update_callback = show_data

        self.root = tk.Tk()
        self.root.title('Xóa sản phẩm')
        self.root.geometry('200x100')

        tk.Label(self.root, text='Mã sản phẩm:').pack()
        self.product_id_entry = tk.Entry(self.root)
        self.product_id_entry.pack()

        tk.Button(self.root, text='Xóa', command=self.delete_product).pack()

    def delete_product(self):
        product_id = self.product_id_entry.get()

        cursor = self.db_connection.cursor()

        cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
        self.db_connection.commit()

        cursor.close()

        self.update_callback()

        self.root.destroy()
