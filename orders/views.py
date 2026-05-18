from django.shortcuts import render

# orders section
def add_order(request):

    return render(request, 'add_orders.html', context={'title': 'Add New Order'})

def all_orders(request):

    return render(request, 'all_orders.html', context={'title': 'View All Orders'})
