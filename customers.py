import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "samtronic.db")

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_customer(first_name, last_name, phone, tree):
    if not first_name or not last_name or not phone:
        messagebox.showwarning("خطا", "لطفاً تمام فیلدها را وارد کنید.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO customers (first_name, last_name, phone) VALUES (?, ?, ?)",
              (first_name, last_name, phone))
    conn.commit()
    conn.close()

    messagebox.showinfo("ثبت شد", "مشتری با موفقیت ثبت شد.")
    show_customers(tree)

def show_customers(tree):
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=row)

def run():
    create_table()

    win = tk.Toplevel()
    win.title("ثبت مشتری")
    win.geometry("550x400")

    frame = ttk.Frame(win, padding=10)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="نام:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    first_name_entry = ttk.Entry(frame)
    first_name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="نام خانوادگی:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    last_name_entry = ttk.Entry