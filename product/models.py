from django.db import models
from vendor.models import Vendor
from company.models import Branch
from PIL import Image
import io
from django.core.files.base import ContentFile
from rembg import remove  # pip install rembg pillow

class Commission(models.Model):
    COMMISSION_TYPES = [
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage'),
    ]

    name = models.CharField(max_length=100)
    commission_type = models.CharField(max_length=20, choices=COMMISSION_TYPES)
    commission_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.commission_value}{'%' if self.commission_type=='percentage' else ''}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    commission = models.ForeignKey(
        Commission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="categories"
    )

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brandsCategory', null=True, blank=True)
    image = models.ImageField(upload_to='brands/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Agar image hai to process karo
        if self.image:
            # Step 1: Image open karo
            img = Image.open(self.image)

            # Step 2: Background remove
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
            output = remove(img_bytes)

            # Step 3: Compress image
            img_no_bg = Image.open(io.BytesIO(output)).convert('RGBA')
            buffer = io.BytesIO()
            img_no_bg.save(buffer, format='WEBP', optimize=True, quality=80)  # compression
            buffer.seek(0)

            # Step 4: Save compressed + bg-removed image
            file_name = f"{self.name}_compressed.webp"
            self.image.save(file_name, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)


class SubBrand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subbrandsCategory', null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subbrandsSubCategory', null=True, blank=True)
    image = models.ImageField(upload_to='subbrands/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
            output = remove(img_bytes)

            img_no_bg = Image.open(io.BytesIO(output)).convert('RGBA')
            buffer = io.BytesIO()
            img_no_bg.save(buffer, format='WEBP', optimize=True, quality=80)
            buffer.seek(0)

            file_name = f"{self.name}_compressed.webp"
            self.image.save(file_name, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)


class Model(models.Model):
    name = models.CharField(max_length=100)
    subbrand = models.ForeignKey(SubBrand, on_delete=models.CASCADE, related_name='models', null=True, blank=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    """
    This model stores product types (like Glass Type, Belt Type, etc.)
    linked directly to Category.
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='types')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class HSN(models.Model):
    code = models.CharField(max_length=20)
    cgst = models.DecimalField(max_digits=5, decimal_places=2)
    sgst = models.DecimalField(max_digits=5, decimal_places=2)
    igst = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='hsn_codes')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code


class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    subbrand = models.ForeignKey(SubBrand, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    hsn = models.ForeignKey(HSN, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    commission_type = models.CharField(max_length=20, choices=[('fixed', 'Fixed'), ('percentage', 'Percentage')], null=True, blank=True)
    commission_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_qty_alert = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)

    is_warranty_item = models.BooleanField(default=False)
    WARRANTY_CHOICES = [
        ('3', '3 Months'),
        ('6', '6 Months'),
        ('9', '9 Months'),
        ('12', '12 Months'),
    ]
    warranty_period = models.CharField(max_length=5, choices=WARRANTY_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class SerialNumber(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='serial_numbers')
    serial_number = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)  # false when sold
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.serial_number}"


class Rack(models.Model):
    name = models.CharField(max_length=50)  # Rack code or name
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='racks')

    def __str__(self):
        return f"{self.name} ({self.branch.name})"

    class Meta:
        unique_together = ('name', 'branch')  # Ek branch me same name duplicate na ho


class Quantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='quantities')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    barcode = models.TextField(null=True, blank=True)
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True, blank=True, related_name='rack_quantities')
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.product.name} - {self.branch.name}"
