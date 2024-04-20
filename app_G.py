import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('400x400')
        self.root.title("Welcome")
        self.root.configure(bg='#0e101c')

        welcome_label = tk.Label(self.root, text="WELCOME", fg="#fff", font=("Arial", 24), bg='#0e101c')
        welcome_label.pack(pady=(20, 10))

        sign_in_frame = tk.Frame(self.root, bg='#0e101c')
        sign_in_frame.pack()

        sign_in_label = tk.Label(sign_in_frame, text="Sign In", fg="#fff", font=("Arial", 18), bg='#0e101c')
        sign_in_label.pack()

        username_frame = tk.Frame(sign_in_frame, bg='#0e101c')
        username_frame.pack()

        username_label = tk.Label(username_frame, text="Tài Khoản", fg="#fff", bg='#0e101c')
        username_label.pack(side=tk.LEFT, padx=10)

        self.username_entry = tk.Entry(username_frame)
        self.username_entry.pack(side=tk.LEFT, padx=10)

        password_frame = tk.Frame(sign_in_frame, bg='#0e101c')
        password_frame.pack()

        password_label = tk.Label(password_frame, text="Mật Khẩu", fg="#fff", bg='#0e101c')
        password_label.pack(side=tk.LEFT, padx=10)

        self.password_entry = tk.Entry(password_frame, show='•')
        self.password_entry.pack(side=tk.LEFT, padx=10)

        login_button = tk.Button(sign_in_frame, text="LOGIN", command=self.check_credentials, bg='#1cb5ac', fg='#fff')
        login_button.pack(pady=(20, 5), ipadx=10)

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
                Main()
            else:
                messagebox.showinfo("Login info", "Incorrect credentials")

            mydb.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database error", "Something went wrong: {}".format(err))

class Main:
    def __init__(self):
        # Kết nối đến cơ sở dữ liệu
        self.db_connection = mysql.connector.connect(user='root', password='26072003', host='localhost', database='sneakershop')
        self.cursor = self.db_connection.cursor()
        
        self.cart = Cart()

        # Cửa sổ
        self.root = tk.Tk()
        self.root.title('Quản lí sản phẩm giày')
        self.root.geometry('1000x300')
        self.root.resizable(False, False)

        # Menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Thoát", command=self.exit_program)
        self.menu_bar.add_cascade(label="Menu", menu=self.file_menu)

        # Khung
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP)

        # Tìm kiếm
        self.search_label = tk.Label(self.frame, text="Tìm kiếm:")
        self.search_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_button = tk.Button(self.frame, text='Tìm kiếm', width=10, command=self.search_data)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        # Button làm mới
        self.refresh_button = tk.Button(self.frame, text='Làm mới', width=10, command=self.show_data)
        self.refresh_button.grid(row=0, column=3, padx=5, pady=5)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=('id', 'name', 'size', 'brand', 'price', 'quantity'), show='headings', height=5)
        self.tree.heading('id', text='Mã sản phẩm', anchor='center')
        self.tree.heading('name', text='Tên sản phẩm', anchor='center')
        self.tree.heading('size', text='Kích thước', anchor='center')
        self.tree.heading('brand', text='Hãng', anchor='center')
        self.tree.heading('price', text='Giá', anchor='center')
        self.tree.heading('quantity', text='Số lượng', anchor='center')
        self.tree.pack(fill='both', expand=True)

        # Tải dữ liệu từ cơ sở dữ liệu
        self.show_data()

        # Các nút
        self.add_button = tk.Button(self.root, text='Thêm', width=20, command=self.open_add_window)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.delete_button = tk.Button(self.root, text='Xóa', width=20, command=self.delete_data)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.edit_button = tk.Button(self.root, text='Sửa', width=20, command=self.edit_data)
        self.edit_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.add_to_cart_button = tk.Button(self.root, text='Thêm vào giỏ hàng', command=self.add_to_cart)
        self.add_to_cart_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.view_cart_button = tk.Button(self.root, text='Xem giỏ hàng', command=self.view_cart)
        self.view_cart_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Đặt trọng số của cột trong Treeview để chúng mở rộng tự động
        self.tree.column('#0', width=0, stretch=tk.NO)
        for col in self.tree['columns']:
            self.tree.column(col, width=160, stretch=tk.YES)

        self.root.mainloop()

    def show_data(self):
        # Xóa các mục hiện có trong treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy dữ liệu từ cơ sở dữ liệu và cập nhật treeview
        self.cursor.execute('SELECT * FROM products')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def open_add_window(self):
        # Mở cửa sổ Thêm
        add_window = Add(self.db_connection, self.show_data)

    def delete_data(self):
        delete_window = Delete(self.db_connection, self.show_data)

    def edit_data(self):
         # Lấy mã sản phẩm từ dòng được chọn trong Treeview
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item)['values'][0]  # Giả sử mã sản phẩm là cột đầu tiên
        # Mở cửa sổ chỉnh sửa thông tin sản phẩm
            edit_window = EditProduct(self.db_connection, product_id, self.show_data)
        else:
            messagebox.showerror('Lỗi', 'Vui lòng chọn một sản phẩm để chỉnh sửa.')

    def search_data(self):
        keyword = self.search_entry.get()
        # Xóa các mục hiện có trong treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Tìm kiếm trong cơ sở dữ liệu
        self.cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + keyword + '%',))
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def exit_program(self):
        self.root.destroy()
        
    def add_to_cart(self):
        # Lấy thông tin sản phẩm được chọn từ Treeview
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item)['values'][0]  # Giả sử mã sản phẩm là cột đầu tiên
            name = self.tree.item(selected_item)['values'][1]  # Giả sử tên sản phẩm là cột thứ hai
            price = self.tree.item(selected_item)['values'][4]  # Giả sử giá sản phẩm là cột thứ năm
            quantity = 1  # Số lượng mặc định khi thêm vào giỏ hàng là 1

            # Thêm sản phẩm vào giỏ hàng
            self.cart.add_item(product_id, name, quantity, price)

            # Hiển thị thông báo xác nhận đã thêm vào giỏ hàng
            messagebox.showinfo('Thông báo', f'Đã thêm sản phẩm "{name}" vào giỏ hàng.')

            self.view_cart()
        else:
            messagebox.showerror('Lỗi', 'Vui lòng chọn một sản phẩm để thêm vào giỏ hàng.')
            
    def view_cart(self):
        # Tạo một cửa sổ hoặc cảnh báo để hiển thị giỏ hàng
        cart_window = tk.Toplevel(self.root)
        cart_window.title('Giỏ hàng')

        # Hiển thị danh sách các mặt hàng trong giỏ hàng
        cart_label = tk.Label(cart_window, text='Danh sách sản phẩm trong giỏ hàng:')
        cart_label.pack()

        cart_listbox = tk.Listbox(cart_window)
        for product_id, item_info in self.cart.items.items():
            product_info = f"{item_info['name']} - Số lượng: {item_info['quantity']} - Giá: {item_info['price']}đ"
            cart_listbox.insert(tk.END, product_info)
        cart_listbox.pack()

        # Hiển thị tổng tiền của giỏ hàng
        total_label = tk.Label(cart_window, text=f'Tổng tiền: {self.cart.get_total()}đ')
        total_label.pack()

        # Thêm nút thanh toán vào cửa sổ giỏ hàng
        checkout_button = tk.Button(cart_window, text='Thanh toán', command=self.checkout)
        checkout_button.pack()

    # Phương thức thanh toán
    def checkout(self):
        total_amount = self.cart.get_total()
        # Thực hiện các bước thanh toán ở đây, ví dụ:
        # - Lưu thông tin đơn hàng vào cơ sở dữ liệu
        # - Hiển thị thông báo xác nhận
        # - Xóa giỏ hàng hoặc cập nhật trạng thái đơn hàng

        # Sau khi thanh toán, có thể cập nhật lại giao diện hoặc thực hiện các hành động khác

        # Ví dụ: Xóa giỏ hàng sau khi thanh toán
        self.cart.clear_cart()

        # Hiển thị thông báo xác nhận
        messagebox.showinfo('Thông báo', 'Đơn hàng của bạn đã được thanh toán thành công!')
        self.cart.clear_cart()
        # Đóng cửa sổ giỏ hàng
        CartWindow.destroy()

        # Cập nhật lại giao diện chính (nếu cần)
        self.show_data()
        # Sau khi thanh toán, đóng cửa sổ giỏ hàng
        if self.cart_window:
            self.cart_window.destroy()

class Add:
    def __init__(self, db_connection, update_callback):
        self.db_connection = db_connection
        self.update_callback = update_callback

        # Window
        self.root = tk.Tk()
        self.root.title('Thêm sản phẩm')
        self.root.geometry('300x230')

        # Labels và Entries
        tk.Label(self.root, text='Tên sản phẩm:').grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.root, text='Kích thước:').grid(row=1, column=0)
        self.size_entry = tk.Entry(self.root)
        self.size_entry.grid(row=1, column=1)

        tk.Label(self.root, text='Hãng:').grid(row=2, column=0)
        self.brand_entry = tk.Entry(self.root)
        self.brand_entry.grid(row=2, column=1)

        tk.Label(self.root, text='Giá:').grid(row=3, column=0)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=3, column=1)

        tk.Label(self.root, text='Số lượng:').grid(row=4, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=4, column=1)

        # Button
        tk.Button(self.root, text='Thêm', command=self.add_product).grid(row=5, column=0, columnspan=2)

    def add_product(self):
        name = self.name_entry.get()
        size = self.size_entry.get()
        brand = self.brand_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        # Connect to database
        cursor = self.db_connection.cursor()

        # Insert data into database
        cursor.execute('INSERT INTO products (name, size, brand, price, quantity) VALUES (%s, %s, %s, %s, %s)', (name, size, brand, price, quantity))
        self.db_connection.commit()

        # Close the connection
        cursor.close()

        # Call the update_callback function to update the treeview in the main window
        self.update_callback()

        # Close the add window
        self.root.destroy()

class EditProduct:
    def __init__(self, db_connection, product_id, update_callback):
        self.db_connection = db_connection
        self.product_id = product_id
        self.update_callback = update_callback

        self.cursor = self.db_connection.cursor()

        self.root = tk.Tk()
        self.root.title('Chỉnh sửa sản phẩm')
        self.root.geometry('300x200')

        self.label_name = tk.Label(self.root, text='Tên sản phẩm:')
        self.label_name.grid(row=0, column=0)
        self.entry_name = tk.Entry(self.root)
        self.entry_name.grid(row=0, column=1)

        self.label_size = tk.Label(self.root, text='Kích thước:')
        self.label_size.grid(row=1, column=0)
        self.entry_size = tk.Entry(self.root)
        self.entry_size.grid(row=1, column=1)

        self.label_brand = tk.Label(self.root, text='Hãng:')
        self.label_brand.grid(row=2, column=0)
        self.entry_brand = tk.Entry(self.root)
        self.entry_brand.grid(row=2, column=1)

        self.label_price = tk.Label(self.root, text='Giá:')
        self.label_price.grid(row=3, column=0)
        self.entry_price = tk.Entry(self.root)
        self.entry_price.grid(row=3, column=1)
        
        self.label_quantity = tk.Label(self.root, text='Số lượng:')
        self.label_quantity.grid(row=4, column=0)
        self.entry_quantity = tk.Entry(self.root)
        self.entry_quantity.grid(row=4, column=1)

        self.button_save = tk.Button(self.root, text='Lưu', command=self.save_product)
        self.button_save.grid(row=5, column=0, columnspan=2)

        # Load existing product information
        self.load_product_info()

    def load_product_info(self):
        # Retrieve product information from the database based on product_id
        self.cursor.execute('SELECT name, size, brand, price, quantity FROM products WHERE id = %s', (self.product_id,))
        product_info = self.cursor.fetchone()

        # Fill entry fields with existing product information
        if product_info:
            self.entry_name.insert(0, product_info[0])
            self.entry_size.insert(0, product_info[1])
            self.entry_brand.insert(0, product_info[2])
            self.entry_price.insert(0, product_info[3])
        else:
            messagebox.showerror('Error', 'Product not found.')

    def save_product(self):
        # Retrieve updated product information from entry fields
        name = self.entry_name.get()
        size = self.entry_size.get()
        brand = self.entry_brand.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()

        # Update product information in the database
        self.cursor.execute('UPDATE products SET name = %s, size = %s, brand = %s, price = %s, quantity = %s WHERE id = %s',
                            (name, size, brand, price, quantity, self.product_id))
        self.db_connection.commit()
        
        # Call the update_callback function to update the main window
        self.update_callback()

        # Close the edit window
        self.root.destroy()

class Delete:
    def __init__(self, db_connection, update_callback):
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.update_callback = update_callback

        # Tạo cửa sổ
        self.root = tk.Tk()
        self.root.title('Xóa sản phẩm')
        self.root.geometry('300x150')

        # Label và Entry cho mã sản phẩm
        tk.Label(self.root, text='Mã sản phẩm:').grid(row=0, column=0)
        self.product_id_entry = tk.Entry(self.root)
        self.product_id_entry.grid(row=0, column=1)

        # Nút xóa
        tk.Button(self.root, text='Xóa', command=self.delete_product).grid(row=1, column=0, columnspan=2)

    def delete_product(self):
        product_id = self.product_id_entry.get()

        if not product_id:
            messagebox.showerror('Lỗi', 'Vui lòng nhập mã sản phẩm.')
            return

        # Xác nhận việc xóa sản phẩm
        confirmation = messagebox.askyesno('Xác nhận', 'Bạn có chắc chắn muốn xóa sản phẩm này?')

        if confirmation:
            try:
                # Xóa sản phẩm từ cơ sở dữ liệu
                self.cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
                self.db_connection.commit()

                # Cập nhật treeview trong cửa sổ chính
                self.update_callback()

                messagebox.showinfo('Thông báo', 'Đã xóa sản phẩm thành công.')
            except mysql.connector.Error as error:
                messagebox.showerror('Lỗi', f'Lỗi khi xóa sản phẩm: {error}')

        # Đóng cửa sổ
        self.root.destroy()
        
class Cart:
    def __init__(self):
        self.items = {}  # Dùng một từ điển để lưu trữ sản phẩm trong giỏ hàng

    def add_item(self, product_id, name, quantity, price):
        quantity = int(quantity)
        price = float(price)
        self.items[product_id] = {'name': name, 'quantity': quantity, 'price': price}
        if product_id in self.items:
            self.items[product_id]['quantity'] += quantity
        else:
            self.items[product_id] = {'name': name, 'quantity': quantity, 'price': price}

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
        else:
            print("Sản phẩm không tồn tại trong giỏ hàng.")

    def clear_cart(self):
        self.items = {}

    def get_total(self):
        total = 0
        for item in self.items.values():
            total += item['quantity'] * item['price']
        return total
    
class CartWindow:
     def __init__(self, parent, cart):
         self.parent = parent
         self.cart = cart

         self.root = tk.Toplevel(parent)
         self.root.title('Giỏ hàng')

         # Treeview để hiển thị danh sách sản phẩm trong giỏ hàng
         self.cart_tree = ttk.Treeview(self.root, columns=('id', 'name', 'price'))
         self.cart_tree.heading('id', text='Mã SP')
         self.cart_tree.heading('name', text='Tên sản phẩm')
         self.cart_tree.heading('price', text='Giá')
         self.cart_tree.pack(expand=True, fill=tk.BOTH)

         # Thêm dữ liệu sản phẩm vào Treeview
         self.populate_cart()

     def populate_cart(self):
         for item_id, item_info in self.cart_items.items():
             self.cart_tree.insert('', 'end', values=(item_id, item_info['name'], item_info['price']))

if __name__ == "__main__":
    app = LoginApp()