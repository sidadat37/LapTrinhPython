import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector 

class LoginForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('300x200')
        self.root.title("Login")
        self.root.configure(bg='light blue')

        title_label = tk.Label(self.root, text= "Login", fg= "red", font=("cambria",16), width=25, bg='light blue')
        title_label.pack(pady=10)

        username_label = tk.Label(self.root, text="Username", bg='light blue')
        username_label.pack()

        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        password_label = tk.Label(self.root, text="Password", bg='light blue')
        password_label.pack()

        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()

        submit_button = tk.Button(self.root, text="Submit", command=self.check_credentials, bg='light green')
        submit_button.pack(pady=10)

        self.root.mainloop()

    def check_credentials(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="26072003",
                database="sneakershop"
            )

            mycursor = mydb.cursor()

            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            val = (self.username_entry.get(), self.password_entry.get())

            mycursor.execute(sql, val)

            result = mycursor.fetchone()

            if result:
                messagebox.showinfo("Login info", "Welcome " + str(result[1]) + "!")
                self.root.destroy()
                Main(result[1])  # Truyền tên người dùng sang Main
            else:
                messagebox.showinfo("Login info", "Incorrect credentials")

            mydb.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database error", "Something went wrong: {}".format(err))

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

        # Kiểm tra xem sản phẩm đã tồn tại trong giỏ hàng của người dùng hay chưa
            self.cursor.execute('SELECT * FROM cart WHERE userid = %s AND productid = %s', (userid, productid))
            existing_row = self.cursor.fetchone()

            if existing_row:
            # Nếu sản phẩm đã tồn tại trong giỏ hàng, cập nhật số lượng
                new_quantity = existing_row[2] + 1
                self.cursor.execute('UPDATE cart SET quantity = %s WHERE userid = %s AND productid = %s', (new_quantity, userid, productid))
            else:
            # Nếu sản phẩm chưa tồn tại trong giỏ hàng, thêm mới vào
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

class Add:
    def __init__(self, db_connection, show_data, main_obj):
        self.db_connection = db_connection
        self.update_callback = show_data

        self.root = tk.Tk()
        self.root.title('Thêm sản phẩm')
        self.root.geometry('300x200')

        tk.Label(self.root, text='Mã sản phẩm:').grid(row=0, column=0)
        self.productid_entry = tk.Entry(self.root)
        self.productid_entry.grid(row=0, column=1)

        tk.Label(self.root, text='Tên sản phẩm:').grid(row=1, column=0)
        self.productname_entry = tk.Entry(self.root)
        self.productname_entry.grid(row=1, column=1)

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
        productid= self.productid_entry.get()
        productname = self.productname_entry.get()
        size = self.size_entry.get()
        brand = self.brand_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        cursor = self.db_connection.cursor()

        cursor.execute('INSERT INTO products (productid, productname, size, brand, price, quantity) VALUES (%s,%s, %s, %s, %s, %s)', (productid,productname, size, brand, price,quantity))
        self.db_connection.commit()

        cursor.close()

        self.update_callback()

        self.root.destroy()


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

class CartWindow:
    def __init__(self, db_connection):
        self.db_connection = db_connection

        self.root = tk.Tk()
        self.root.title('Giỏ hàng')
        self.root.geometry('400x200')

        self.tree = ttk.Treeview(self.root, columns=('productid', 'productname', 'size', 'brand', 'price', 'quantity'), show='headings', height=5)
        self.tree.heading('productid', text='Mã sản phẩm', anchor='center')
        self.tree.heading('productname', text='Tên sản phẩm', anchor='center')
        self.tree.heading('size', text='Kích thước', anchor='center')
        self.tree.heading('brand', text='Hãng', anchor='center')
        self.tree.heading('price', text='Giá', anchor='center')
        self.tree.heading('quantity', text='Số lượng', anchor='center')
        self.tree.pack(fill='both', expand=True)

        self.show_cart()

        self.root.mainloop()

    def show_cart(self):
        cursor = self.db_connection.cursor()

        cursor.execute('SELECT products.productid, products.productname, products.size, products.brand, products.price, cart.quantity FROM products INNER JOIN cart ON products.productid = cart.productid')
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)

        cursor.close()
        

if __name__ == "__main__":
    app = LoginForm()