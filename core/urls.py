"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from os import name
from django.views.generic import View
from django.db import router
from django.contrib import admin
from django.urls import path

from home.views import *
from orders.views import *
from inventory.views import *
from customers.views import *
from analytics.views import *
from accounts.views import *

urlpatterns = [
    path(route='', view=dashboard, name='dashboard'),

    #login section
    path(route='login_page/', view=login_page, name='login_page'),
    path(route='logout/', view=logout_view, name='logout'),
    
    #paths for orders section
    path(route='add_orders/', view=add_order, name='add_order'),
    path(route='all_orders/', view=all_orders, name='all_orders'),
    
    #paths for customers/clients section
    path(route='customers/create/', view=create_customer, name='create_customer'),
    path(route='create_customer/', view=create_customer, name='create_customer'),
    path(route='view_customers/', view=view_customers, name='view_customers'),

    path(route='customers/delete/<int:customer_id>/', view=delete_customer, name='delete_customer'),
    path(route='customers/update/<int:customer_id>/', view=update_customer, name='update_customer'),

    #paths for inventory section
    path(route='add_inventory/', view=add_inventory, name='add_inventory'),
    path(route='view_inventory/', view=view_inventory, name='view_inventory'),

    #paths for analytics section
    path(route='view_analytics/', view=view_analytics, name='view_analytics'),
    
    path("admin/", admin.site.urls),
]
