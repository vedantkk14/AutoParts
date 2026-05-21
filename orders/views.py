import json
from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from inventory.models import Inventory
from .models import Order, OrderItem


@login_required(login_url='login_page')
def add_order(request):
    all_customers = Customer.objects.all()
    inventory_items = Inventory.objects.filter(
        status=Inventory.Status.ACTIVE
    ).prefetch_related('vehicle_compatibilities')
    return render(request, 'add_orders.html', context={
        'title': 'Add New Order',
        'customers': all_customers,
        'inventory_items': inventory_items,
    })


@login_required(login_url='login_page')
@require_POST
def save_order(request):
    """
    Accepts a JSON payload:
    {
        "customer_id": 5,
        "items": [
            { "id": 12, "qty": 3, "price": 450.00 },
            ...
        ],
        "discount_percent": 10
    }
    """
    try:
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        items_data = data.get('items', [])
        discount_percent = Decimal(str(data.get('discount_percent', 10)))

        if not customer_id:
            return JsonResponse({'status': 'error', 'message': 'Please select a customer.'}, status=400)

        if not items_data:
            return JsonResponse({'status': 'error', 'message': 'Please add at least one item to the order.'}, status=400)

        customer = get_object_or_404(Customer, id=customer_id)

        # Create the order
        order = Order.objects.create(
            customer=customer,
            discount_percent=discount_percent,
        )

        subtotal = Decimal('0.00')

        for item_data in items_data:
            inv_item = get_object_or_404(Inventory, id=item_data['id'])
            qty = int(item_data['qty'])
            unit_price = Decimal(str(item_data['price']))
            line_total = unit_price * qty

            OrderItem.objects.create(
                order=order,
                inventory_item=inv_item,
                quantity=qty,
                unit_price=unit_price,
                line_total=line_total,
            )

            subtotal += line_total

        discount_amount = subtotal * discount_percent / Decimal('100')
        final_total = subtotal - discount_amount

        order.subtotal = subtotal
        order.discount_amount = discount_amount
        order.final_total = final_total
        order.save()

        return JsonResponse({
            'status': 'success',
            'message': f'Order ORD-{order.id:05d} saved successfully!',
            'order_id': order.id,
        })

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid request data.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url='login_page')
def all_orders(request):
    orders = Order.objects.select_related('customer').prefetch_related('items__inventory_item').all()
    return render(request, 'all_orders.html', context={
        'title': 'View All Orders',
        'orders': orders,
    })


@login_required(login_url='login_page')
@require_POST
def update_order_status(request, order_id):
    """Update the status of an order via AJAX."""
    try:
        data = json.loads(request.body)
        new_status = data.get('status', '')

        valid_statuses = [choice[0] for choice in Order.Status.choices]
        if new_status not in valid_statuses:
            return JsonResponse({'status': 'error', 'message': 'Invalid status value.'}, status=400)

        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])

        return JsonResponse({
            'status': 'success',
            'message': f'Order ORD-{order.id:05d} status updated to {order.get_status_display()}.',
            'new_status': new_status,
            'new_status_display': order.get_status_display(),
        })

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid request data.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
