from fpdf import FPDF
import sqlite3
import os
import datetime

class ReportGenerator:
    def __init__(self):
        self.conn = sqlite3.connect("samtronic.db")
        self.cursor = self.conn.cursor()

    def generate(self):
        self.generate_repairs_report()
        self.generate_inventory_report()

    def generate_repairs_report(self):
        self.cursor.execute("""
            SELECT r.id, c.name, r.device, r.problem, r.status, r.cost
            FROM repairs r
            JOIN customers c ON r.customer_id = c.id
        """)
        repairs = self.cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("IRANSans", "", "fonts/IRANSans.ttf", uni=True)
        pdf.set_font("IRANSans", size=12)

        if os.path.exists("static/samtronic_logo.png"):
            pdf.image("static/samtronic_logo.png", x=10, y=8, w=30)

        pdf.cell(200, 10, txt="📋 گزارش تعمیرات", ln=True, align="C")
        pdf.ln(10)

        for r in repairs:
            pdf.cell(0, 10, txt=f"#{r[0]} | مشتری: {r[1]} | دستگاه: {r[2]} | مشکل: {r[3]} | وضعیت: {r[4]} | هزینه: {r[5]} تومان", ln=True, align="R")

        filename = f"report_repairs_{datetime.date.today()}.pdf"
        pdf.output(filename)

    def generate_inventory_report(self):
        self.cursor.execute("SELECT name, quantity, buy_price, sell_price FROM inventory")
        parts = self.cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("IRANSans", "", "fonts/IRANSans.ttf", uni=True)
        pdf.set_font("IRANSans", size=12)

        if os.path.exists("static/samtronic_logo.png"):
            pdf.image("static/samtronic_logo.png", x=10, y=8, w=30)

        pdf.cell(200, 10, txt="📦 گزارش موجودی انبار", ln=True, align="C")
        pdf.ln(10)

        for p in parts:
            pdf.cell(0, 10, txt=f"{p[0]} | موجودی: {p[1]} | خرید: {p[2]} | فروش: {p[3]}", ln=True, align="R")

        filename = f"report_inventory_{datetime.date.today()}.pdf"
        pdf.output(filename)