from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, login_not_required

@login_required(login_url='login_page')
def dashboard(request):
    
    return render(request, 'dashboard.html', context={'title': 'Dashboard Page'})

def view_inventory(request):

    return render(request, 'view_inventory.html', context={'title': 'View Inventory'})


