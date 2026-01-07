import os
import requests
from typing import Optional
import dotenv

dotenv.load_dotenv()   # loads .env from CWD or project root
# read from env (recommended to set in .env or your process manager)
PHONE_NUMBER_ID = os.getenv("WH_PHONE_NUMBER_ID")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")

if not PHONE_NUMBER_ID or not WHATSAPP_TOKEN:
    # We don't crash at import time in prod; just warn (optional)

    pass

BASE_MESSAGES_URL = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
BASE_MEDIA_URL = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/media"

HEADERS_JSON = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}

def _format_mobile(phone_raw: Optional[str]) -> Optional[str]:
    if not phone_raw:
        return None
    s = str(phone_raw).strip().replace("+", "").replace(" ", "").replace("-", "")
    if s.startswith("0") and len(s) > 10:
        s = s.lstrip("0")
    if len(s) == 10:
        s = "91" + s
    return s

def upload_media(file_path: str, mime_type: str = "application/pdf") -> str:
    """
    Upload a file to WhatsApp Cloud API media endpoint.
    Returns media_id on success, raises requests.exceptions.HTTPError on failure.
    """
    if not PHONE_NUMBER_ID or not WHATSAPP_TOKEN:
        raise RuntimeError("WH_PHONE_NUMBER_ID and WHATSAPP_TOKEN must be set in environment")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Media file not found: {file_path}")

    files = {
        "file": (os.path.basename(file_path), open(file_path, "rb"), mime_type)
    }
    data = {"messaging_product": "whatsapp"}
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

    resp = requests.post(BASE_MEDIA_URL, headers=headers, files=files, data=data, timeout=60)
    resp.raise_for_status()
    res_json = resp.json()
    media_id = res_json.get("id")
    if not media_id:
        raise RuntimeError(f"Unexpected response from media upload: {res_json}")
    return media_id

def send_invoice_template(bill, media_id: Optional[str] = None, template_name: str = "goldfire_invoice"):
    """
    Send a template message for invoice.
    - bill: Bill instance (must have customer with name & phone, bill_number, id)
    - media_id: optional uploaded media id (for document header)
    - template_name: the approved template name in WhatsApp Manager
    Returns response JSON from WhatsApp API.
    Raises requests.exceptions.HTTPError on non-2xx responses.
    """
    if not PHONE_NUMBER_ID or not WHATSAPP_TOKEN:
        raise RuntimeError("WH_PHONE_NUMBER_ID and WHATSAPP_TOKEN must be set in environment")

    to_mobile = _format_mobile(getattr(bill.customer, "phone", None))
    if not to_mobile:
        raise ValueError("Customer phone not available or invalid")

    components = []

    # header (document) if provided
    if media_id:
        components.append({
            "type": "header",
            "parameters": [
                {"type": "document", "document": {"id": str(media_id), "filename": f"{bill.bill_number}.pdf"}}
            ]
        })

    # body parameters (customer name, bill number)
    components.append({
        "type": "body",
        "parameters": [
            {"type": "text", "text": str(getattr(bill.customer, 'name', '') or '')},
            {"type": "text", "text": str(getattr(bill, 'bill_number', '') or '')}
        ]
    })

    payload = {
        "messaging_product": "whatsapp",
        "to": to_mobile,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en_US"},
            "components": components
        }
    }

    resp = requests.post(BASE_MESSAGES_URL, json=payload, headers=HEADERS_JSON, timeout=30)
    # Helpful: if you want to inspect non-2xx, don't raise here; raise for now so caller can catch
    resp.raise_for_status()
    return resp.json()
