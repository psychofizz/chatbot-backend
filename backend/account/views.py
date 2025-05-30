import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction as db_transaction
from django.db.models import Sum, DecimalField
from decimal import Decimal
from .models import Invoice
from customers.models import Customer
from .serializers import InvoiceSerializer, CreateInvoiceSerializer

@csrf_exempt
def get_customer_invoices_view(request, identity_card_number):
    """
    Get all invoices for a specific customer using their identity_card_number.
    """
    if request.method == 'GET':
        try:
            customer = Customer.objects.get(identity_card_number=identity_card_number)
            invoices = customer.invoices.all() 
            
            if not invoices.exists():
                return JsonResponse([], safe=False, status=200) 

            serializer = InvoiceSerializer(invoices, many=True) 
            return JsonResponse(serializer.data, safe=False, status=200)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
    else:
        return JsonResponse({'error': 'Only GET method allowed'}, status=405)
    

@csrf_exempt
def get_customer_amount_owed(request, identity_card_number):
    """
    Calculate and return the total amount owed by a customer from their unpaid invoices.
    """
    if request.method == 'GET':
        try:
            customer = Customer.objects.get(identity_card_number=identity_card_number)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)


        total_owed_sum = customer.invoices.filter(is_paid=False).aggregate(
            total_amount=Sum('amount_due', output_field=DecimalField())
        )

        total_owed = total_owed_sum['total_amount'] if total_owed_sum['total_amount'] is not None else Decimal('0.00')
        
        if not isinstance(total_owed, Decimal):
            try:
                total_owed = Decimal(str(total_owed))
            except Exception:
                total_owed = Decimal('0.00')

        return JsonResponse({
            'total_amount_owed': f"{total_owed:.2f}"
        }, status=200)
    else:
        return JsonResponse({'error': 'Only GET method allowed'}, status=405)


@csrf_exempt
@db_transaction.atomic
def create_invoice_view(request):
    """
    Create a new invoice.
    Expects JSON body with 'customer_identity_card_number' and 'amount_due'.
    {
        "customer_identity_card_number": "0000000000000",
        "amount_due": 100.00
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        serializer = CreateInvoiceSerializer(data=data)
        if serializer.is_valid():
            customer_identity_card = serializer.validated_data['customer_identity_card_number']
            amount_due = serializer.validated_data['amount_due']

            try:
                customer = Customer.objects.get(identity_card_number=customer_identity_card)
            except Customer.DoesNotExist:
                return JsonResponse({'error': 'Customer not found'}, status=404) 

            invoice = Invoice.objects.create(
                customer=customer,
                amount_due=amount_due
            )
            response_serializer = InvoiceSerializer(invoice)
            return JsonResponse(response_serializer.data, status=201)
        else:
            return JsonResponse({'errors': serializer.errors}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
@db_transaction.atomic
def pay_invoice_view(request, invoice_id):
    """
    Mark an invoice as paid.
    (This view remains largely the same as it operates on a single invoice ID)
    """
    if request.method == 'PUT': 
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return JsonResponse({'error': 'Invoice not found'}, status=404)

        if invoice.is_paid:
            return JsonResponse({'message': 'Invoice is already paid'}, status=200)

        invoice.is_paid = True
        invoice.save()
        
        serializer = InvoiceSerializer(invoice)
        return JsonResponse(serializer.data, status=200)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)