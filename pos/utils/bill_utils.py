# # utils/bill_utils.py
# import io
# import os
# from datetime import datetime
# from decimal import Decimal

# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import mm
# from reportlab.lib import utils as rl_utils
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import getSampleStyleSheet
# from PIL import Image

# import barcode
# from barcode.writer import ImageWriter

# def _draw_image(c, img_path, x, y, max_width, max_height):
#     """Helper to draw and scale an image on reportlab canvas."""
#     if not img_path or not os.path.exists(img_path):
#         return
#     im = rl_utils.ImageReader(img_path)
#     iw, ih = im.getSize()
#     scale = min(max_width / iw, max_height / ih)
#     w, h = iw * scale, ih * scale
#     c.drawImage(img_path, x, y - h, width=w, height=h, preserveAspectRatio=True, mask='auto')

# def _generate_barcode_image(bill_number, out_dir="/tmp"):
#     """Generate Code128 barcode PNG and return filepath."""
#     code_class = barcode.get_barcode_class('code128')
#     barcode_obj = code_class(bill_number, writer=ImageWriter())
#     filename = os.path.join(out_dir, f"barcode_{bill_number}.png")
#     # write with some options
#     barcode_obj.save(filename, options={"module_height": 10.0, "module_width": 0.4, "font_size": 10})
#     return filename

# def generate_bill_pdf(bill_obj, items_queryset_or_list, branch_obj, logo_path=None, output_dir="/tmp"):
#     """
#     Generate bill PDF file for given bill and return path to PDF.
#     Supports both queryset of BillItem objects and list of dicts.
#     """
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir, exist_ok=True)

#     filename = os.path.join(output_dir, f"bill_{bill_obj.bill_number}.pdf")
#     c = canvas.Canvas(filename, pagesize=A4)
#     width, height = A4

#     margin = 18 * mm
#     x = margin
#     y = height - margin

#     # Draw logo left side
#     if logo_path:
#         _draw_image(c, logo_path, x, y, max_width=60*mm, max_height=20*mm)

#     # Header text (company name)
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(x + 70*mm, y - 8, "GOLDFIRE")

#     # Bill meta
#     c.setFont("Helvetica", 9)
#     y -= 30
#     c.drawString(x, y, f"Bill No: {bill_obj.bill_number}")
#     c.drawRightString(
#         width - margin,
#         y,
#         f"Date: {bill_obj.date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(bill_obj, 'date') else datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
#     )

#     y -= 14
#     c.drawString(x, y, f"Customer: {bill_obj.customer.name if bill_obj.customer else ''}")
#     c.drawRightString(width - margin, y, f"Phone: {bill_obj.customer.phone if getattr(bill_obj.customer, 'phone', None) else ''}")

#     # Branch address
#     y -= 14
#     branch_lines = (branch_obj.address or "").splitlines()
#     c.setFont("Helvetica", 8)
#     c.drawString(x, y, "Store Address:")
#     for line in branch_lines:
#         c.drawString(x + 60, y, line)
#         y -= 10

#     # Table headers
#     y -= 8
#     c.setFont("Helvetica-Bold", 9)
#     c.drawString(x, y, "S.No")
#     c.drawString(x + 30*mm, y, "Description")
#     c.drawString(x + 110*mm, y, "Price")
#     c.drawString(x + 135*mm, y, "Qty")
#     c.drawString(x + 155*mm, y, "Disc")
#     c.drawString(x + 180*mm, y, "Total")

#     c.setFont("Helvetica", 9)
#     y -= 12
#     sno = 1
#     total_qty = Decimal(0)

#     for it in items_queryset_or_list:
#         # Safe getter to handle model instance or dict
#         def safe(obj, key, default=None):
#             if hasattr(obj, key):
#                 return getattr(obj, key)
#             if isinstance(obj, dict):
#                 return obj.get(key, default)
#             return default

#         product = safe(it, "product", None)
#         desc = ""
#         if product and hasattr(product, "name"):
#             desc = product.name
#         else:
#             desc = safe(it, "description", "")

#         price = Decimal(safe(it, "price", 0) or 0)
#         qty = Decimal(safe(it, "qty", 0) or 0)
#         disc_val = Decimal(safe(it, "discount_value", 0) or 0)
#         total = safe(it, "total", None)
#         if total is None:
#             total = (price * qty) - disc_val
#         total = Decimal(total)

#         if y < 80 * mm:
#             c.showPage()
#             y = height - margin

#         c.drawString(x, y, str(sno))
#         c.drawString(x + 30 * mm, y, str(desc)[:40])
#         c.drawRightString(x + 135 * mm, y, f"{price:.2f}")
#         c.drawRightString(x + 155 * mm, y, f"{qty}")
#         c.drawRightString(x + 180 * mm, y, f"{disc_val:.2f}")
#         c.drawRightString(width - margin, y, f"{total:.2f}")

#         y -= 12
#         sno += 1
#         total_qty += qty

#     # Totals
#     y -= 10
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(x, y, f"No of Items: {sno - 1}")
#     c.drawRightString(width - margin, y, f"Total Qty: {total_qty}")

#     y -= 14
#     c.drawString(x, y, f"Gross Total: {float(bill_obj.total_amount):.2f}")
#     y -= 12
#     c.drawString(x, y, f"Total Discount: {float(bill_obj.total_discount):.2f}")
#     y -= 12
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(x, y, f"Final Amount: {float(bill_obj.final_amount):.2f}")

#     # Barcode
#     try:
#         barcode_path = _generate_barcode_image(bill_obj.bill_number, out_dir=output_dir)
#         _draw_image(c, barcode_path, x, y - 50, max_width=60 * mm, max_height=20 * mm)
#     except Exception as e:
#         print("Barcode gen error:", e)

#     # Footer
#     y_footer = 30 * mm
#     c.setFont("Helvetica", 8)
#     c.drawString(x, y_footer, "Thank you for shopping with GOLDFIRE.")
#     c.save()

#     try:
#         if "barcode_path" in locals() and os.path.exists(barcode_path):
#             os.remove(barcode_path)
#     except Exception:
#         pass

#     return filename

import os
import base64
import io
from django.template.loader import render_to_string
from weasyprint import HTML
import barcode
from barcode.writer import ImageWriter
from PIL import Image

def generate_barcode_base64(text):
    """Generate barcode as base64 string for embedding in HTML"""
    try:
        # Create Code128 barcode
        code128 = barcode.get_barcode_class('code128')
        barcode_instance = code128(str(text), writer=ImageWriter())
        
        # Save to memory buffer
        buffer = io.BytesIO()
        barcode_instance.write(buffer, options={
            'module_height': 5.0,
            'module_width': 0.25,
            'write_text': False,
            'text_distance': 0,
            'quiet_zone': 1.0
        })
        
        # Convert to base64
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:

        return None

def generate_bill_pdf_html(bill, items, branch, logo_path=None, output_dir="tmp"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Generate barcode as base64 image
    barcode_base64 = generate_barcode_base64(bill.bill_number)

    # Calculate if there are any GST items
    has_gst_items = any(item.cgst_amount or item.sgst_amount or item.igst_amount for item in items)
    
    context = {
        "bill": bill,
        "items": items,
        "branch": branch,
        "logo_url": logo_path or "",
        "barcode_image": barcode_base64,
        "has_gst_items": has_gst_items,
        "is_gst": bill.is_gst,
    }

    html_content = render_to_string("bills/invoice.html", context)
    pdf_file = os.path.join(output_dir, f"bill_{bill.bill_number}.pdf")

    HTML(string=html_content).write_pdf(pdf_file)
    return pdf_file
