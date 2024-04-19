from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
class CartWindow:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()

        self.root = Tk()
        self.root.title('Giỏ hàng')
        self.root.geometry('800x500')
        self.root.resizable(False, False)

        self.frame = Frame(self.root)
        self.frame.pack()

        self.tree_cart = ttk.Treeview(self.frame, columns=('id', 'name', 'size', 'brand', 'price', 'quantity'), show='headings', height=5)
        # Đặt heading cho các cột
        self.tree_cart.heading('id', text='Mã sản phẩm', anchor='center')
        self.tree_cart.heading('name', text='Tên sản phẩm', anchor='center')
        self.tree_cart.heading('size', text='Kích thước', anchor='center')
        self.tree_cart.heading('brand', text='Hãng', anchor='center')
        self.tree_cart.heading('price', text='Giá', anchor='center')
        self.tree_cart.heading('quantity', text='Số lượng', anchor='center')
        self.tree_cart.pack(fill='both', expand=True)

        # Nút Hủy giỏ hàng
        self.cancel_button = Button(self.frame, text='Hủy giỏ hàng', width=20, command=self.cancel_cart)
        self.cancel_button.pack(side=LEFT)

        # Nút Thanh toán
        self.pay_button = Button(self.frame, text='Thanh toán', width=20, command=self.pay_and_print_bill)
        self.pay_button.pack(side=RIGHT)

        self.show_cart_items()

        self.root.mainloop()

    def show_cart_items(self):
        # Lấy dữ liệu sản phẩm từ cơ sở dữ liệu và hiển thị lên treeview
        self.tree_cart.delete(*self.tree_cart.get_children())  # Xóa dữ liệu hiện tại trong treeview

        self.cursor.execute('SELECT * FROM cart')
        cart_items = self.cursor.fetchall()
        for item in cart_items:
            product_id = item[0]  # Mã sản phẩm
            quantity = item[1]  # Số lượng
            # Lấy thông tin sản phẩm từ bảng products
            self.cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
            product_info = self.cursor.fetchone()
            if product_info:
                # Hiển thị thông tin sản phẩm lên treeview
                self.tree_cart.insert('', 'end', values=(product_info[0], product_info[1], product_info[2], product_info[3], product_info[4], quantity))

    def cancel_cart(self):
        # Xóa toàn bộ sản phẩm trong giỏ hàng
        self.cursor.execute('DELETE FROM cart')
        self.db_connection.commit()
        messagebox.showinfo('Thông báo', 'Đã hủy giỏ hàng thành công.')
        # Cập nhật lại treeview
        self.show_cart_items()

    def pay_and_print_bill(self):
        # Thực hiện thanh toán và in hóa đơn
        # Giả sử bạn muốn in hóa đơn vào file 'bill.txt'
        bill_file = open('bill.txt', 'w')
        total_price = 0
        self.cursor.execute('SELECT * FROM cart')
        cart_items = self.cursor.fetchall()
        for item in cart_items:
            product_id = item[0]
            quantity = item[1]
            # Lấy thông tin sản phẩm từ bảng products
            self.cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
            product_info = self.cursor.fetchone()
            if product_info:
                product_name = product_info[1]
                product_price = product_info[4]
                total_price += product_price * quantity
                # In thông tin sản phẩm và số lượng vào hóa đơn
                bill_file.write(f"{product_name}: {quantity} x {product_price}\n")
        # In tổng số tiền
        bill_file.write(f"Tổng cộng: {total_price}")
        bill_file.close()
        # Xóa giỏ hàng sau khi thanh toán
        self.cursor.execute('DELETE FROM cart')
        self.db_connection.commit()
        messagebox.showinfo('Thông báo', 'Đã thanh toán thành công và in hóa đơn.')
        # Cập nhật lại treeview
        self.show_cart_items()

if __name__ == "__main__":
    db_connection = mysql.connector.connect(user='root', password='26072003', host='localhost', database='sneakershop')

    def update_treeview():
        # Update the treeview with new data from the database
        pass  # Your code to update the treeview goes here

    add_window = CartWindow(db_connection, update_treeview)
    add_window.root.mainloop()

