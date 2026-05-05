from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError
import employee
from employee.models import *
from company.models import *
from pos.utils.bill_utils import *
from pos.utils.whatsapp import *
from product.models import *
from django.db.models import Q, Exists, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from .serializers import *
from .models import *
from datetime import date, datetime
from .pagination import *
from django.db.models import Count, Sum, F
from django.db import transaction
from decimal import Decimal
from django.db.models import Sum
from django.utils.timezone import now
from vendor.models import VendorReturnMonthly, PurchaseItem, StockIn

# ---------------------
# CREATE RACK
# ---------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_rack(request):
    user = request.user

    # ---------- Verify branch ----------
    if not hasattr(user, 'branch') or not user.branch:
        return Response(
            {"success": False, "message": "User is not assigned to any branch."},
            status=status.HTTP_400_BAD_REQUEST
        )

    branch = user.branch
    serializer = RackSerializer(data=request.data)
    if serializer.is_valid():
        rack = serializer.save(branch=branch)
        return Response(RackSerializer(rack).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------
# LIST RACKS
# ---------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_racks(request):
    user = request.user
    if not user.branch:
        return Response({'error': 'Branch not found for user'}, status=status.HTTP_400_BAD_REQUEST)

    racks = Rack.objects.filter(branch=user.branch)
    serializer = RackSerializer(racks, many=True)
    return Response(serializer.data)


# ---------------------
# UPDATE RACK
# ---------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_rack(request, rack_id):
    employee = request.user
    if not employee or not employee.branch:
        return Response({'error': 'Branch not found for user'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        rack = Rack.objects.get(id=rack_id, branch=employee.branch)
    except Rack.DoesNotExist:
        return Response({'error': 'Rack not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RackSerializer(rack, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()  # branch same rahegi
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------
# DELETE RACK
# ---------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_rack(request, rack_id):
    employee = request.user
    if not employee or not employee.branch:
        return Response({'error': 'Branch not found for user'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        rack = Rack.objects.get(id=rack_id, branch=employee.branch)
    except Rack.DoesNotExist:
        return Response({'error': 'Rack not found'}, status=status.HTTP_404_NOT_FOUND)

    rack.delete()
    return Response({'message': 'Rack deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# ---------------------------
# RACK ALLOCATION API
# ---------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def allocate_rack(request):
    """
    Allocate a product to a specific rack in the current user's branch.
    Required: product_id, rack_id
    """
    employee = request.user
    if not employee or not employee.branch:
        return Response({'error': 'Branch not found for user'}, status=status.HTTP_400_BAD_REQUEST)

    branch = employee.branch
    product_id = request.data.get('product_id')
    rack_id = request.data.get('rack_id')

    # Validate required fields
    if not product_id or not rack_id:
        return Response({'error': 'product_id and rack_id are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate product & rack existence
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        rack = Rack.objects.get(id=rack_id, branch=branch)
    except Rack.DoesNotExist:
        return Response({'error': 'Rack not found in your branch'}, status=status.HTTP_404_NOT_FOUND)

    # Get or create Quantity record
    quantity_obj, created = Quantity.objects.get_or_create(
        product=product,
        branch=branch,
        defaults={'rack': rack}
    )

    # If already exists, update rack
    if not created:
        quantity_obj.rack = rack
        quantity_obj.save()

    return Response({
        'success': True,
        'message': 'Rack allocated successfully',
        'data': {
            'product': product.name,
            'branch': branch.name,
            'rack': rack.name,
            'qty': quantity_obj.qty,
            'created': created
        }
    }, status=status.HTTP_200_OK)


# ------------------------
# PRODUCT LIST WITH RACKS AND QUANTITIES
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    """Return branch-wise product list with racks and quantities"""
    employee = request.user
    if not employee or not employee.branch:
        return Response({'error': 'Branch not found for user'}, status=status.HTTP_400_BAD_REQUEST)

    branch = employee.branch

    products = Product.objects.filter(
        status='active',
        quantities__branch=branch
    ).prefetch_related(
        'quantities__rack', 'brand', 'category'
    ).distinct()

    serializer = ProductBranchSerializer(products, many=True, context={'branch': branch})
    return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------
# CREATE PRODUCT TRANSFER REQUEST
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transfer_request(request):
    product_id = request.data.get('product_id')
    to_branch_id = request.data.get('to_branch')
    qty = int(request.data.get('quantity'))
    notes = request.data.get('notes')

    from_branch = request.user.branch
    product = Product.objects.filter(id=product_id).first()
    to_branch = Branch.objects.filter(id=to_branch_id).first()

    if not product or not to_branch:
        return Response({"error": "Invalid product or branch"}, status=400)

    from_qty = Quantity.objects.filter(product=product, branch=from_branch).first()

    transfer = ProductTransfer.objects.create(
        product=product,
        from_branch=from_branch,
        to_branch=to_branch,
        quantity=qty,
        notes=notes if notes else '',
        status='pending'
    )
    return Response({"message": "Transfer request created", "id": transfer.id})


# ------------------------
# UPDATE TRANSFER STATUS
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_transfer_status(request, transfer_id):
    action = request.data.get('action')  # 'accept' or 'reject'
    user_branch = request.user.branch

    transfer = ProductTransfer.objects.filter(id=transfer_id).first()
    if not transfer:
        return Response({"error": "Transfer not found"}, status=404)

    if transfer.to_branch != user_branch:
        return Response({"error": "Not authorized for this transfer"}, status=403)

    if action == 'reject':
        transfer.status = 'rejected'
        transfer.save()
        return Response({"message": "Transfer rejected"})

    if action == 'accept':
        # Update stock quantities
        from_qty = Quantity.objects.filter(product=transfer.product, branch=transfer.from_branch).first()
        to_qty, _ = Quantity.objects.get_or_create(product=transfer.product, branch=transfer.to_branch)

        if from_qty and from_qty.qty >= transfer.quantity:
            from_qty.qty -= transfer.quantity
            from_qty.save()

            to_qty.qty += transfer.quantity
            to_qty.save()

            transfer.status = 'completed'
            transfer.save()
            return Response({"message": "Transfer completed successfully"})
        else:
            return Response({"error": "Not enough stock in source branch"}, status=400)

    return Response({"error": "Invalid action"}, status=400)


# ------------------------
# SENT TRANSFERS
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sent_transfers(request):
    """
    Get all product transfers sent FROM the logged-in user's branch
    """
    employee = request.user
    if not employee or not employee.branch:
        return Response({"error": "Branch not found for user"}, status=400)

    branch = employee.branch
    transfers = ProductTransfer.objects.filter(from_branch=branch).select_related('product', 'from_branch', 'to_branch')

    data = [
        {
            "id": t.id,
            "product": t.product.name,
            "brand": t.product.brand.name if t.product.brand else None,
            "model": t.product.model.name if t.product.model else None,
            "subbrand": t.product.subbrand.name if t.product.subbrand else None,
            "from": t.from_branch.name,
            "to": t.to_branch.name,
            "quantity": t.quantity,
            "status": t.status,
            "created_at": t.created_at,
        }
        for t in transfers
    ]
    return Response(data)


# ------------------------
# GET BRANCH EMPLOYEES
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def received_transfers(request):
    """
    Get all product transfers received BY the logged-in user's branch
    """
    employee = request.user
    if not employee or not employee.branch:
        return Response({"error": "Branch not found for user"}, status=400)

    branch = employee.branch
    transfers = ProductTransfer.objects.filter(to_branch=branch).select_related('product', 'from_branch', 'to_branch')

    data = [
        {
            "id": t.id,
            "product": t.product.name,
            "brand": t.product.brand.name if t.product.brand else None,
            "model": t.product.model.name if t.product.model else None,
            "subbrand": t.product.subbrand.name if t.product.subbrand else None,
            "from": t.from_branch.name,
            "to": t.to_branch.name,
            "quantity": t.quantity,
            "status": t.status,
            "created_at": t.created_at,
        }
        for t in transfers
    ]
    return Response(data)


# ------------------------
# GET BRANCH EMPLOYEES
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_branch_employees(request):
    """
    Fetch all employees from the logged-in user's branch.
    Returns minimal data (id, name).
    Handles errors safely for production use.
    """
    try:
        user = request.user  # Authenticated via JWT

        # ---------- Validate User Branch ----------
        if not user.branch:
            return Response(
                {"success": False, "message": "No branch assigned to the logged-in user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---------- Validate Branch Existence ----------
        try:
            branch = Branch.objects.get(id=user.branch.id)
        except Branch.DoesNotExist:
            return Response(
                {"success": False, "message": "Branch not found or deleted."},
                status=status.HTTP_404_NOT_FOUND
            )

        # ---------- Fetch Employees Safely ----------
        employees_qs = Employee.objects.filter(branch=branch, status='active').only('id', 'name')
        employees = [{"id": emp.id, "name": emp.name} for emp in employees_qs]

        if not employees:
            return Response(
                {
                    "success": True,
                    "branch": branch.name,
                    "employees": [],
                    "message": "No active employees found for this branch."
                },
                status=status.HTTP_200_OK
            )

        # ---------- Return Successful Response ----------
        return Response(
            {
                "success": True,
                "branch": branch.name,
                "employees": employees,
                "total_employees": len(employees)
            },
            status=status.HTTP_200_OK
        )

    # ---------- Error Handling ----------
    except DatabaseError as db_err:
        return Response(
            {"success": False, "message": "Database error occurred.", "error": str(db_err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        return Response(
            {"success": False, "message": "Something went wrong.", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_products(request):
    try:
        user = request.user

        # Response format (purchase-wise lots):
        # {
        #   "success": true,
        #   "count": 2,
        #   "branch": "Main Branch",
        #   "products": [
        #     {
        #       "product_id": 10,
        #       "variant_id": 21,
        #       "purchase_item_id": 501,
        #       "purchase_id": 120,
        #       "purchase_date": "2026-04-21",
        #       "purchase_bill_no": "BILL-784",
        #       "name": "Smart Watch",
        #       "brand": "XYZ",
        #       "subbrand": "Pro",
        #       "model": "M2",
        #       "selling_price": 2499.0,
        #       "minimum_selling_price": 2299.0,
        #       "qty": 3,
        #       "barcode": "STA2604E0178",
        #       "is_warranty_item": true,
        #       "warranty_period": "12",
        #       "hsn_code": "8517",
        #       "gst": {"cgst": 9.0, "sgst": 9.0, "igst": 18.0},
        #       "serial_numbers": ["SN1001", "SN1002", "SN1003"],
        #       "search_type": "product/barcode/model"
        #     }
        #   ]
        # }

        # ---------- Verify branch ----------
        if not hasattr(user, 'branch') or not user.branch:
            return Response(
                {"success": False, "message": "User is not assigned to any branch."},
                status=status.HTTP_400_BAD_REQUEST
            )

        branch = user.branch
        query = request.GET.get('q', '').strip()

        if not query:
            return Response(
                {"success": False, "message": "Search query (q) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # =====================================================
        # STEP 1: SEARCH BY SERIAL NUMBER
        # =====================================================
        serial_branch_stock = Stock.objects.filter(
            product_id=OuterRef('product_id'),
            variant_id=OuterRef('variant_id'),
            branch=branch,
            qty__gt=0
        )

        serial_obj = SerialNumber.objects.select_related(
            'product__hsn',
            'product__brand',
            'variant__model',
            'variant__subbrand',
            'purchase_item'
        ).annotate(
            in_branch_stock=Exists(serial_branch_stock)
        ).filter(
            serial_number__iexact=query,
            is_available=True,
            product__status='active',
            in_branch_stock=True
        ).first()

        if serial_obj:
            p = serial_obj.product
            v = serial_obj.variant
            hsn = p.hsn
            purchase_item = serial_obj.purchase_item

            selling_price = (
                purchase_item.selling_price
                if purchase_item and purchase_item.selling_price is not None
                else (v.selling_price if v and v.selling_price is not None else (p.selling_price or 0))
            )

            return Response({
                "success": True,
                "products": [{
                    "product_id": p.id,
                    "variant_id": v.id if v else None,

                    "name": p.name,
                    "brand": p.brand.name if p.brand else None,
                    "subbrand": v.subbrand.name if v and v.subbrand else None,
                    "model": v.model.name if v and v.model else None,

                    "selling_price": float(selling_price),
                    "minimum_selling_price": float(
                        v.minimum_selling_price if v and v.minimum_selling_price
                        else p.minimum_selling_price or 0
                    ),

                    "is_warranty_item": p.is_warranty_item,
                    "warranty_period": p.warranty_period,

                    "hsn_code": hsn.code if hsn else None,
                    "gst": {
                        "cgst": float(hsn.cgst) if hsn else 0,
                        "sgst": float(hsn.sgst) if hsn else 0,
                        "igst": float(hsn.igst) if hsn else 0,
                    },

                    "serial_number": serial_obj.serial_number,
                    "purchase_item_id": purchase_item.id if purchase_item else None,
                    "barcode": purchase_item.barcode if purchase_item else None,
                    "qty": 1,
                    "search_type": "serial_number"
                }],
                "message": "Matched via serial number"
            }, status=status.HTTP_200_OK)

        # =====================================================
        # STEP 2: SEARCH BY PRODUCT / BARCODE / MODEL
        # Return strict purchase-lot wise rows for correct billing price selection.
        # =====================================================
        barcode_match_subquery = PurchaseItem.objects.annotate(
            variant_key=Coalesce('variant_id', Value(0))
        ).filter(
            product_id=OuterRef('product_id'),
            variant_key=OuterRef('variant_key'),
            barcode__icontains=query
        )

        name_terms = [term for term in query.split() if term]
        name_all_terms_filter = Q()
        for term in name_terms:
            name_all_terms_filter &= Q(product__name__icontains=term)

        search_filter = (
            Q(product__name__iexact=query) |
            Q(product__name__istartswith=query) |
            Q(product__name__icontains=query) |
            Q(product__brand__name__icontains=query) |
            Q(variant__model__name__icontains=query) |
            Q(variant__subbrand__name__icontains=query) |
            Q(barcode_match=True)
        )

        if name_terms:
            search_filter |= name_all_terms_filter

        stocks = (
            Stock.objects.select_related(
                'product__hsn',
                'product__brand',
                'variant__model',
                'variant__subbrand',
                'branch'
            ).annotate(
                variant_key=Coalesce('variant_id', Value(0)),
                barcode_match=Exists(barcode_match_subquery)
            )
            .filter(
                branch=branch,
                product__status='active',
                qty__gt=0
            ).filter(
                search_filter
            )
        )
        
        if not stocks.exists():
            return Response(
                {"success": True, "products": [], "message": "No matching products found."},
                status=status.HTTP_200_OK
            )

        products = []

        for stock in stocks:
            p = stock.product
            v = stock.variant
            hsn = p.hsn
            remaining_branch_qty = int(stock.qty or 0)

            if remaining_branch_qty <= 0:
                continue

            purchase_items_qs = PurchaseItem.objects.select_related('purchase').filter(
                product=p,
                variant=v
            ).order_by('-purchase__purchase_date', '-id')

            barcode_items_qs = purchase_items_qs.filter(barcode__icontains=query)
            if barcode_items_qs.exists():
                purchase_items_qs = barcode_items_qs

            purchase_items_with_qty = []
            for purchase_item_obj in purchase_items_qs:
                purchase_item_qty = StockIn.objects.filter(
                    purchase_item=purchase_item_obj,
                    branch=branch
                ).aggregate(total=Sum('qty'))['total'] or 0

                if purchase_item_qty > 0:
                    purchase_items_with_qty.append((purchase_item_obj, purchase_item_qty))

            purchase_items = purchase_items_with_qty

            # Purchase-wise strict mode: if no available purchase lots, skip this stock row.
            if not purchase_items:
                continue

            for purchase_item, purchase_item_qty in purchase_items:
                if remaining_branch_qty <= 0:
                    break

                selling_price = (
                    purchase_item.selling_price
                    if purchase_item and purchase_item.selling_price is not None
                    else (v.selling_price if v and v.selling_price is not None else (p.selling_price or 0))
                )

                serial_numbers = []
                if p.is_warranty_item:
                    serial_qs = SerialNumber.objects.filter(
                        product=p,
                        variant=v,
                        is_available=True
                    )
                    if purchase_item:
                        serial_qs = serial_qs.filter(purchase_item=purchase_item)

                    serial_numbers = list(serial_qs.values_list('serial_number', flat=True))

                display_qty = purchase_item_qty
                if p.is_warranty_item:
                    display_qty = len(serial_numbers)

                display_qty = min(int(display_qty or 0), remaining_branch_qty)

                if p.is_warranty_item and serial_numbers:
                    serial_numbers = serial_numbers[:display_qty]

                if display_qty <= 0:
                    continue

                remaining_branch_qty -= display_qty

                products.append({
                    "product_id": p.id,
                    "variant_id": v.id if v else None,
                    "purchase_item_id": purchase_item.id if purchase_item else None,
                    "purchase_id": purchase_item.purchase_id if purchase_item else None,
                    "purchase_date": (
                        purchase_item.purchase.purchase_date.isoformat()
                        if purchase_item and purchase_item.purchase and purchase_item.purchase.purchase_date
                        else None
                    ),
                    "purchase_bill_no": (
                        purchase_item.purchase.bill_no
                        if purchase_item and purchase_item.purchase
                        else None
                    ),

                    "name": p.name,
                    "brand": p.brand.name if p.brand else None,
                    "subbrand": v.subbrand.name if v and v.subbrand else None,
                    "model": v.model.name if v and v.model else None,

                    "selling_price": float(selling_price),
                    "minimum_selling_price": float(
                        v.minimum_selling_price if v and v.minimum_selling_price
                        else p.minimum_selling_price or 0
                    ),

                    "qty": display_qty,
                    "barcode": purchase_item.barcode if purchase_item else None,

                    "is_warranty_item": p.is_warranty_item,
                    "warranty_period": p.warranty_period,

                    "hsn_code": hsn.code if hsn else None,
                    "gst": {
                        "cgst": float(hsn.cgst) if hsn else 0,
                        "sgst": float(hsn.sgst) if hsn else 0,
                        "igst": float(hsn.igst) if hsn else 0,
                    },

                    "serial_numbers": serial_numbers,
                    "search_type": "product/barcode/model"
                })

        if not products:
            return Response(
                {"success": True, "products": [], "message": "No matching products found."},
                status=status.HTTP_200_OK
            )

        for item in products:
            if item.get("is_warranty_item"):
                item["qty"] = len(item.get("serial_numbers") or [])

        return Response({
            "success": True,
            "count": len(products),
            "branch": branch.name,
            "products": products
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response(
            {"success": False, "message": "Something went wrong", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



# --------------------------
# CREATE BILL API
# --------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_bill(request):
    """
    Create a new bill with items, salesperson per product, and payment details.
    Expected JSON structure:
    {
        "customer": {"name": "Rahul", "phone": "9999999999"},
        "items": [
            {
                "product_id": 1,
                "variant_id": 11,
                "barcodes": ["STA2604E0178", "STA2604E0179"],
                "qty": 2,
                "price": 500,
                "discount_type": "fixed",
                "discount_value": 50,
                "salesperson_id": 3,
                "serial_numbers": ["SN001", "SN002"]
            },
            {
                "product_id": 2,
                "variant_id": null,
                "barcode": "ABC2604X0012",
                "qty": 1,
                "price": 1000,
                "discount_type": "percentage",
                "discount_value": 10,
                "salesperson_id": 4
            }
        ],
        "payment": {"payment_method": "split", "cash_amount": 400, "upi_amount": 600},
        "is_gst": true
    }
    """
    try:
        data = request.data
        user = request.user  # logged-in employee
        customer_data = data.get("customer")
        is_gst = data.get("is_gst", False)
        items_data = data.get("items", [])
        payment_data = data.get("payment")

        # --------------------------
        # VALIDATIONS
        # --------------------------
        if not customer_data or not customer_data.get("name"):
            return Response({"error": "Customer details required."}, status=status.HTTP_400_BAD_REQUEST)
        if not items_data:
            return Response({"error": "At least one item is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not payment_data:
            return Response({"error": "Payment details are required."}, status=status.HTTP_400_BAD_REQUEST)

        name = customer_data.get("name")
        with transaction.atomic():
            
            branch = Branch.objects.select_for_update().get(id=user.branch.id)
            
            # increment
            branch.last_bill_number += 1
            seq = branch.last_bill_number
            branch.save()

            # build bill_number: G-<BRANCHCODE_OR_ID>-YYYYMMDD-XXXX
            branch_identifier = getattr(branch, 'code', None) or str(branch.id)
            branch_identifier = str(branch_identifier).zfill(3)
            seq_str = str(seq).zfill(4)
            date_str = date.today().strftime('%Y%m%d')
            bill_number = f"G-{date_str}-{seq_str}"
            
            # --------------------------
            # CUSTOMER (get or create)
            # --------------------------
            customer, _ = Customer.objects.get_or_create(
                phone=customer_data.get("phone"),
                defaults={"name": name}
            )

            # --------------------------
            # CREATE BILL
            # --------------------------
            bill = Bill.objects.create(
                bill_number=bill_number,
                bill_name = name,
                customer=customer,
                branch=user.branch,
                is_gst=is_gst,
            )

            total_amount = Decimal(0)
            total_discount = Decimal(0)
            total_taxable_value = Decimal(0)
            total_cgst = Decimal(0)
            total_sgst = Decimal(0)
            total_igst = Decimal(0)

            # --------------------------
            # ADD ITEMS
            # --------------------------
            for item in items_data:
                product_id = item.get("product_id")
                variant_id = item.get("variant_id")
                purchase_item_id = item.get("purchase_item_id")
                purchase_item_ids = item.get("purchase_item_ids") or []
                barcode = str(item.get("barcode") or "").strip()
                barcode_list = item.get("barcodes") or item.get("barcode_list") or []
                qty = int(item.get("qty", 0))
                price = Decimal(item.get("price", 0))  # This is inclusive GST price
                discount_type = item.get("discount_type")
                discount_value = Decimal(item.get("discount_value", 0))
                salesperson_id = item.get("salesperson_id")
                serial_numbers = item.get("serial_numbers", [])  # Array of serial numbers

                if qty <= 0:
                    raise ValueError(f"Invalid quantity for product {product_id}")

                product = Product.objects.filter(id=product_id).first()
                if not product:
                    raise ValueError("Invalid product")

                variant = None
                if variant_id:
                    variant = ProductVariant.objects.filter(
                        id=variant_id,
                        product=product
                    ).first()
                    if not variant:
                        raise ValueError("Invalid variant for this product")

                # branch-wise global qty check (source of truth)
                stock = Stock.objects.select_for_update().filter(
                    product=product,
                    variant=variant,
                    branch=user.branch,
                    qty__gte=qty
                ).first()

                if not stock:
                    raise ValueError(f"Insufficient stock for {product.name}")

                requested_purchase_item_ids = []
                if purchase_item_id:
                    requested_purchase_item_ids.append(int(purchase_item_id))

                for pid in purchase_item_ids:
                    if pid is None:
                        continue
                    requested_purchase_item_ids.append(int(pid))

                requested_purchase_item_ids = list(dict.fromkeys(requested_purchase_item_ids))

                requested_barcodes = []
                if barcode:
                    requested_barcodes.append(barcode)
                for bcode in barcode_list:
                    if bcode is None:
                        continue
                    barcode_text = str(bcode).strip()
                    if barcode_text:
                        requested_barcodes.append(barcode_text)
                requested_barcodes = list(dict.fromkeys(requested_barcodes))

                purchase_items_qs = PurchaseItem.objects.filter(
                    product=product,
                    variant=variant
                ).order_by('id')

                if requested_barcodes:
                    purchase_items_qs = purchase_items_qs.filter(barcode__in=requested_barcodes)

                if requested_purchase_item_ids:
                    purchase_items_qs = purchase_items_qs.filter(id__in=requested_purchase_item_ids)

                candidate_purchase_items = list(purchase_items_qs)
                if not candidate_purchase_items and product.is_warranty_item:
                    raise ValueError(f"No purchase lots found for warranty product {product.name}")

                purchase_item_availability = []
                available_qty_by_purchase_item_id = {}
                purchase_item_by_id = {pi.id: pi for pi in candidate_purchase_items}

                for pi in candidate_purchase_items:
                    pi_stock_qs = StockIn.objects.select_for_update().filter(
                        purchase_item=pi,
                        branch=user.branch
                    )
                    pi_available_qty = pi_stock_qs.aggregate(total=Sum('qty'))['total'] or 0

                    if pi_available_qty > 0:
                        purchase_item_availability.append((pi, pi_available_qty))
                        available_qty_by_purchase_item_id[pi.id] = pi_available_qty

                total_available_qty = sum(av for _, av in purchase_item_availability)

                if product.is_warranty_item:
                    if total_available_qty <= 0:
                        raise ValueError(f"Selected purchase lots are not available in {user.branch.name}")
                    if total_available_qty < qty:
                        raise ValueError(f"Insufficient stock across purchase lots for {product.name}")

                purchase_allocations = []
                serial_obj_map = {}

                # find salesperson if provided
                salesperson = None
                if salesperson_id:
                    salesperson = Employee.objects.filter(id=salesperson_id, branch=user.branch).first()
                    if not salesperson:
                        raise ValueError(f"Salesperson with ID {salesperson_id} not found in this branch")


                # --------------------------
                # SERIAL NUMBER VALIDATION (for warranty items only)
                # --------------------------
                if product.is_warranty_item:
                    if len(serial_numbers) != qty:
                        raise ValueError("Serial count mismatch")

                    if len(set(serial_numbers)) != len(serial_numbers):
                        raise ValueError("Duplicate serial numbers found in request")

                    serial_objs = list(
                        SerialNumber.objects.select_for_update().filter(
                            serial_number__in=serial_numbers,
                            product=product,
                            variant=variant,
                            is_available=True
                        )
                    )

                    if len(serial_objs) != qty:
                        raise ValueError("One or more serial numbers are invalid or unavailable")

                    serial_obj_map = {s.serial_number: s for s in serial_objs}

                    if requested_purchase_item_ids:
                        for serial_obj in serial_objs:
                            if serial_obj.purchase_item_id not in requested_purchase_item_ids:
                                raise ValueError(
                                    f"Serial {serial_obj.serial_number} does not belong to selected purchase lot"
                                )
                    elif requested_barcodes:
                        for serial_obj in serial_objs:
                            if serial_obj.purchase_item_id not in purchase_item_by_id:
                                raise ValueError(
                                    f"Serial {serial_obj.serial_number} does not belong to selected barcode lot"
                                )

                    serial_count_by_purchase_item = {}
                    for serial_obj in serial_objs:
                        serial_count_by_purchase_item[serial_obj.purchase_item_id] = (
                            serial_count_by_purchase_item.get(serial_obj.purchase_item_id, 0) + 1
                        )

                    for pi_id, serial_count in serial_count_by_purchase_item.items():
                        if available_qty_by_purchase_item_id.get(pi_id, 0) < serial_count:
                            raise ValueError(f"Insufficient stock in purchase lot for serial items of {product.name}")

                    purchase_allocations = [
                        (purchase_item_by_id[pi_id], serial_count)
                        for pi_id, serial_count in serial_count_by_purchase_item.items()
                    ]
                else:
                    remaining_qty = qty
                    for pi, pi_available_qty in purchase_item_availability:
                        if remaining_qty <= 0:
                            break

                        consume_qty = min(remaining_qty, int(pi_available_qty))
                        if consume_qty > 0:
                            purchase_allocations.append((pi, consume_qty))
                            remaining_qty -= consume_qty

                    if remaining_qty > 0:
                        # Fallback for legacy/partial ledger: consume from global stock without purchase lot tagging.
                        purchase_allocations.append((None, remaining_qty))

                # --------------------------
                # DISCOUNT CALCULATIONS (on original price)
                # --------------------------
                if discount_type == 'percentage':
                    # For percentage: discount_amount = original price ka percentage
                    per_unit_discount = (price * discount_value / 100).quantize(Decimal('0.01'))
                    stored_discount_value = discount_value
                    discount_amount = (price * qty) * (discount_value / 100)
                else:
                    # For fixed: discount_value per unit
                    per_unit_discount = discount_value
                    stored_discount_value = per_unit_discount
                    discount_amount = discount_value

                # Final amount per unit after discount
                final_amount_per_unit = price - per_unit_discount
                item_total = (price * qty) - discount_amount

                # --------------------------
                # GST CALCULATIONS (only if is_gst = True)
                # --------------------------
                if is_gst:
                    hsn = product.hsn
                    if hsn:
                        # Calculate total GST percentage
                        total_gst_percent = hsn.cgst + hsn.sgst
                        
                        # Convert discounted price to exclusive price
                        final_exclusive_price = final_amount_per_unit / (1 + (total_gst_percent / 100))
                        final_exclusive_price = final_exclusive_price.quantize(Decimal('0.01'))
                        
                        # Calculate GST on final discounted exclusive price
                        cgst_amount = (final_exclusive_price * hsn.cgst / 100).quantize(Decimal('0.01'))
                        sgst_amount = (final_exclusive_price * hsn.sgst / 100).quantize(Decimal('0.01'))
                        igst_amount = (final_exclusive_price * hsn.igst / 100).quantize(Decimal('0.01'))
                        
                        # Taxable value is the exclusive price after discount
                        taxable_value_per_unit = final_exclusive_price
                    else:
                        taxable_value_per_unit = final_amount_per_unit
                        cgst_amount = sgst_amount = igst_amount = Decimal(0)
                else:
                    # No GST calculations
                    taxable_value_per_unit = Decimal(0)
                    cgst_amount = sgst_amount = igst_amount = Decimal(0)
                    hsn = None

                # --------------------------
                # CREATE BILL ITEMS
                # --------------------------
                if product.is_warranty_item and serial_numbers:
                    # Separate entry for each serial number
                    for serial_num in serial_numbers:
                        BillItem.objects.create(
                            bill=bill,
                            product=product,
                            variant=variant,
                            salesperson=salesperson,
                            qty=1,  # Each item has qty = 1
                            price=price,
                            discount_type=discount_type,
                            discount_value=stored_discount_value,
                            final_amount=final_amount_per_unit,
                            cgst_percent=hsn.cgst if hsn else 0,
                            sgst_percent=hsn.sgst if hsn else 0,
                            igst_percent=hsn.igst if hsn else 0,
                            taxable_value=taxable_value_per_unit,
                            cgst_amount=cgst_amount,
                            sgst_amount=sgst_amount,
                            igst_amount=igst_amount,
                            total=final_amount_per_unit,
                            serial_number=serial_num  # Store serial number
                        )

                        serial = serial_obj_map.get(serial_num)
                        if serial:
                            serial.is_available = False
                            serial.save(update_fields=['is_available'])
                        
                        # Update totals
                        total_amount += price
                        total_discount += per_unit_discount
                        if is_gst:
                            total_taxable_value += taxable_value_per_unit
                            total_cgst += cgst_amount
                            total_sgst += sgst_amount
                            total_igst += igst_amount
                else:
                    # Normal single entry
                    BillItem.objects.create(
                        bill=bill,
                        product=product,
                        salesperson=salesperson,
                        variant=variant,
                        qty=qty,
                        price=price,
                        discount_type=discount_type,
                        discount_value=stored_discount_value,
                        final_amount=final_amount_per_unit,
                        cgst_percent=hsn.cgst if hsn else 0,
                        sgst_percent=hsn.sgst if hsn else 0,
                        igst_percent=hsn.igst if hsn else 0,
                        taxable_value=taxable_value_per_unit,
                        cgst_amount=cgst_amount,
                        sgst_amount=sgst_amount,
                        igst_amount=igst_amount,
                        total=item_total
                    )
                    
                    # Update totals
                    total_amount += (price * qty)
                    total_discount += discount_amount
                    if is_gst:
                        total_taxable_value += (taxable_value_per_unit * qty)
                        total_cgst += (cgst_amount * qty)
                        total_sgst += (sgst_amount * qty)
                        total_igst += (igst_amount * qty)
                
                # --------------------------
                # COMMISSION CALCULATION
                # --------------------------
                if salesperson:
                    commission_amount = Decimal(0)
                    
                    # Calculate commission based on actual item total (after discount)
                    if product.is_warranty_item and serial_numbers:
                        actual_item_total = final_amount_per_unit * qty  # Total for all serial numbers
                    else:
                        actual_item_total = item_total  # Regular item total (from above calculation)
                    
                    if product.commission_type == 'fixed':
                        # Fixed per unit * quantity
                        commission_amount = product.commission_value * qty
                    elif product.commission_type == 'percentage':
                        # Percentage of item total after discount
                        commission_amount = (actual_item_total * product.commission_value) / 100

                    # Round off
                    commission_amount = commission_amount.quantize(Decimal('0.01'))

                    # --------------------------
                    # UPDATE SALESCOMMISSION
                    # --------------------------
                    current_month = date.today().strftime('%Y-%m')
                    sales_comm, _ = SalesCommission.objects.get_or_create(
                        salesperson=salesperson,
                        month=current_month,
                        defaults={'total_sales': 0, 'total_commission': 0}
                    )

                    sales_comm.total_sales += (price * qty)
                    sales_comm.total_commission += commission_amount
                    sales_comm.save()

                    # --------------------------
                    # UPDATE SALARY COMMISSION
                    # --------------------------
                    current_year = date.today().year
                    current_month_num = date.today().month

                    salary_obj, _ = Salary.objects.get_or_create(
                        employee=salesperson,
                        year=current_year,
                        month=current_month_num,
                        defaults={
                            'base_salary': Decimal(0),
                            'overtime_salary': Decimal(0),
                            'commission': Decimal(0),
                            'deduction': Decimal(0),
                        }
                    )

                    salary_obj.commission += commission_amount
                    salary_obj.save()


                # decrease branch quantity
                stock.qty -= qty
                stock.save()

                # purchase-level stock movement (sale)
                for allocated_purchase_item, allocated_qty in purchase_allocations:
                    StockIn.objects.create(
                        purchase_item=allocated_purchase_item,
                        product=product,
                        variant=variant,
                        branch=user.branch,
                        qty=-allocated_qty
                    )

            # --------------------------
            # PAYMENT
            # --------------------------
            payment_method = payment_data.get("payment_method")
            cash_amount = Decimal(payment_data.get("cash_amount") or 0)
            upi_amount = Decimal(payment_data.get("upi_amount") or 0)
            total_payment = cash_amount + upi_amount
            final_amount = total_amount - total_discount

            
            if payment_method == 'pay_later':
                customer.due_amount += final_amount
                customer.save()
            else:
                Payment.objects.create(
                    bill=bill,
                    payment_method=payment_method,
                    cash_amount=cash_amount if payment_method in ['cash', 'split'] else None,
                    upi_amount=upi_amount if payment_method in ['upi', 'split'] else None,
                    total_amount=total_payment,
                )

            # --------------------------
            # FINAL BILL TOTALS
            # --------------------------
            bill.total_amount = total_amount
            bill.total_discount = total_discount
            bill.total_taxable_value = total_taxable_value
            bill.total_cgst = total_cgst
            bill.total_sgst = total_sgst
            bill.total_igst = total_igst
            bill.final_amount = final_amount
            bill.save()
            
            # after bill.save() inside transaction.atomic()
            if not bill.customer.phone == "0000000000":
                try:
                    logo_path = request.build_absolute_uri('/media/logo/goldfire_logo.png')  # or wherever you keep logo
                    pdf_path = generate_bill_pdf_html(bill, BillItem.objects.filter(bill=bill), bill.branch, logo_path, output_dir="A:/STARTUP/GOLDFIRE/gf_backend/temp")
                except Exception as e:
                    print("PDF generation error:", e)

                media_id = None
                if pdf_path:
                    try:
                        media_id = upload_media(pdf_path, mime_type="application/pdf")
                    except Exception as e:
                        print("Media upload error:", e)
                        media_id = None

                try:
                    send_invoice_template(bill, media_id=media_id, template_name="goldfire_invoice")
                except Exception as e:
                    print("Template send error:", e)

            # --------------------------
            # SUCCESS RESPONSE
            # --------------------------
            return Response({
                "success": True,
                "message": "Bill created successfully.",
                "bill_id": bill.id,
                "bill_number": bill.bill_number,
                "final_amount": str(final_amount),
                "customer": customer.name,
                "branch": bill.branch.name
            }, status=status.HTTP_201_CREATED)

    except ValueError as ve:
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "Something went wrong while creating bill.", 'details': str(e),}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------------
# BILL LIST API (with pagination) BRANCH WISE
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bill_list(request):
    """
    Returns all bills for the logged-in user's branch.
    Optional filter: ?date=YYYY-MM-DD
    Pagination: ?page=1&page_size=10
    """
    try:
        user = request.user
        branch = getattr(user, 'branch', None)
        if not branch:
            return Response({"error": "User does not belong to any branch."}, status=status.HTTP_400_BAD_REQUEST)

        # Base queryset (branch-wise)
        bills = (
            Bill.objects.filter(branch=branch)
            .select_related('customer', 'branch')
            .prefetch_related('items__product', 'items__salesperson', 'payments')
            .order_by('-date')
        )

        # --------------------------
        # DATE FILTER (optional)
        # --------------------------
        date_str = request.query_params.get('date')
        if date_str:
            try:
                filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                bills = bills.filter(date__date=filter_date)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # --------------------------
        # PAGINATION
        # --------------------------
        paginator = BillPagination()
        paginated_bills = paginator.paginate_queryset(bills, request)

        serializer = BillListSerializer(paginated_bills, many=True)

        # DRF pagination response format
        return paginator.get_paginated_response({
            "success": True,
            "branch": branch.name,
            "filter_date": date_str or "All",
            "total_bills": bills.count(),
            "bills": serializer.data
        })

    except Exception as e:
        print("Bill List Error:", e)
        return Response({"error": "Something went wrong while fetching bills."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------------
# BILL LIST API (with pagination) ALL BRANCH
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bill_list_admin(request):
    try:
        branch_id = request.query_params.get("branch")
        search = request.query_params.get("search")

        # Base queryset
        bills = Bill.objects.all().select_related('customer', 'branch').prefetch_related('payments')

        if branch_id:
            bills = bills.filter(branch_id=branch_id)
        
        if search:
            bills = bills.filter(
                Q(bill_number__icontains=search)
            )
        # --------------------------
        # DATE FILTER 
        # --------------------------
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "date is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            bills = bills.filter(date__date=filter_date)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # --------------------------
        # REVENUE CALCULATIONS
        # --------------------------
        payments = Payment.objects.filter(bill__in=bills)

        total_revenue = bills.aggregate(total=Sum("final_amount"))["total"] or 0

        # For CASH
        cash_revenue = payments.filter(
            Q(payment_method="cash") | Q(payment_method="split")
        ).aggregate(
            total=Sum("cash_amount")
        )["total"] or 0

        # For UPI
        upi_revenue = payments.filter(
            Q(payment_method="upi") | Q(payment_method="split")
        ).aggregate(
            total=Sum("upi_amount")
        )["total"] or 0

        # For Pay Later
        pay_later_revenue = payments.filter(
            payment_method="pay_later"
        ).aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        # --------------------------
        # PAGINATION
        # --------------------------
        paginator = BillPagination()
        paginated_bills = paginator.paginate_queryset(bills, request)

        serializer = BillListSerializer(paginated_bills, many=True)

        # --------------------------
        # FINAL RESPONSE
        # --------------------------
        return paginator.get_paginated_response({
            "success": True,
            "date": date_str,
            "summary": {
                "total_bills": bills.count(),
                "total_revenue": total_revenue,
                "cash_revenue": cash_revenue,
                "upi_revenue": upi_revenue,
                "pay_later_revenue": pay_later_revenue,
            },
            "bills": serializer.data
        })

    except Exception as e:
        print("Bill List Error:", e)
        return Response({"error": "Something went wrong while fetching bills."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

# --------------------------
# BILL SEARCH API
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bill_search(request):
    """
    Search bills for the logged-in user's branch by:
    - Customer name
    - Customer phone
    - Bill number

    Example:
        /api/bills/search/?q=rahul
        /api/bills/search/?q=9999999999
        /api/bills/search/?q=G-20251105-0001
    """
    try:
        user = request.user
        branch = getattr(user, 'branch', None)
        if not branch:
            return Response({"error": "User does not belong to any branch."}, status=status.HTTP_400_BAD_REQUEST)

        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({"error": "Search query (q) is required."}, status=status.HTTP_400_BAD_REQUEST)

        # --------------------------
        # BASE QUERYSET (branch-wise)
        # --------------------------
        bills = (
            Bill.objects.filter(branch=branch)
            .select_related('customer', 'branch')
            .prefetch_related('items__product', 'items__salesperson', 'payments')
        )

        # --------------------------
        # SEARCH FILTER
        # --------------------------
        bills = bills.filter(
            Q(bill_name__icontains=query) |
            Q(customer__phone__icontains=query) |
            Q(bill_number__icontains=query)
        ).order_by('-date')

        # --------------------------
        # PAGINATION
        # --------------------------
        paginator = BillPagination()
        paginated_bills = paginator.paginate_queryset(bills, request)

        serializer = BillListSerializer(paginated_bills, many=True)
        # DRF pagination response (same as bill_list)
        return paginator.get_paginated_response({
            "success": True,
            "branch": branch.name,
            "search_query": query,
            "total_bills": bills.count(),
            "bills": serializer.data
        })

    except Exception as e:
        print("Bill Search Error:", e)
        return Response({"error": "Something went wrong while searching bills."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# ------------------------
# BILL RETURN API
# ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_return_bill(request):
    try:
        data = request.data
        user = request.user
        branch = getattr(user, 'branch', None)

        if not branch:
            return Response({"error": "User does not belong to any branch."}, status=status.HTTP_400_BAD_REQUEST)

        bill_id = data.get("bill_id")
        items_data = data.get("items", [])
        return_destination = data.get("return_destination", "")

        # 🔽 Refund info
        refund_type = data.get("refund_type", "")
        cash_amount = Decimal(data.get("cash_amount", 0) or 0)
        upi_amount = Decimal(data.get("upi_amount", 0) or 0)

        if not bill_id:
            return Response({"error": "bill_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not items_data:
            return Response({"error": "At least one return item is required."}, status=status.HTTP_400_BAD_REQUEST)

        bill = Bill.objects.filter(id=bill_id, branch=branch).first()
        if not bill:
            return Response({"error": "Invalid bill or does not belong to this branch."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            total_refund = Decimal(0)
            final_refund = Decimal(0)

            # 🔽 Create ReturnBill first
            return_bill = ReturnBill.objects.create(
                bill=bill,
                customer=bill.customer,
                branch=branch,
                refund_type=refund_type if refund_type in ['cash', 'upi', 'split'] else None,
                cash_amount=cash_amount,
                upi_amount=upi_amount,
                total_refund=0,
                return_destination=return_destination
            )

            # --------------------
            # Process Return Items
            # --------------------
            for item in items_data:
                bill_item_id = item.get("bill_item_id")
                qty = int(item.get("qty", 0))

                if qty <= 0:
                    raise ValueError("Invalid quantity provided.")

                bill_item = BillItem.objects.filter(id=bill_item_id, bill=bill).first()
                if not bill_item:
                    raise ValueError(f"Bill item {bill_item_id} not found.")

                if qty > bill_item.qty:
                    raise ValueError("Return qty cannot exceed sold qty.")
                
                bill_item.is_returned = True
                bill_item.save()
                
                refund_amount = bill_item.price * qty
                final_refund += refund_amount
                if refund_type:
                    total_refund += refund_amount

                ReturnItem.objects.create(
                    return_bill=return_bill,
                    product=bill_item.product,
                    original_bill_item=bill_item,
                    qty=qty,
                    price=bill_item.price,
                    total_refund=refund_amount,
                    salesperson=bill_item.salesperson
                )
                
                if return_bill.return_destination == 'stock':
                    product_qty, created = Quantity.objects.get_or_create(
                        product=bill_item.product,
                        branch=bill.branch,
                        defaults={'qty': 0}
                    )
                    product_qty.qty += qty
                    product_qty.save()
                    
                    if bill_item.product.is_warranty_item:
                        SerialNumber.objects.filter(
                            serial_number=bill_item.serial_number,
                            product=bill_item.product
                        ).update(is_available=True)
                    
                else:
                    today = now()

                    obj, created = VendorReturnMonthly.objects.get_or_create(
                        product=bill_item.product,
                        vendor=bill_item.product.vendor,
                        branch=return_bill.branch,
                        year=today.year,
                        month=today.month,
                        defaults={
                            "total_qty": qty
                        }
                    )

                    if not created:
                        obj.total_qty += qty
                        obj.save()

                # --------------------
                # Commission Reversal
                # --------------------
                salesperson = bill_item.salesperson
                if salesperson:
                    original_month = bill.date.strftime('%Y-%m')
                    original_year = bill.date.year
                    original_month_num = bill.date.month

                    if bill_item.product.commission_type == 'fixed':
                        commission_amount = bill_item.product.commission_value * qty
                    elif bill_item.product.commission_type == 'percentage':
                        commission_amount = ((bill_item.price * qty) * bill_item.product.commission_value) / 100
                    else:
                        commission_amount = Decimal(0)

                    commission_amount = commission_amount.quantize(Decimal('0.01'))

                    sales_comm, _ = SalesCommission.objects.get_or_create(
                        salesperson=salesperson,
                        month=original_month,
                        defaults={'total_sales': 0, 'total_commission': 0}
                    )
                    sales_comm.total_sales -= refund_amount
                    sales_comm.total_commission -= commission_amount
                    sales_comm.save()

                    salary_obj, _ = Salary.objects.get_or_create(
                        employee=salesperson,
                        year=original_year,
                        month=original_month_num,
                        defaults={
                            'base_salary': 0,
                            'overtime_salary': 0,
                            'commission': 0,
                            'deduction': 0,
                        }
                    )
                    salary_obj.commission -= commission_amount
                    salary_obj.save()

            # --------------------
            # 🔥 FINAL VALIDATION
            # --------------------
            if refund_type == 'cash' and cash_amount != total_refund:
                raise ValueError("Cash amount must match total refund.")

            if refund_type == 'upi' and upi_amount != total_refund:
                raise ValueError("UPI amount must match total refund.")

            # Update final refund
            if refund_type:
                return_bill.total_refund = total_refund
                return_bill.save()
            else:
                bill.customer.due_amount -= final_refund
                bill.customer.save()

            return Response({
                "success": True,
                "message": "Return processed successfully.",
                "return_bill_id": return_bill.id,
                "bill_number": bill.bill_number,
                "refund_type": refund_type,
                "cash_amount": str(cash_amount),
                "upi_amount": str(upi_amount),
                "total_refund": str(total_refund),
            }, status=status.HTTP_201_CREATED)

    except ValueError as ve:
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ReturnBill Error:", e)
        return Response({"error": "Something went wrong while processing the return."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------
# BILL RETURN API
# ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_list(request):
    try:
        search = request.GET.get("search", "").strip()

        customers = Customer.objects.annotate(
            total_bills=Count('bills'),
            total_spent=Sum('bills__final_amount')
        ).order_by('-created_at')

        # ---------------------------
        # 🔍 SEARCH FILTER
        # ---------------------------
        if search:
            customers = customers.filter(
                Q(name__icontains=search) |
                Q(phone__icontains=search)
            )

        # ---------------------------
        # Pagination
        # ---------------------------
        paginator = CustomerPagination()
        paginated_qs = paginator.paginate_queryset(customers, request)

        data = [
            {
                "id": c.id,
                "name": c.name,
                "phone": c.phone,
                "total_bills": c.total_bills or 0,
                "total_spent": float(c.total_spent or 0),
            }
            for c in paginated_qs
        ]

        return paginator.get_paginated_response(data)

    except Exception as e:
        print("Error:", e)
        return Response({"error": str(e)}, status=400)
  
  
# ---------------------------
# ALL BILLS FOR CUSTOMER
# ---------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_details_with_bills(request, pk):
    try:
        # --------------- CUSTOMER --------------------
        try:
            customer = Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        # ------- Summary: total bills & total spent --------
        summary = Bill.objects.filter(customer=customer).aggregate(
            total_bills=Count('id'),
            total_spent=Sum('final_amount')
        )

        # --------------- BILLS LIST --------------------
        bills = Bill.objects.filter(customer=customer).order_by('-date')

        # 🔍 Search by bill_number
        search = request.GET.get("search")
        if search:
            bills = bills.filter(bill_number__icontains=search)

        # 🔍 Filter by payment status = pay_later
        payment_status = request.GET.get("payment_status")
        if payment_status == "pay_later":
            bills = bills.filter(customer__due_amount__gt=0)

        # ------------ Pagination ----------------
        paginator = CustomerPagination()
        paginated_bills = paginator.paginate_queryset(bills, request)

        # ------------ Prepare Bills + Items ----------------
        bills_data = []

        for b in paginated_bills:

            bill_items = []
            for item in b.items.all():

                bill_items.append({
                    "item_id": item.id,
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "qty": item.qty,
                    "price": float(item.price),
                    "discount_type": item.discount_type,
                    "discount_value": float(item.discount_value),
                    "taxable_value": float(item.taxable_value),
                    "cgst_percent": float(item.cgst_percent),
                    "sgst_percent": float(item.sgst_percent),
                    "igst_percent": float(item.igst_percent),
                    "cgst_amount": float(item.cgst_amount),
                    "sgst_amount": float(item.sgst_amount),
                    "igst_amount": float(item.igst_amount),
                    "final_amount": float(item.final_amount),
                    "total": float(item.total),
                    "serial_number": item.serial_number,
                    "salesperson": {
                        "id": item.salesperson.id if item.salesperson else None,
                        "name": item.salesperson.name if item.salesperson else None,
                    }
                })

            bills_data.append({
                "bill_id": b.id,
                "bill_number": b.bill_number,
                "bill_name": b.bill_name,
                "date": b.date.strftime("%Y-%m-%d %H:%M"),
                "total_amount": float(b.total_amount),
                "total_discount": float(b.total_discount),
                "total_taxable_value": float(b.total_taxable_value),
                "total_cgst": float(b.total_cgst),
                "total_sgst": float(b.total_sgst),
                "total_igst": float(b.total_igst),
                "final_amount": float(b.final_amount),
                "branch": b.branch.name if b.branch else None,
                "items": bill_items,  # 🔥 FULL BILL ITEMS ATTACHED
            })

        # ----- FINAL RESPONSE -----
        response = {
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "phone": customer.phone,
                "due_amount": float(customer.due_amount or 0),
                "total_bills": summary["total_bills"] or 0,
                "total_spent": float(summary["total_spent"] or 0),
            },
            "bills": bills_data
        }

        return paginator.get_paginated_response(response)

    except Exception as e:
        print("Error:", e)
        return Response({"error": str(e)}, status=400)

 

def bills_show(request):
    bill = Bill.objects.get(bill_number='G-20251106-0058')
    items = BillItem.objects.filter(bill=bill)
    branch = bill.branch
    
    context = {
        'bill': bill,
        'items': items,
        'branch': branch,
        'is_gst': bill.is_gst,  # Pass is_gst from bill to template
    }

    return render(request, 'bills/invoice.html', context)


# --------------------------
# UPDATE CUSTOMER DUE
# --------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_bill_due(request):
    try:
        data = request.data
    
        bill_id = data.get("bill_id")
        payment_method = data.get("payment_method")
        cash_amount = Decimal(data.get("cash_amount", 0) or 0)
        upi_amount = Decimal(data.get("upi_amount", 0) or 0)

        if not bill_id:
            return Response({"error": "bill_id is required."}, status=400)

        bill = Bill.objects.filter(id=bill_id).select_related('customer').first()
        if not bill:
            return Response({"error": "Bill not found."}, status=404)

        customer = bill.customer
        if not customer:
            return Response({"error": "Bill has no customer."}, status=400)

        if customer.due_amount <= 0:
            return Response({"error": "No due amount for this customer."}, status=400)

        paid_amount = cash_amount + upi_amount
        if paid_amount <= 0:
            return Response({"error": "Payment amount must be greater than zero."}, status=400)

        if paid_amount > customer.due_amount:
            return Response(
                {"error": "Paid amount cannot exceed due amount."},
                status=400
            )

        with transaction.atomic():
            # Create Payment with BILL reference
            Payment.objects.create(
                bill=bill,
                payment_method=payment_method,
                cash_amount=cash_amount if cash_amount > 0 else None,
                upi_amount=upi_amount if upi_amount > 0 else None,
                total_amount=paid_amount
            )

            # Reduce customer due
            customer.due_amount -= paid_amount
            customer.save()

        return Response({
            "success": True,
            "message": "Bill due cleared successfully.",
            "bill_id": bill.id,
            "bill_number": bill.bill_number,
            "customer": customer.name,
            "payment_method": payment_method,
            "paid_amount": str(paid_amount),
            "remaining_due": str(customer.due_amount)
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("Pay Bill Due Error:", e)
        return Response(
            {"error": "Something went wrong while clearing bill due."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# --------------------------
# CREATE REPLACEMENT BILL
# --------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_replacement(request):
    try:
        data = request.data

        with transaction.atomic():

            bill = Bill.objects.select_for_update().get(id=data["bill_id"])
            replacement_type = data["replacement_type"]
            return_destination = data["return_destination"]
            items_data = data["items"]

            replacement_bill = ReplacementBill.objects.create(
                bill=bill,
                customer=bill.customer,
                branch=bill.branch,
                replacement_type=replacement_type,
                return_destination=return_destination
            )

            old_total = Decimal("0.00")
            new_total = Decimal("0.00")

            for item in items_data:

                bill_item = BillItem.objects.select_for_update().get(
                    id=item["bill_item_id"],
                    bill=bill
                )

                qty = bill_item.qty
                old_price = bill_item.final_amount
                old_total += bill_item.total

                # -------------------------
                # PRODUCT & PRICE
                # -------------------------
                if replacement_type == "warranty":
                    new_product = bill_item.product
                    new_price = bill_item.final_amount
                else:
                    new_product = Product.objects.get(id=item["new_product_id"])
                    new_price = Decimal(item.get("price", new_product.selling_price))

                discount_type = item.get("discount_type")
                discount_value = Decimal(item.get("discount_value", 0))

                # -------------------------
                # DISCOUNT CALC
                # -------------------------
                if discount_type == "percentage":
                    per_unit_discount = (new_price * discount_value / 100).quantize(Decimal("0.01"))
                elif discount_type == "fixed":
                    per_unit_discount = discount_value
                else:
                    per_unit_discount = Decimal("0.00")

                final_price = new_price - per_unit_discount

                # -------------------------
                # GST CHECK
                # -------------------------
                apply_gst = bill.is_gst or (
                    bill_item.cgst_percent + bill_item.sgst_percent > 0
                )

                if apply_gst:
                    hsn = new_product.hsn
                    gst_percent = (hsn.cgst + hsn.sgst) if hsn else Decimal(0)

                    taxable_value = (final_price / (1 + gst_percent / 100)).quantize(Decimal("0.01"))
                    cgst_amount = (taxable_value * hsn.cgst / 100).quantize(Decimal("0.01"))
                    sgst_amount = (taxable_value * hsn.sgst / 100).quantize(Decimal("0.01"))
                    igst_amount = (taxable_value * hsn.igst / 100).quantize(Decimal("0.01"))
                else:
                    taxable_value = Decimal(0)
                    cgst_amount = sgst_amount = igst_amount = Decimal(0)


                # -------------------------
                # STOCK HANDLING
                # -------------------------
                if return_destination == "stock":
                    product_qty, created = Quantity.objects.get_or_create(
                        product=bill_item.product,
                        branch=bill.branch,
                        defaults={'qty': 0}
                    )
                    product_qty.qty += qty
                    product_qty.save()
                    
                    if bill_item.product.is_warranty_item:
                        SerialNumber.objects.filter(
                            serial_number=bill_item.serial_number,
                            product=bill_item.product
                        ).update(is_available=True)
                    
                else:
                    today = now()
                    
                    obj, created = VendorReturnMonthly.objects.get_or_create(
                        product=bill_item.product,
                        vendor=bill_item.product.vendor,
                        branch=bill.branch,
                        year=today.year,
                        month=today.month,
                        defaults={
                            "total_qty": item.qty
                        }
                    )

                    if not created:
                        obj.total_qty += item.qty
                        obj.save()
                    
                # DECREASE NEW PRODUCT STOCK
                product_qty, created = Quantity.objects.get_or_create(
                        product=new_product,
                        branch=bill.branch,
                        defaults={'qty': 0}
                    )
                product_qty.qty -= qty
                product_qty.save()
            
                # SERIAL AVAILABILITY
                if bill_item.serial_number:
                    SerialNumber.objects.filter(
                        serial_number=bill_item.serial_number,
                        product=new_product
                    ).update(is_available=False)

                new_total += bill_item.total

                ReplacementItem.objects.create(
                    replacement_bill=replacement_bill,
                    old_bill_item=bill_item,
                    old_product=bill_item.product,
                    new_product=new_product,
                    qty=qty,
                    old_price=old_price,
                    new_price=new_price,
                    old_serial_number=item.get("old_serial_number"),
                    new_serial_number=item.get("new_serial_number")
                )

                # -------------------------
                # UPDATE BILL ITEM (🔥 MAIN POINT)
                # -------------------------
                bill_item.product = new_product
                bill_item.price = new_price
                bill_item.discount_type = discount_type
                bill_item.discount_value = discount_value
                bill_item.final_amount = final_price
                bill_item.taxable_value = taxable_value
                bill_item.cgst_amount = cgst_amount
                bill_item.sgst_amount = sgst_amount
                bill_item.igst_amount = igst_amount
                bill_item.total = final_price * qty

                # SERIAL UPDATE
                if "new_serial_number" in item:
                    bill_item.serial_number = item["new_serial_number"]

                bill_item.save()
                
            # -------------------------
            # FINAL AMOUNTS
            # -------------------------
            difference = new_total - old_total

            replacement_bill.old_total_amount = old_total
            replacement_bill.new_total_amount = new_total
            replacement_bill.difference_amount = difference
            replacement_bill.save()

            # -------------------------
            # PAYMENT / REFUND
            # -------------------------
            if difference > 0:
                p = data["payment"]
                ReplacementPayment.objects.create(
                    replacement_bill=replacement_bill,
                    payment_method=p["payment_method"],
                    cash_amount=p.get("cash_amount", 0),
                    upi_amount=p.get("upi_amount", 0),
                    total_amount=difference
                )

            if difference < 0:
                r = data["refund"]
                ReplacementRefund.objects.create(
                    replacement_bill=replacement_bill,
                    refund_method=r["refund_method"],
                    cash_amount=r.get("cash_amount", 0),
                    upi_amount=r.get("upi_amount", 0),
                    total_refund=abs(difference)
                )

            # -------------------------
            # UPDATE BILL TOTALS
            # -------------------------
            bill.total_amount = sum(i.price * i.qty for i in bill.items.all())
            bill.total_discount = sum(i.discount_value for i in bill.items.all())
            bill.final_amount = sum(i.total for i in bill.items.all())
            bill.save()

            return Response({
                "success": True,
                "replacement_id": replacement_bill.id,
                "difference_amount": str(difference)
            }, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
