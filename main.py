import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector 
from add import Add
from delete import Delete
from edit import EditProduct
from cart_window import CartWindow

class Main:
    def __init__(self, username):
        self.db_connection = mysql.connector.connect(user='root', password='26072003', host='localhost', database='sneakershop')
        self.cursor = self.db_connection.cursor()

        self.username = username
        self.root = tk.Tk()
        self.root.title('Quản lí sản phẩm giày')
        self.root.geometry('800x300')
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self.frame, columns=('id', 'name', 'size', 'brand', 'price', 'quantity'), show='headings', height=5)
        self.tree.heading('id', text='Mã sản phẩm', anchor='center')
        self.tree.heading('name', text='Tên sản phẩm', anchor='center')
        self.tree.heading('size', text='Kích thước', anchor='center')
        self.tree.heading('brand', text='Hãng', anchor='center')
        self.tree.heading('price', text='Giá', anchor='center')
        self.tree.heading('quantity', text='Số lượng', anchor='center')
        self.tree.pack(fill='both', expand=True)

        self.show_data()

        self.add_button = tk.Button(self.frame, text='Thêm', width=20, command=self.open_add_window)
        self.add_button.pack(side=tk.RIGHT)
        self.delete_button = tk.Button(self.frame, text='Xóa', width=20, command=self.delete_data)
        self.delete_button.pack(side=tk.RIGHT)
        self.edit_button = tk.Button(self.frame, text='Sửa', width=20, command=self.edit_data)
        self.edit_button.pack(side=tk.RIGHT)
        self.add_to_cart_button = tk.Button(self.frame, text='Thêm vào giỏ hàng', width=20, command=self.add_to_cart)
        self.add_to_cart_button.pack(side=tk.RIGHT)
        self.view_cart_button = tk.Button(self.frame, text='Xem giỏ hàng', width=20, command=self.view_cart)
        self.view_cart_button.pack(side=tk.RIGHT)

        self.tree.column('#0', width=0, stretch=tk.NO)
        for col in self.tree['columns']:
            self.tree.column(col, width=160, stretch=tk.YES)

        self.root.mainloop()

    def show_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute('SELECT * FROM products')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def open_add_window(self):
        add_window = Add(self.db_connection, self.show_data, self)

    def delete_data(self):
        delete_window = Delete(self.db_connection, self.show_data)

    def edit_data(self):
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item)['values'][0]
            edit_window = EditProduct(self.db_connection, product_id, self.show_data)
        else:
            messagebox.showerror('Lỗi', 'Vui lòng chọn một sản phẩm để chỉnh sửa.')

    def add_to_cart(self):
        selected_item = self.tree.selection()
        if selected_item:
            productid = self.tree.item(selected_item)['values'][0]
            quantity = 1

            userid = self.get_current_user_id()

            self.cursor.execute('INSERT INTO cart (userid, productid, quantity) VALUES (%s, %s, %s)', (userid, productid, quantity))
            self.db_connection.commit()
            messagebox.showinfo('Thông báo', 'Sản phẩm đã được thêm vào giỏ hàng.')

            self.show_data()
            return
        else:
            messagebox.showerror('Lỗi', 'Vui lòng chọn một sản phẩm để thêm vào giỏ hàng.')

    def get_current_user_id(self):
        current_user_query = "SELECT userid FROM users WHERE username = %s"

        self.cursor.execute(current_user_query, (self.username,))
        user_id = self.cursor.fetchone()[0]

        return user_id

    def view_cart(self):
        cart_window = CartWindow(self.db_connection)

if __name__ == "__main__":
    main_obj = Main("admin")
