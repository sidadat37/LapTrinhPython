from tkinter import *
from tkinter import messagebox
import mysql.connector

class Delete:
    def __init__(self, db_connection, update_callback):
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.update_callback = update_callback

        # Tạo cửa sổ
        self.root = Tk()
        self.root.title('Xóa sản phẩm')
        self.root.geometry('300x150')

        # Label và Entry cho mã sản phẩm
        Label(self.root, text='Mã sản phẩm:').grid(row=0, column=0)
        self.product_id_entry = Entry(self.root)
        self.product_id_entry.grid(row=0, column=1)

        # Nút xóa
        self.delete_button = Button(self.root, text='Xóa', command=self.delete_product)
        self.delete_button.grid(row=1, column=0, columnspan=2)

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

if __name__ == "__main__":
    # Kết nối đến cơ sở dữ liệu
    db_connection = mysql.connector.connect(user='root', password='26072003', host='localhost', database='sneakershop')

    # Hàm cập nhật treeview trong cửa sổ chính
    def update_treeview():
        pass  # Thay bằng mã để cập nhật treeview

    # Mở cửa sổ xóa sản phẩm
    delete_window = Delete(db_connection, update_treeview)
    delete_window.root.mainloop()
