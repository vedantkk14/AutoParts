from django.template import context
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .models import Customer
import json

# def create_customer(request):
#     if request.method == 'POST':
#         try:
#             # Parse JSON body
#             data = json.loads(request.body)
#             company_name = data.get('customer_company_name')
#             name = data.get('customer_name')
#             phone_str = data.get('customer_phone_number')
#             city = data.get('customer_city')
            
#             # Server-side validation
#             if not company_name or not name or not phone_str or not city:
#                 return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)
            
#             # Ensure the phone number contains only digits
#             cleaned_phone = ''.join(c for c in str(phone_str) if c.isdigit())
#             if not cleaned_phone:
#                 return JsonResponse({'status': 'error', 'message': 'Phone number must contain digits.'}, status=400)
            
#             try:
#                 phone = int(cleaned_phone)
#             except ValueError:
#                 return JsonResponse({'status': 'error', 'message': 'Invalid phone number format.'}, status=400)
            
#             # Create the customer in the database
#             customer = Customer.objects.create(
#                 customer_company_name=company_name.strip(),
#                 customer_name=name.strip(),
#                 customer_phone_number=phone,
#                 customer_city=city.strip()
#             )
            
#             return JsonResponse({
#                 'status': 'success',
#                 'customer': {
#                     'id': customer.id,
#                     'customer_company_name': customer.customer_company_name,
#                     'customer_name': customer.customer_name,
#                     'customer_phone_number': str(customer.customer_phone_number),
#                     'customer_city': customer.customer_city
#                 }
#             })
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def create_customer(request):
    return render(request, 'create_customer.html', context={'title': 'Add New Customer'})


def view_customers(request):

    return render(request, 'view_customers.html', context={'title': 'View Customers'})