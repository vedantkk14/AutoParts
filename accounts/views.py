from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, login_not_required
from django.contrib import messages
from django.contrib.auth import get_user_model


def login_page(request):

    if request.method == "POST":
        
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(
            request,
            phone_number=phone_number,
            password=password
        )

        if user is not None:
            login(request, user)

            if remember_me:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
        
            return redirect('dashboard')

        else:
            User = get_user_model()
            if not User.objects.filter(phone_number=phone_number).exists():
                messages.error(request, "Invalid Phone number.")
            else:
                messages.error(request, "Incorrect password.")


    return render(request, 'login_pg.html', context={'title' : 'Login Page'})


def logout_view(request):
    logout(request)
    return redirect('login_page')