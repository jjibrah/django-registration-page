from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect("register")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required()
def home(request):
    return render(request, 'home.html')
