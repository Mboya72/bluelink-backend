from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.base import ContentFile

def generate_order_receipt(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Bluelink Receipt - Order #{order.id}")
    
    # Body
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, 750, f"Buyer: {order.buyer.email}")
    p.drawString(100, 730, f"Seller: {order.seller.email}")
    p.line(100, 720, 500, 720)
    
    p.drawString(100, 700, f"Total Amount Paid: KES {order.total_amount}")
    p.drawString(100, 680, f"Status: {order.get_status_display()}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer.getvalue()