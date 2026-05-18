from django.shortcuts import render, redirect

def dashboard(request):
    
    return render(request, 'dashboard.html', context={'title': 'Dashboard Page'})

def view_inventory(request):

    return render(request, 'view_inventory.html', context={'title': 'View Inventory'})


