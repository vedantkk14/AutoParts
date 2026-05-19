from django.shortcuts import render
from django.contrib.auth.decorators import login_required, login_not_required


@login_required(login_url='login_page')
def add_order(request):

    return render(request, 'add_orders.html', context={'title': 'Add New Order'})


@login_required(login_url='login_page')
def all_orders(request):

    return render(request, 'all_orders.html', context={'title': 'View All Orders'})
