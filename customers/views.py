from django.template import context
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import *
import json
from django.contrib.auth.decorators import login_required, login_not_required
from django.shortcuts import get_object_or_404


# “Am I returning a webpage or returning data?”
# That single question decides whether to use:   render() or JsonResponse()

# Traditional Django flow:
#     Browser Request → Django View → render() → HTML Page → Browser reloads page

# JSON/AJAX flow:
#     Browser loads page → JavaScript sends request → Backend returns JSON → Frontend updates UI dynamically


@login_required(login_url='login_page')
def create_customer(request):
    if request.method == 'POST':
        # Check if content type is JSON
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                company_name = data.get('customer_company_name')
                name = data.get('customer_name')
                phone_str = data.get('customer_phone_number')
                city = data.get('customer_city')
            except json.JSONDecodeError as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
            # Validation
            if not company_name:
                return JsonResponse({'status': 'error', 'message': 'Company name is required.'}, status=400)
            
            phone = None
            if phone_str:
                cleaned_phone = ''.join(c for c in str(phone_str) if c.isdigit())
                if not cleaned_phone:
                    return JsonResponse({'status': 'error', 'message': 'Phone number must contain digits only.'}, status=400)
                try:
                    phone = int(cleaned_phone)
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid phone number format.'}, status=400)
            
            customer = Customer.objects.create(
                customer_company_name=company_name.strip(),
                customer_name=name.strip() if name else '',
                customer_phone_number=phone,
                customer_city=city.strip() if city else ''
            )
            return JsonResponse({
                'status': 'success',
                'customer': {
                    'id': customer.id,
                    'customer_company_name': customer.customer_company_name,
                    'customer_name': customer.customer_name,
                    'customer_phone_number': str(customer.customer_phone_number) if customer.customer_phone_number else '',
                    'customer_city': customer.customer_city
                }
            })
        else:
            # Standard HTML form POST
            company_name = request.POST.get('customer_company_name')
            name = request.POST.get('customer_name')
            phone_str = request.POST.get('customer_phone_number')
            city = request.POST.get('customer_city')
            
            # Validation
            if not company_name:
                messages.error(request, 'Company name is required.')
                return render(request, 'create_customer.html', context={'title': 'Add New Customer'})
            
            phone = None
            if phone_str:
                cleaned_phone = ''.join(c for c in str(phone_str) if c.isdigit())
                if not cleaned_phone:
                    messages.error(request, 'Phone number must contain digits only.')
                    return render(request, 'create_customer.html', context={'title': 'Add New Customer'})
                try:
                    phone = int(cleaned_phone)
                except ValueError:
                    messages.error(request, 'Invalid phone number format.')
                    return render(request, 'create_customer.html', context={'title': 'Add New Customer'})
            
            # Create Customer
            Customer.objects.create(
                customer_company_name=company_name.strip(),
                customer_name=name.strip() if name else '',
                customer_phone_number=phone,
                customer_city=city.strip() if city else ''
            )
            messages.success(request, 'Customer created successfully.')
            return redirect('view_customers')
            
    # GET request: render the HTML page
    return render(request, 'create_customer.html', context={'title': 'Add New Customer'})


@login_required(login_url='login_page')
def view_customers(request):
    search_query = request.GET.get('search', '').strip()
    selected_region = request.GET.get('region', '').strip()
    
    customers_qs = Customer.objects.all().order_by('-created_at')
    
    if selected_region:
        customers_qs = customers_qs.filter(customer_city__iexact=selected_region)
        
    if search_query:
        phone_q = Q()
        if search_query.isdigit():
            phone_q = Q(customer_phone_number=int(search_query)) | Q(id=int(search_query))
        
        customers_qs = customers_qs.filter(
            Q(customer_company_name__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(customer_city__icontains=search_query) |
            phone_q
        )
        
    paginator = Paginator(customers_qs, 10)             # 10 customers per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    total_customers = Customer.objects.count()
    
    regions = Customer.objects.exclude(customer_city='').exclude(customer_city__isnull=True).values_list('customer_city', flat=True).distinct().order_by('customer_city')
    
    return render(request, 'view_customers.html', context={
        'title': 'View Customers',
        'customers': page_obj,
        'page_obj': page_obj,
        'total_customers': total_customers,
        'search_query': search_query,
        'regions': regions,
        'selected_region': selected_region
    })


@login_required(login_url='login_page')
def delete_customer(request, customer_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to update records.')
        return redirect('login_page')
        
    if request.method == 'POST':
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return JsonResponse({'status': 'success', 'message': 'Customer deleted successfully.'})
        except Customer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Customer not found.'}, status=404)
    return redirect('view_customers')


@login_required(login_url='login_page')
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        # Check if content type is JSON
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                company_name = data.get('customer_company_name')
                name = data.get('customer_name')
                phone_str = data.get('customer_phone_number')
                city = data.get('customer_city')
            except json.JSONDecodeError as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
            # Validation
            if not company_name:
                return JsonResponse({'status': 'error', 'message': 'Company name is required.'}, status=400)
            
            phone = None
            if phone_str:
                cleaned_phone = ''.join(c for c in str(phone_str) if c.isdigit())
                if not cleaned_phone:
                    return JsonResponse({'status': 'error', 'message': 'Phone number must contain digits only.'}, status=400)
                try:
                    phone = int(cleaned_phone)
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid phone number format.'}, status=400)
            
            customer.customer_company_name = company_name.strip()
            customer.customer_name = name.strip() if name else ''
            customer.customer_phone_number = phone
            customer.customer_city = city.strip() if city else ''
            customer.save()
            return JsonResponse({
                'status': 'success',
                'customer': {
                    'id': customer.id,
                    'customer_company_name': customer.customer_company_name,
                    'customer_name': customer.customer_name,
                    'customer_phone_number': str(customer.customer_phone_number) if customer.customer_phone_number else '',
                    'customer_city': customer.customer_city
                }
            })

        else:
            # Standard HTML form POST
            company_name = request.POST.get('customer_company_name')
            name = request.POST.get('customer_name')
            phone_str = request.POST.get('customer_phone_number')
            city = request.POST.get('customer_city')
            
            # Validation
            if not company_name:
                messages.error(request, 'Company name is required.')
                return render(request, 'update_customer.html', context={'title': 'Edit Customer', 'customer': customer})
            
            phone = None
            if phone_str:
                cleaned_phone = ''.join(c for c in str(phone_str) if c.isdigit())
                if not cleaned_phone:
                    messages.error(request, 'Phone number must contain digits only.')
                    return render(request, 'update_customer.html', context={'title': 'Edit Customer', 'customer': customer})
                try:
                    phone = int(cleaned_phone)
                except ValueError:
                    messages.error(request, 'Invalid phone number format.')
                    return render(request, 'update_customer.html', context={'title': 'Edit Customer', 'customer': customer})
            
            customer.customer_company_name = company_name.strip()
            customer.customer_name = name.strip() if name else ''
            customer.customer_phone_number = phone
            customer.customer_city = city.strip() if city else ''
            customer.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('view_customers')
            
    # GET request: render the HTML page
    return render(request, 'update_customer.html', context={'title': 'Edit Customer', 'customer': customer})
        

