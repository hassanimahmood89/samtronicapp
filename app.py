import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# مسیر فونت سفارشی (اگر استفاده می‌کنی)
FONT_PATH = os.path.join(os.path.dirname(sys.argv[0]), "fonts", "IRANSans.ttf")


# تابع‌هایی برای هر بخش
def open_customers():
    try:
        import customers

        customers.run()
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در اجرای بخش مشتریان:\n{e}")


def open_repairs():
    try:
        import repairs

        repairs.run()
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در اجرای بخش تعمیرات:\n{e}")


def open_invoice():
    try:
        import invoice

        invoice.run()
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در اجرای بخش فاکتور:\n{e}")


def exit_app():
    app.destroy()


# ساخت پنجره اصلی
app = tk.Tk()
app.title("سامترونیک - سیستم مدیریت تعمیرگاه")
app.geometry("600x400")
app.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

# عنوان اصلی
title = ttk.Label(app, text="سامترونیک", font=("Tahoma", 20, "bold"))
title.pack(pady=30)

# دکمه‌ها
button_frame = ttk.Frame(app)
button_frame.pack(pady=20)

ttk.Button(button_frame, text="ثبت مشتری", command=open_customers, width=20).grid(
    row=0, column=0, padx=10, pady=10
)
ttk.Button(button_frame, text="ثبت تعمیر", command=open_repairs, width=20).grid(
    row=0, column=1, padx=10, pady=10
)
ttk.Button(button_frame, text="فاکتور", command=open_invoice, width=20).grid(
    row=1, column=0, padx=10, pady=10
)
ttk.Button(button_frame, text="خروج", command=exit_app, width=20).grid(
    row=1, column=1, padx=10, pady=10
)

# اجرا
app.mainloop()
