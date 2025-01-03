import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

def connect_database():
    conn = sqlite3.connect('product.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            Id INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Price REAL NOT NULL,
            Amount INTEGER NOT NULL
        )
    ''')
    conn.commit()
    return conn

def add_product():
    name = entry_name.get()
    try:
        price = float(entry_price.get())
        amount = int(entry_amount.get())
        cursor = conn.cursor()
        cursor.execute("INSERT INTO product (Name, Price, Amount) VALUES (?, ?, ?)", (name, price, amount))
        conn.commit()
        messagebox.showinfo("Thành công", "Đã thêm sản phẩm mới.")
        show_products()
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng cho giá và số lượng.")

def show_products():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    rows = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", "end", values=row)

def search_product():
    name = entry_name.get()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE Name LIKE ?", ('%' + name + '%',))
    rows = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", "end", values=row)

def update_product():
    try:
        selected = tree.selection()[0]
        values = tree.item(selected, "values")
        product_id = values[0]
        new_price = float(entry_price.get())
        new_amount = int(entry_amount.get())
        cursor = conn.cursor()
        cursor.execute("UPDATE product SET Price = ?, Amount = ? WHERE Id = ?", (new_price, new_amount, product_id))
        conn.commit()
        messagebox.showinfo("Thành công", "Đã cập nhật sản phẩm.")
        show_products()
    except IndexError:
        messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để cập nhật.")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng cho giá và số lượng.")

def delete_product():
    try:
        selected = tree.selection()[0]
        values = tree.item(selected, "values")
        product_id = values[0]
        cursor = conn.cursor()
        cursor.execute("DELETE FROM product WHERE Id = ?", (product_id,))
        conn.commit()
        messagebox.showinfo("Thành công", "Đã xóa sản phẩm.")
        show_products()
    except IndexError:
        messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để xóa.")

root = tk.Tk()
root.title("Quản Lý Sản Phẩm")

conn = connect_database()

tk.Label(root, text="Tên sản phẩm:").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Giá sản phẩm:").grid(row=1, column=0, padx=10, pady=5)
entry_price = tk.Entry(root)
entry_price.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Số lượng:").grid(row=2, column=0, padx=10, pady=5)
entry_amount = tk.Entry(root)
entry_amount.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Thêm", command=add_product).grid(row=3, column=0, padx=10, pady=5)
tk.Button(root, text="Tìm kiếm", command=search_product).grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Cập nhật", command=update_product).grid(row=4, column=0, padx=10, pady=5)
tk.Button(root, text="Xóa", command=delete_product).grid(row=4, column=1, padx=10, pady=5)

tree = ttk.Treeview(root, columns=("ID", "Tên", "Giá", "Số lượng"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Tên", text="Tên sản phẩm")
tree.heading("Giá", text="Giá sản phẩm")
tree.heading("Số lượng", text="Số lượng")
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

show_products()

root.mainloop()

conn.close()