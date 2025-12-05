# apps/users/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model

User = get_user_model()

def login_signup_view(request):
    if request.user.is_authenticated:
        return redirect('products:index')

    if request.method == 'POST':
        action = request.POST.get('action')

        # SIGNUP
        if action == 'signup':
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            location_city = request.POST.get('location_city')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect('/users/login_signup/?show=signup')

            if User.objects.filter(username=email).exists():
                messages.error(request, "Email is already registered. Please login.")
                return redirect('/users/login_signup/?show=login')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name,
            )
            if hasattr(user, 'phone_number'):
                user.phone_number = phone_number
            if hasattr(user, 'location_city'):
                user.location_city = location_city
            user.save()

            messages.success(request, "Account created successfully! You can now login.")
            return redirect('/users/login_signup/?show=login')

        # LOGIN
        elif action == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('products:index')
            else:
                messages.error(request, "Invalid email or password!")
                return redirect('/users/login_signup/?show=login')

    return render(request, 'users/login_signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/users/login_signup/')
