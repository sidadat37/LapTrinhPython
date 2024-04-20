import tkinter as tk
from tkinter import ttk
import mysql.connector

class CartWindow:
    def __init__(self, db_connection):
        self.db_connection = db_connection

        self.root = tk.Tk()
        self.root.title('Giỏ hàng')
        self.root.geometry('400x300')

        self.tree = ttk.Treeview(self.root, columns=('id', 'name', 'size', 'brand', 'price', 'quantity'), show='headings', height=5)
        self.tree.heading('id', text='Mã sản phẩm', anchor='center')
        self.tree.heading('name', text='Tên sản phẩm', anchor='center')
        self.tree.heading('size', text='Kích thước', anchor='center')
        self.tree.heading('brand', text='Hãng', anchor='center')
        self.tree.heading('price', text='Giá', anchor='center')
        self.tree.heading('quantity', text='Số lượng', anchor='center')
        self.tree.pack(fill='both', expand=True)

        self.show_cart()

        self.root.mainloop()

    def show_cart(self):
        cursor = self.db_connection.cursor()

        cursor.execute('SELECT products.id, products.name, products.size, products.brand, products.price, cart.quantity FROM products INNER JOIN cart ON products.id = cart.productid')
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)

        cursor.close()
