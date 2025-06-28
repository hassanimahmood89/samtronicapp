import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "samtronic.db")

def fetch_invoices():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT customers.first_name || ' ' || customers.last_name AS name,
               repairs.description,
               repairs.price,
               repairs.date
        FROM repairs
        JOIN customers ON customers.id = repairs.customer_id
        ORDER BY repairs.date DESC
        LIMIT 20
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def run():
    win = tk.Toplevel()
    win.title("صدور فاکتور")
    win.geometry("650x450")

    title = ttk.Label(win, text="فاکتورهای اخیر", font=("Tahoma", 16))
    title.pack(pady=10)

    columns = ("name", "description", "price", "date")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    tree.pack(padx=10, pady=10)

    def print_invoice():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("خطا", "لطفاً یک ردیف را انتخاب کنید.")
            return

        values = tree.item(selected[0], "values")
        output = f"""********* سامترونیک *********
مشتری: {values[0]}
توضیح: {values[1]}
قیمت: {values[2]} تومان
تاریخ: {values[3]}

با تشکر از اعتماد شما.
------------------------------"""
        messagebox.showinfo("چاپ فاکتور", output)

    ttk.Button(win, text="نمایش فاکتور انتخاب‌شده", command=print_invoice).pack(pady=10)

    rows = fetch_invoices()
    for row in rows:
        tree.insert("", "end", values=row)

    win.mainloop()