from tkinter import *
from tkinter import messagebox
import mysql.connector 

class EditProduct:
    def __init__(self, db_connection, product_id, update_callback):
        self.db_connection = db_connection
        self.product_id = product_id
        self.update_callback = update_callback

        self.cursor = self.db_connection.cursor()

        self.root = Tk()
        self.root.title('Chỉnh sửa sản phẩm')
        self.root.geometry('300x200')

        self.label_name = Label(self.root, text='Tên sản phẩm:')
        self.label_name.grid(row=0, column=0)
        self.entry_name = Entry(self.root)
        self.entry_name.grid(row=0, column=1)

        self.label_size = Label(self.root, text='Kích thước:')
        self.label_size.grid(row=1, column=0)
        self.entry_size = Entry(self.root)
        self.entry_size.grid(row=1, column=1)

        self.label_brand = Label(self.root, text='Hãng:')
        self.label_brand.grid(row=2, column=0)
        self.entry_brand = Entry(self.root)
        self.entry_brand.grid(row=2, column=1)

        self.label_price = Label(self.root, text='Giá:')
        self.label_price.grid(row=3, column=0)
        self.entry_price = Entry(self.root)
        self.entry_price.grid(row=3, column=1)

        self.button_save = Button(self.root, text='Lưu', command=self.save_product)
        self.button_save.grid(row=4, column=0, columnspan=2)

        # Load existing product information
        self.load_product_info()

    def load_product_info(self):
        # Retrieve product information from the database based on product_id
        self.cursor.execute('SELECT name, size, brand, price FROM products WHERE id = %s', (self.product_id,))
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

        # Update product information in the database
        self.cursor.execute('UPDATE products SET name = %s, size = %s, brand = %s, price = %s WHERE id = %s',
                            (name, size, brand, price, self.product_id))
        self.db_connection.commit()
        
        # Call the update_callback function to update the main window
        self.update_callback()

        # Close the edit window
        self.root.destroy()

# Example of usage:
# db_connection = mysql.connector.connect(user='root', password='your_password', host='localhost', database='your_database')
# edit_window = EditProduct(db_connection, product_id, update_callback_function)
# edit_window.root.mainloop()
