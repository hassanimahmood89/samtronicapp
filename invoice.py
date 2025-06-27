from fpdf import FPDF
import sqlite3
import os
import webbrowser


class InvoiceGenerator:
    def __init__(self, repair_id):
        self.repair_id = repair_id
        self.conn = sqlite3.connect("samtronic.db")
        self.cursor = self.conn.cursor()
        self.generate_invoice()

    def generate_invoice(self):
        self.cursor.execute(
            """
            SELECT r.id, c.name, c.phone, r.device, r.problem, r.status, r.cost, r.note, r.warranty
            FROM repairs r
            JOIN customers c ON r.customer_id = c.id
            WHERE r.id = ?
        """,
            (self.repair_id,),
        )
        r = self.cursor.fetchone()
        if not r:
            return

        self.cursor.execute(
            """
            SELECT i.name, rp.quantity_used, i.sell_price
            FROM repair_parts rp
            JOIN inventory i ON rp.part_id = i.id
            WHERE rp.repair_id = ?
        """,
            (self.repair_id,),
        )
        parts = self.cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("IRANSans", "", "fonts/IRANSans.ttf", uni=True)
        pdf.set_font("IRANSans", size=14)

        if os.path.exists("static/samtronic_logo.png"):
            pdf.image("static/samtronic_logo.png", x=10, y=8, w=30)

        pdf.cell(200, 10, txt="فاکتور رسمی تعمیرات", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("IRANSans", size=12)

        labels = [
            f"شماره فاکتور: {r[0]}",
            f"مشتری: {r[1]} - {r[2]}",
            f"دستگاه: {r[3]}",
            f"مشکل گزارش‌شده: {r[4]}",
            f"وضعیت تعمیر: {r[5]}",
            f"هزینه کل: {r[6]} تومان",
            f"توضیحات فنی: {r[7]}",
            f"گارانتی: {r[8]}",
        ]
        for line in labels:
            pdf.cell(0, 10, txt=line, ln=True, align="R")

        pdf.ln(5)
        pdf.cell(0, 10, txt="🔩 قطعات مصرفی:", ln=True, align="R")
        total_parts = 0
        for name, qty, price in parts:
            subtotal = int(price or 0) * qty
            total_parts += subtotal
            pdf.cell(
                0, 10, txt=f"{name} × {qty} = {subtotal} تومان", ln=True, align="R"
            )

        pdf.ln(5)
        pdf.cell(0, 10, txt=f"جمع کل قطعات: {total_parts} تومان", ln=True, align="R")

        filename = f"invoice_{r[0]}.pdf"
        pdf.output(filename)

        try:
            webbrowser.open_new(filename)
        except:
            pass
