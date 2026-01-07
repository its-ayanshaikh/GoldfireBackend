from django.db import models
from employee.models import Employee

DISCOUNT_CHOICES = [
    ('percentage', 'Percentage'),
    ('fixed', 'Fixed'),
]

PAYMENT_METHOD_CHOICES = [
    ('cash', 'Cash'),
    ('upi', 'UPI'),
    ('split', 'Split'),
    ('pay_later', 'Pay Later'),
]


class ProductTransfer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='transfers')
    from_branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE, related_name='outgoing_transfers')
    to_branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE, related_name='incoming_transfers')
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.from_branch.name} ➝ {self.to_branch.name}) - {self.status}"
    

# -------------------------------
# CUSTOMER MODEL
# -------------------------------
class Customer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone or 'No phone'})"
    

# -------------------------------
# BILL MODEL
# -------------------------------
class Bill(models.Model):
    bill_number = models.CharField(max_length=50, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='bills')
    bill_name = models.CharField(max_length=150, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_taxable_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_gst = models.BooleanField(default=False, help_text="Indicates if the bill is a GST bill") 
    total_cgst = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    total_sgst = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    total_igst = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.customer.name if self.customer else 'Unknown'} - {self.date.strftime('%Y-%m-%d')}"


# -------------------------------
# BILL ITEM MODEL
# -------------------------------
class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    salesperson = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_CHOICES, blank=True, null=True)
    discount_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cgst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sgst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    igst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    taxable_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    serial_number = models.CharField(max_length=100, null=True, blank=True)  # For warranty items
    is_returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product.name} ({self.qty})"


# -------------------------------
# PAYMENT MODEL
# -------------------------------
class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES)
    cash_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    upi_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} - {self.total_amount}"


# -------------------------------
# RETURN BILL MODEL
# -------------------------------
class ReturnBill(models.Model):
    REFUND_TYPE_CHOICES = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('split', 'Split'),
    )
    
    RETURN_DESTINATION_CHOICES = (
        ('stock', 'Return To Stock'),
        ('vendor', 'Return To Vendor'),
    )

    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='returns',
        help_text="Original bill reference"
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE)

    total_refund = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # 🔽 Refund Payment Info
    refund_type = models.CharField(
        max_length=10,
        choices=REFUND_TYPE_CHOICES,
        null=True,
        blank=True
    )
    cash_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=0
    )
    upi_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=0
    )
    
    return_destination = models.CharField(
        max_length=10,
        choices=RETURN_DESTINATION_CHOICES,
        default='stock'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return #{self.id} - {self.bill.bill_number}"

    @property
    def return_items_count(self):
        return self.items.count()

    

# -------------------------------
# RETURN BILL MODEL
# -------------------------------
class ReturnItem(models.Model):
    return_bill = models.ForeignKey(ReturnBill, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    original_bill_item = models.ForeignKey(BillItem, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    total_refund = models.DecimalField(max_digits=12, decimal_places=2)
    salesperson = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} (x{self.qty})"



# -------------------------------
# REPLACE MODEL
# -------------------------------
class ReplacementBill(models.Model):

    REPLACEMENT_TYPE_CHOICES = (
        ('warranty', 'Warranty Replacement'),
        ('dissatisfaction', 'Customer Dissatisfaction'),
    )

    RETURN_DESTINATION_CHOICES = (
        ('stock', 'Return To Stock'),
        ('vendor', 'Return To Vendor'),
    )

    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='replacements'
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey('company.Branch', on_delete=models.CASCADE)

    replacement_type = models.CharField(
        max_length=20,
        choices=REPLACEMENT_TYPE_CHOICES
    )

    return_destination = models.CharField(
        max_length=10,
        choices=RETURN_DESTINATION_CHOICES
    )

    # 💰 Amount summary
    old_total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    new_total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # +ve => customer pays | -ve => refund
    difference_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


# -------------------------------
# REPLACEMENT ITEM MODEL
# -------------------------------
class ReplacementItem(models.Model):
    replacement_bill = models.ForeignKey(
        ReplacementBill,
        on_delete=models.CASCADE,
        related_name='items'
    )

    old_bill_item = models.ForeignKey(
        BillItem,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    old_product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name='replacement_old_products'
    )
    new_product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name='replacement_new_products'
    )

    qty = models.PositiveIntegerField()

    old_price = models.DecimalField(max_digits=12, decimal_places=2)
    new_price = models.DecimalField(max_digits=12, decimal_places=2)

    # 🔢 serial handling (warranty)
    old_serial_number = models.CharField(max_length=100, null=True, blank=True)
    new_serial_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.old_product.name} ➝ {self.new_product.name}"


# -------------------------------
# REPLACEMENT PAYMENT MODEL
# -------------------------------
class ReplacementPayment(models.Model):

    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('split', 'Split'),
    )

    replacement_bill = models.ForeignKey(
        ReplacementBill,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES
    )

    cash_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    upi_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Replacement Payment {self.total_amount}"


# -------------------------------
# REPLACEMENT REFUND MODEL
# -------------------------------
class ReplacementRefund(models.Model):

    REFUND_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('split', 'Split'),
    )

    replacement_bill = models.ForeignKey(
        ReplacementBill,
        on_delete=models.CASCADE,
        related_name='refunds'
    )

    refund_method = models.CharField(
        max_length=10,
        choices=REFUND_METHOD_CHOICES
    )

    cash_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    upi_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_refund = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Replacement Refund {self.total_refund}"
