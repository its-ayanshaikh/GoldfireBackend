import requests

# ✅ WhatsApp API Configuration
PHONE_NUMBER_ID = "847415435125406"
WHATSAPP_TOKEN = "EAAJZCq8QYRIoBP0LX5911g0mIzAZAN4uktsRQwUkF2KdGd3nqzBdElDFV17t6zMzDzkVBZASZBtLvzHUD0IO5Wu3UYZCM2Hsa4s3ZACbATZAcq1WcUneMMflMu5jZAp8oz0ZCVbd9Hc2lE4NWOF1juUhymk2qOPjqQOgihrhetBaUREXMS6ePe5UhSymvsXOhKZC4BRDeOt9pHzI1NZBK8jwBW9aHkwISohziNasJ2vZB2a7rSYCUMYafjuBDA5nExdwC5VdGgC59yaTki11r1qzl8bjAKT6"

WHATSAPP_API_URL = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
# ✅ Customer Details (Static for test)
CUSTOMER_NAME = "Musab Shaikh"
CUSTOMER_PHONE = "919825093413"  # include country code
BILL_NUMBER = "G-003-20251104-0001"
BILL_ID = 123  # static for now

# ✅ Template Payload
payload = {
    "messaging_product": "whatsapp",
    "to": CUSTOMER_PHONE,
    "type": "template",
    "template": {
        "name": "goldfire_invoice",
        "language": {"code": "en_US"},
        "components": [
            {
                "type": "header",
                "parameters": [
                    {"type": "document", "document": {"id": "795208900016309", "filename": "GoldfireInvoice.pdf"}}
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": CUSTOMER_NAME},
                    {"type": "text", "text": BILL_NUMBER}
                ]
            }
        ]
    }
}

# ✅ Headers
headers = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}



try:
    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers, timeout=30)



    if response.status_code == 200:

    else:


except requests.exceptions.RequestException as e:


# upload_url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/media"

# file_path = r"A:\STARTUP\GOLDFIRE\bill.pdf"

# files = {
#     "file": ("bill.pdf", open(file_path, "rb"), "application/pdf")
# }

# print(files)

# data = {"messaging_product": "whatsapp"}

# headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

# resp = requests.post(upload_url, headers=headers, files=files, data=data)
# print(resp.json())
