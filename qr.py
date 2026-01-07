import qrcode

# -------- USER CONFIG --------
upi_id = "ayanhusainshaikh2110@okaxis"          # <-- yahan apni UPI ID daalo
name = "Shaikh Ayan Husain"              # <-- Business ya apna naam
amount = "250.00"              # <-- Dynamic value (billing ke hisaab se badal sakti)
file_name = "upi_qr.png"       # <-- Output QR file
# ------------------------------

# UPI URL with encoded name (space ko %20 se replace)
upi_link = f"upi://pay?pa={upi_id}&pn={name.replace(' ', '%20')}&am={amount}&cu=INR"

# QR Code Generate
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(upi_link)
qr.make(fit=True)

# Save QR Image
img = qr.make_image(fill_color="black", back_color="white")
img.save(file_name)



