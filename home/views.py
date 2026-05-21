from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.utils import timezone
from decimal import Decimal

from orders.models import Order
from inventory.models import Inventory
from customers.models import Customer

@login_required(login_url='login_page')
def dashboard(request):
    today = timezone.now().date()
    
    # Calculate Metrics
    total_orders = Order.objects.count()
    daily_sales = Order.objects.filter(created_at__date=today).aggregate(total=Sum('final_total'))['total'] or Decimal('0.00')
    pending_orders = Order.objects.filter(status='pending').count()
    low_stock_count = Inventory.objects.filter(
        initial_stock__lte=F('low_stock_threshold'),
        status=Inventory.Status.ACTIVE
    ).count()
    total_customers = Customer.objects.count()
    
    # Fetch lists
    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:5]
    critical_stock = Inventory.objects.filter(
        initial_stock__lte=F('low_stock_threshold'),
        status=Inventory.Status.ACTIVE
    ).order_by('initial_stock')[:5]

    context = {
        'title': 'Dashboard Page',
        'total_orders': total_orders,
        'daily_sales': daily_sales,
        'pending_orders': pending_orders,
        'low_stock_count': low_stock_count,
        'total_customers': total_customers,
        'recent_orders': recent_orders,
        'critical_stock': critical_stock,
    }
    return render(request, 'dashboard.html', context=context)

def view_inventory(request):
    return render(request, 'view_inventory.html', context={'title': 'View Inventory'})


