import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer

def parse_json_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return {}

@csrf_exempt 
def customer_list_create(request):
    """
    Gets all customers or makes a new one
    """
    if request.method == 'GET':
        customers = Customer.objects.all().values('id', 'full_name', 'phone_number', 'identity_card_number')
        return JsonResponse(list(customers), safe=False)

    elif request.method == 'POST':
        data = parse_json_body(request)
        form = CustomerForm(data)
        if form.is_valid():
            customer = form.save()
            return JsonResponse(model_to_dict(customer), status=201) 
        else:
            return JsonResponse(form.errors, status=400)
    return HttpResponse(status=405) 

@csrf_exempt
def customer_detail_update_delete(request, identity_card_number):
    """
    For viewing, updating, or deleting a specific customer by identity_card_number.
    """
    try:
        customer = Customer.objects.get(identity_card_number=identity_card_number)
    except Customer.DoesNotExist:
        return JsonResponse(
            {'error': f'Customer with identity card number "{identity_card_number}" not found.'},
            status=200
        )
    except Customer.MultipleObjectsReturned:
        # Hemos encontrado varias cuentas asociadas a ese DNI.
        return JsonResponse(
            {'error': f'Error: Multiple customers found with identity card number "{identity_card_number}". Please check data integrity.'},
            status=200
        )

    if request.method == 'GET':
        return JsonResponse(model_to_dict(customer))

    elif request.method == 'PUT':
        data = parse_json_body(request)
        if data is None:
            return JsonResponse({'error': 'Invalid JSON data in request body.'}, status=400)

        form = CustomerForm(data, instance=customer) 
        if form.is_valid():
            customer = form.save()
            return JsonResponse(model_to_dict(customer))
        else:
            return JsonResponse(form.errors, status=400)

    elif request.method == 'DELETE':
        customer_id_for_message = customer.identity_card_number
        customer.delete()
        return JsonResponse(
            {'message': f'Customer with identity card number "{customer_id_for_message}" deleted successfully.'},
            status=200
        )

    # If method is not GET, PUT, or DELETE
    return JsonResponse({'error': f'Method {request.method} not allowed for this resource.'}, status=405)