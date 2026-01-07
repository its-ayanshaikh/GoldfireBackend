from django import template
from decimal import Decimal
from collections import defaultdict

register = template.Library()

@register.simple_tag
def items_by_igst_slab(items):
    """Group bill items by GST slab percentage for display"""
    # Separate GST and non-GST items
    gst_items = defaultdict(list)
    non_gst_items = []
    
    for item in items:
        # Check if item has GST (CGST + SGST or IGST)
        if (item.cgst_amount and item.cgst_amount > 0) or (item.sgst_amount and item.sgst_amount > 0) or (item.igst_amount and item.igst_amount > 0):
            # Group by total GST rate (CGST + SGST + IGST)
            total_gst_rate = (item.cgst_percent or 0) + (item.sgst_percent or 0) + (item.igst_percent or 0)
            key = f"{total_gst_rate:.0f}"
            gst_items[key].append(item)
        else:
            non_gst_items.append(item)
    
    # Create result with slab headers and items
    result = []
    slab_letters = ['A', 'B', 'C', 'D', 'E']
    
    # Add GST slabs
    for i, (rate, items_list) in enumerate(sorted(gst_items.items(), key=lambda x: float(x[0]))):
        slab_letter = slab_letters[i] if i < len(slab_letters) else chr(65 + i)
        
        # Get GST rates from first item (assuming all items in slab have same rates)
        first_item = items_list[0]
        cgst_rate = first_item.cgst_percent or 0
        sgst_rate = first_item.sgst_percent or 0
        
        # Generate header based on GST type
        if cgst_rate > 0 and sgst_rate > 0:
            header = f"{slab_letter}) CGST@{cgst_rate}% SGST@{sgst_rate}%"
        elif first_item.igst_percent > 0:
            header = f"{slab_letter}) IGST@{first_item.igst_percent}%"
        else:
            header = f"{slab_letter}) GST@{rate}%"
        
        # Calculate totals for this slab
        total_taxable = sum(item.taxable_value or 0 for item in items_list)
        total_cgst = sum(item.cgst_amount or 0 for item in items_list)
        total_sgst = sum(item.sgst_amount or 0 for item in items_list)
        total_igst = sum(item.igst_amount or 0 for item in items_list)
        total_amount = sum(item.total or 0 for item in items_list)
        
        result.append({
            'slab_letter': f"{slab_letter})",
            'slab_header': f"{slab_letter}) GST ITEMS",
            'slab_header_formatted': header,
            'items': items_list,
            'total_taxable': total_taxable,
            'total_cgst': total_cgst,
            'total_sgst': total_sgst,
            'total_igst': total_igst,
            'total_amount': total_amount,
            'cgst_rate': cgst_rate,
            'sgst_rate': sgst_rate,
            'igst_rate': first_item.igst_percent or 0
        })
    
    # Add non-GST items if any
    if non_gst_items:
        next_letter = slab_letters[len(result)] if len(result) < len(slab_letters) else chr(65 + len(result))
        result.append({
            'slab_letter': f"{next_letter})",
            'slab_header': f"{next_letter}) NON-GST ITEMS", 
            'slab_header_formatted': f"{next_letter}) NON-GST ITEMS",
            'items': non_gst_items,
            'total_taxable': sum(item.total or 0 for item in non_gst_items),
            'total_cgst': Decimal('0'),
            'total_sgst': Decimal('0'),
            'total_igst': Decimal('0'),
            'total_amount': sum(item.total or 0 for item in non_gst_items),
            'cgst_rate': 0,
            'sgst_rate': 0,
            'igst_rate': 0
        })
    
    return result

@register.simple_tag  
def total_quantity(items):
    """Calculate total quantity from bill items"""
    total_qty = sum(item.qty for item in items)
    return f"{total_qty}.00"

@register.simple_tag
def get_serial_number(bill_item):
    """Get serial number for warranty items"""
    # Return the stored serial number directly
    return bill_item.serial_number if hasattr(bill_item, 'serial_number') else None

@register.simple_tag
def calculate_discount(item):
    """Calculate discount amount: price - final_amount"""
    try:
        discount = item.price - item.final_amount
        return discount
    except:
        return Decimal('0')

@register.simple_tag  
def calculate_net_amount(item):
    """Calculate net amount: final_amount * qty"""
    try:
        net_amount = item.final_amount * item.qty
        return net_amount
    except:
        return Decimal('0')

@register.filter
def round_amount(value):
    """Round amount: <50 paise = down, >=50 paise = up"""
    try:
        value = float(value)
        # Get decimal part
        decimal_part = value - int(value)
        
        if decimal_part < 0.5:
            # Round down
            return int(value)
        else:
            # Round up  
            return int(value) + 1
    except:
        return 0

@register.filter
def round_off_difference(value):
    """Calculate round off difference"""
    try:
        original = float(value)
        rounded = round_amount(original)
        difference = rounded - original
        return f"{difference:.2f}"
    except:
        return "0.00"

@register.simple_tag
def calculate_slab_total(taxable, cgst, sgst):
    """Calculate slab total: taxable + cgst + sgst with proper decimal handling"""
    try:
        from decimal import Decimal
        taxable_val = Decimal(str(taxable)) if taxable else Decimal('0')
        cgst_val = Decimal(str(cgst)) if cgst else Decimal('0')
        sgst_val = Decimal(str(sgst)) if sgst else Decimal('0')
        
        total = taxable_val + cgst_val + sgst_val
        total_float = float(total)
        
        # Round off logic: if decimal part >= 0.90, round up
        decimal_part = total_float - int(total_float)
        if decimal_part >= 0.90:
            return int(total_float) + 1
        else:
            return total_float
    except:
        return 0.0