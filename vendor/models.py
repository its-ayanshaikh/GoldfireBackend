from django.db import models
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

class Vendor(models.Model):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    gst = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

def purchase_receipt_upload_path(instance, filename):
    return f"purchases/receipts/{instance.purchase.vendor.name}/{filename}"


class Purchase(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name="purchases")
    total = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-purchase_date"]

    def __str__(self):
        return f"Purchase #{self.id} - {self.vendor.name}"


class PurchaseReceipt(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="receipts")
    file = models.FileField(upload_to=purchase_receipt_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Compress image if it's an image file (lossless).
        """
        try:
            if self.file and self.file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                img = Image.open(self.file)

                # Convert to RGB (avoid issues with PNG or transparency)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                img_io = BytesIO()
                img.save(img_io, format="JPEG", optimize=True, quality=85)  # lossless compression
                new_name = os.path.splitext(self.file.name)[0] + ".jpg"
                self.file = ContentFile(img_io.getvalue(), name=new_name)
        except Exception as e:
            print(f"Image compression failed: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt for Purchase #{self.purchase.id}"


class VendorReturnMonthly(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    vendor = models.ForeignKey('vendor.Vendor', on_delete=models.CASCADE)
    branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE)

    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    total_qty = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            'product',
            'vendor',
            'branch',
            'year',
            'month'
        )

    def __str__(self):
        return f"{self.product.name} - {self.month}/{self.year}"


