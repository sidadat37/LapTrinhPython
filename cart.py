from tkinter import *
from tkinter import ttk
import mysql.connector 
from main import Main 

class Cart:
    def __init__(self, db_connection, update_callback):
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.update_callback = update_callback

        self.root = Tk()
        self.root.title('Giỏ hàng')
        self.root.geometry('800x500')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.frame1 = Frame(self.root)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame1.columnconfigure(0, weight=1)

        self.frame2 = Frame(self.root)
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.frame2.columnconfigure(0, weight=1)

        self.tree_cart = ttk.Treeview(self.frame1, columns=('cartid', 'username'), show='headings', height=5, width=400)
        self.tree_cart.heading('cartid', text='Mã sản phẩm', anchor='center')
        self.tree_cart.heading('username', text='Tên người dùng', anchor='center')
        self.tree_cart.pack(fill='both', expand=True)

        self.tree_cart.bind('<<TreeviewSelect>>', self.show_cart_items)

        self.tree_products_in_cart = ttk.Treeview(self.frame2, columns=('productid', 'productname', 'size', 'brand', 'price', 'quantity'), show='headings', height=5, width=400)
        self.tree_products_in_cart.heading('productid', text='Mã sản phẩm', anchor='center')
        self.tree_products_in_cart.heading('productname', text='Tên sản phẩm', anchor='center')
        self.tree_products_in_cart.heading('size', text='Kích thước', anchor='center')
        self.tree_products_in_cart.heading('brand', text='Hãng', anchor='center')
        self.tree_products_in_cart.heading('price', text='Giá', anchor='center')
        self.tree_products_in_cart.heading('quantity', text='Số lượng', anchor='center')
        self.tree_products_in_cart.pack(fill='both', expand=True)

        self.show_cart()

        self.root.mainloop()

    def show_cart(self):
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)

        self.cursor.execute('SELECT * FROM cart')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree_cart.insert('', 'end', values=row)

    def show_cart_items(self, event):
        selected_item = self.tree_cart.selection()
        if selected_item:
            self.tree_products_in_cart.delete(*self.tree_products_in_cart.get_children())
            cart_id = self.tree_cart.item(selected_item)['values'][0]  # Assuming cart id is the first column
            self.cursor.execute('SELECT * FROM cart WHERE cartid = %s', (cart_id,))
            cart_items = self.cursor.fetchall()
            for item in cart_items:
                product_id = item[2]  # Assuming product id is the third column
                self.cursor.execute('SELECT * FROM products WHERE productid = %s', (product_id,))
                product_info = self.cursor.fetchone()
                if product_info:
                    self.tree_products_in_cart.insert('', 'end', values=product_info)

if __name__ == "__main__":
    db_connection = mysql.connector.connect(user='root', password='26072003', host='localhost', database='sneakershop')

    cart_window = Cart(db_connection, Main.show_data)
    cart_window.root.mainloop()
