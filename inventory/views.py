from django.shortcuts import render

def add_inventory(request):

    return render(request, "add_inventory.html", context={'title': 'Add Inventory'})
