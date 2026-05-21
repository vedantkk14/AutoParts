from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import *


@login_required(login_url='login_page')
def add_inventory(request):
    if request.method == 'POST':
        part_name = request.POST.get('part_name')
        sku = request.POST.get('sku')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        description = request.POST.get('description', '')
        
        initial_stock = request.POST.get('initial_stock') or 0
        low_stock_threshold = request.POST.get('low_stock_threshold') or 5
        aisle_location = request.POST.get('aisle_location', '')
        bin_location = request.POST.get('bin_location', '')
        
        wholesale_price = request.POST.get('wholesale_price') or 0.00
        retail_price = request.POST.get('retail_price') or 0.00
        is_taxable = request.POST.get('is_taxable') == 'on'
        
        # Action button logic: draft or active
        action = request.POST.get('action')
        if action == 'draft':
            status = 'draft'
        elif action == 'active':
            status = 'active'
        else:
            status = request.POST.get('status', 'draft')

        image = request.FILES.get('image')

        # Simple validation
        if not part_name or not sku or not category:
            messages.error(request, 'Part Name, SKU, and Category are required fields.')
        else:
            try:
                # Check for duplicate SKU
                if Inventory.objects.filter(sku=sku).exists():
                    messages.error(request, f'An item with SKU {sku} already exists.')
                else:
                    item = Inventory.objects.create(
                        part_name=part_name,
                        sku=sku,
                        category=category,
                        brand=brand,
                        description=description,
                        initial_stock=initial_stock,
                        low_stock_threshold=low_stock_threshold,
                        aisle_location=aisle_location,
                        bin_location=bin_location,
                        wholesale_price=wholesale_price,
                        retail_price=retail_price,
                        is_taxable=is_taxable,
                        image=image,
                        status=status
                    )

                    # Save Vehicle Compatibilities
                    makes = request.POST.getlist('make')
                    model_names = request.POST.getlist('model_name')
                    year_ranges = request.POST.getlist('year_range')

                    for make, model_name, year_range in zip(makes, model_names, year_ranges):
                        if make and model_name: # make sure it is not empty
                            VehicleCompatibility.objects.create(
                                part=item,
                                make=make,
                                model_name=model_name,
                                year_range=year_range
                            )

                    messages.success(request, f'Item "{part_name}" has been successfully added.')
                    return redirect('add_inventory')
            except Exception as e:
                messages.error(request, f'Error adding item: {str(e)}')

    categories = Inventory.Category.choices
    brands = Inventory.Brand.choices
    statuses = Inventory.Status.choices
    car_brands = VehicleCompatibility.Make.choices

    return render(request, "add_inventory.html", context={
        'title': 'Add Inventory',
        'categories': categories,
        'brands': brands,
        'statuses': statuses,
        'car_brands' : car_brands
    })


from django.db.models import Q

@login_required(login_url='login_page')
def view_inventory(request):
    query = request.GET.get('q', '')
    make_filter = request.GET.get('make', '')
    brand_filter = request.GET.get('brand', '')
    category_filter = request.GET.get('category', '')
    sort_by = request.GET.get('sort_by', '')

    items = Inventory.objects.all()

    # Search query
    if query:
        items = items.filter(
            Q(part_name__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query)
        )

    # Filter by make
    if make_filter:
        items = items.filter(vehicle_compatibilities__make=make_filter).distinct()

    # Filter by brand
    if brand_filter:
        items = items.filter(brand=brand_filter)

    # Filter by category
    if category_filter:
        items = items.filter(category=category_filter)

    # Sorting
    if sort_by == 'stock_low_high':
        items = items.order_by('initial_stock')
    elif sort_by == 'price_high_low':
        items = items.order_by('-retail_price')
    else:
        items = items.order_by('-created_at')

    # Get dropdown options from models
    categories = Inventory.Category.choices
    brands = Inventory.Brand.choices
    makes = VehicleCompatibility.Make.choices

    return render(request, 'view_inventory.html', context={
        'title': 'View Inventory',
        'item_info': items,
        'categories': categories,
        'brands': brands,
        'makes': makes,
        'query': query,
        'selected_make': make_filter,
        'selected_brand': brand_filter,
        'selected_category': category_filter,
        'selected_sort': sort_by,
    })


@login_required(login_url='login_page')
def edit_inventory(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    
    if request.method == 'POST':
        part_name = request.POST.get('part_name')
        sku = request.POST.get('sku')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        description = request.POST.get('description', '')
        
        initial_stock = request.POST.get('initial_stock') or 0
        low_stock_threshold = request.POST.get('low_stock_threshold') or 5
        aisle_location = request.POST.get('aisle_location', '')
        bin_location = request.POST.get('bin_location', '')
        
        wholesale_price = request.POST.get('wholesale_price') or 0.00
        retail_price = request.POST.get('retail_price') or 0.00
        is_taxable = request.POST.get('is_taxable') == 'on'
        
        action = request.POST.get('action')
        if action == 'draft':
            status = 'draft'
        elif action == 'active':
            status = 'active'
        else:
            status = request.POST.get('status', 'draft')

        image = request.FILES.get('image')

        if not part_name or not sku or not category:
            messages.error(request, 'Part Name, SKU, and Category are required fields.')
        else:
            try:
                # Check for duplicate SKU excluding current item
                if Inventory.objects.filter(sku=sku).exclude(id=item_id).exists():
                    messages.error(request, f'An item with SKU {sku} already exists.')
                else:
                    item.part_name = part_name
                    item.sku = sku
                    item.category = category
                    item.brand = brand
                    item.description = description
                    item.initial_stock = int(initial_stock)
                    item.low_stock_threshold = int(low_stock_threshold)
                    item.aisle_location = aisle_location
                    item.bin_location = bin_location
                    item.wholesale_price = float(wholesale_price)
                    item.retail_price = float(retail_price)
                    item.is_taxable = is_taxable
                    item.status = status
                    
                    if image:
                        item.image = image
                    
                    item.save()

                    # Re-create VehicleCompatibilities
                    # Delete old ones first
                    item.vehicle_compatibilities.all().delete()
                    
                    makes = request.POST.getlist('make')
                    model_names = request.POST.getlist('model_name')
                    year_ranges = request.POST.getlist('year_range')

                    for make, model_name, year_range in zip(makes, model_names, year_ranges):
                        if make and model_name:
                            VehicleCompatibility.objects.create(
                                part=item,
                                make=make,
                                model_name=model_name,
                                year_range=year_range
                            )

                    messages.success(request, f'Item "{part_name}" has been successfully updated.')
                    return redirect('edit_inventory', item_id=item.id)
            except Exception as e:
                messages.error(request, f'Error updating item: {str(e)}')

    categories = Inventory.Category.choices
    brands = Inventory.Brand.choices
    statuses = Inventory.Status.choices
    car_brands = VehicleCompatibility.Make.choices

    return render(request, "edit_inventory.html", context={
        'title': 'Edit Inventory',
        'item': item,
        'categories': categories,
        'brands': brands,
        'statuses': statuses,
        'car_brands': car_brands,
        'compatibilities': item.vehicle_compatibilities.all()
    })


@login_required(login_url='login_page')
@require_POST
def delete_inventory(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    part_name = item.part_name
    item.delete()
    return JsonResponse({'status': 'success', 'message': f'Item "{part_name}" has been successfully deleted.'})