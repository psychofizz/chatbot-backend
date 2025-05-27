import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict #
from .models import Customer
from .forms import CustomerForm

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
def customer_detail_update_delete(request, pk):
    """
    For viewing, updating, or deleting a specific customer by ID
    """
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'GET':
        return JsonResponse(model_to_dict(customer))

    elif request.method == 'PUT':
        data = parse_json_body(request)
        form = CustomerForm(data, instance=customer)
        if form.is_valid():
            customer = form.save()
            return JsonResponse(model_to_dict(customer))
        else:
            return JsonResponse(form.errors, status=400)

    elif request.method == 'DELETE':
        customer.delete()
        return JsonResponse({'message': 'Customer deleted successfully'}, status=204)
    return HttpResponse(status=405) 

