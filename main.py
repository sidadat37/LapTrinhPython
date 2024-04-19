from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector 
from add import Add
from delete import Delete
from edit import EditProduct

class Main:
    def __init__(self):
        # Kết nối đến cơ sở dữ liệu
        self.db_connection = mysql.connector.connect(user='root', password='26072003', host='localhost', database='sneakershop')
        self.cursor = self.db_connection.cursor()

        # Cửa sổ
        self.root = Tk()
        self.root.title('Quản lí sản phẩm giày')
        self.root.geometry('800x300')
        self.root.resizable(False, False)

        # Khung
        self.frame = Frame(self.root)
        self.frame.pack(side=LEFT)

        # Treeview
        self.tree = ttk.Treeview(self.frame, columns=('id', 'name', 'size', 'brand', 'price'), show='headings', height=5)
        self.tree.heading('id', text='Mã sản phẩm', anchor='center')
        self.tree.heading('name', text='Tên sản phẩm', anchor='center')
        self.tree.heading('size', text='Kích thước', anchor='center')
        self.tree.heading('brand', text='Hãng', anchor='center')
        self.tree.heading('price', text='Giá', anchor='center')
        self.tree.pack(fill='both', expand=True)

        # Tải dữ liệu từ cơ sở dữ liệu
        self.show_data()

        # Các nút
        self.add_button = Button(self.frame, text='Thêm', width=20, command=self.open_add_window)
        self.add_button.pack(side=RIGHT)
        self.delete_button = Button(self.frame, text='Xóa', width=20, command=self.delete_data)
        self.delete_button.pack(side=RIGHT)
        self.edit_button = Button(self.frame, text='Sửa', width=20, command=self.edit_data)
        self.edit_button.pack(side=RIGHT)

        # Đặt trọng số của cột trong Treeview để chúng mở rộng tự động
        self.tree.column('#0', width=0, stretch=NO)
        for col in self.tree['columns']:
            self.tree.column(col, width=160, stretch=YES)

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

if __name__ == "__main__":
    main_obj = Main()