from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def compress_image(uploaded_image):
    try:
        img = Image.open(uploaded_image)
        img = img.convert("RGB")  # Just in case PNG or alpha exists

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=80)  # 80% compression

        return ContentFile(buffer.getvalue(), name=uploaded_image.name)
    except Exception:
        return uploaded_image
