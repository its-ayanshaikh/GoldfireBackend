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
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="purchases")

    bill_no = models.CharField(max_length=50, null=True, blank=True)
    purchase_date = models.DateField()

    total = models.DecimalField(max_digits=12, decimal_places=2)

    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-purchase_date"]

    def __str__(self):
        return f"Purchase #{self.id} - {self.vendor.name}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey('product.Product', on_delete=models.PROTECT)
    variant = models.ForeignKey('product.ProductVariant', on_delete=models.PROTECT, null=True, blank=True)

    qty = models.PositiveIntegerField()

    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    barcode = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.qty}"


class StockIn(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, related_name='stock_ins'
    )

    purchase_item = models.ForeignKey(
        PurchaseItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, related_name='stock_ins'
    )

    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    variant = models.ForeignKey('product.ProductVariant', null=True, blank=True, on_delete=models.CASCADE)
    branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE)

    qty = models.IntegerField()  # +ve = purchase, -ve = sale/transfer

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"StockIn #{self.id} - {self.product.name} - {self.qty}"
    

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

    def purchase_receipt_upload_path(instance, filename):
        return f"purchases/{instance.purchase.id}/{filename}"


class VendorReturnMonthly(models.Model):
    variant = models.ForeignKey('product.ProductVariant', on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE)

    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    total_qty = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            'variant',
            'vendor',
            'branch',
            'year',
            'month'
        )

    def __str__(self):
        return f"{self.variant} - {self.month}/{self.year}"
