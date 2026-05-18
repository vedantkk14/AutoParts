from django.shortcuts import render

def view_analytics(request):
    
    return render(request, 'view_analytics.html', context={'title':'Business Analytics'})