import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "samtronic.db")

def search_by_name(name, tree):
    if not name:
        messagebox.showwarning("ورودی ناقص", "لطفاً نام یا نام خانوادگی را وارد کنید.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT customers.first_name || ' ' || customers.last_name AS full_name,
               repairs.description,
               repairs.price,
               repairs.date
        FROM repairs
        JOIN customers ON customers.id = repairs.customer_id
        WHERE customers.first_name LIKE ? OR customers.last_name LIKE ?
        ORDER BY repairs.date DESC
    """, (f"%{name}%", f"%{name}%"))
    results = c.fetchall()
    conn.close()

    tree.delete(*tree.get_children())
    for row in results:
        tree.insert("", "end", values=row)

def run():
    win = tk.Toplevel()
    win.title("گزارش‌گیری")
    win.geometry("700x450")

    frame = ttk.Frame(win, padding=10)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="جستجو بر اساس نام مشتری:").grid(row=0, column=0, sticky="w")
    name_entry = ttk.Entry(frame, width=30)
    name_entry.grid(row=0, column=1, padx=5)

    columns = ("نام مشتری", "شرح", "قیمت", "تاریخ")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.grid(row=2, column=0, columnspan=2, pady=10)

    search_btn = ttk.Button(frame, text="جستجو", command=lambda: search_by_name(name_entry.get(), tree))
    search_btn.grid(row=1, column=0, columnspan=2, pady=5)

    win.mainloop()