import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "samtronic.db")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS repairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            description TEXT,
            price INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    conn.commit()
    conn.close()

def fetch_customers():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, first_name, last_name FROM customers")
    customers = c.fetchall()
    conn.close()
    return customers

def save_repair(customer_id, description, price, tree):
    if not customer_id or not description or not price:
        messagebox.showwarning("خطا", "لطفاً تمام فیلدها را پر کنید.")
        return

    try:
        price = int(price)
    except ValueError:
        messagebox.showerror("خطا", "قیمت باید عدد باشد.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO repairs (customer_id, description, price) VALUES (?, ?, ?)",
              (customer_id, description, price))
    conn.commit()
    conn.close()

    messagebox.showinfo("ثبت شد", "تعمیر با موفقیت ذخیره شد.")
    show_repairs(tree)

def show_repairs(tree):
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT repairs.id, customers.first_name || ' ' || customers.last_name, repairs.description, repairs.price, repairs.date
        FROM repairs
        JOIN customers ON repairs.customer_id = customers.id
        ORDER BY repairs.date DESC
    """)
    rows = c.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=row)

def run():
    create_tables()

    win = tk.Toplevel()
    win.title("ثبت تعمیرات")
    win.geometry("700x450")

    frame = ttk.Frame(win, padding=10)
    frame.pack(fill="both", expand=True)

    # مشتری‌ها
    ttk.Label(frame, text="مشتری:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    customer_combo = ttk.Combobox(frame, width=30)
    customer_data = fetch_customers()
    customer_combo["values"] = [f"{id} - {name} {lname}" for id, name, lname in customer_data]
    customer_combo.grid(row=0, column=1, padx=5, pady=5)

    # توضیح
    ttk.Label(frame, text="شرح تعمیر:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    desc_entry = ttk.Entry(frame, width=40)
    desc_entry.grid(row=1, column=1, padx=5, pady=5)

    # قیمت
    ttk.Label(frame, text="قیمت (تومان):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    price_entry = ttk.Entry(frame, width=20)
    price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # دکمه ثبت
    ttk.Button(frame, text="ثبت تعمیر", command=lambda: save_repair(
        int(customer_combo.get().split(" - ")[0]), desc_entry.get(), price_entry.get(), tree)
    ).grid(row=3, column=0, columnspan=2, pady=10)

    # جدول نمایش تعمیرات
    columns = ("id", "customer", "description", "price", "date")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.grid(row=4, column=0, columnspan=2, pady=10)

    show_repairs(tree)
    win.mainloop()