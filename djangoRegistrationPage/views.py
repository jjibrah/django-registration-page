from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Products

# Start of mpesa related imports
from django_daraja.mpesa import utils
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from datetime import datetime

# End of mpesa related imports

# Start of Mpesa instances and variables
cl = MpesaClient()
stk_push_callback_url = "https://api.darajambili.com/express-payment"
b2c_callback_url = ""


# End of Mpesa instances and variables


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


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def add_product(request):
    if request.method == "POST":
        p_name = request.POST.get('jina')
        p_quantity = request.POST.get('kiasi')
        p_price = request.POST.get('bei')
        product = Products(prod_name=p_name, prod_quantity=p_quantity,
                           prod_price=p_price)
        product.save()
        messages.success(request, 'Product saved successfully!')
        return redirect('add-product')
    return render(request, 'add-product.html')


@login_required()
def view_products(request):
    # select all the product from the database
    products = Products.objects.all()
    # Render the templates with products
    return render(request, 'products.html', {'products': products})


@login_required()
def delete_product(request, id):
    # select the product you need to delete
    product = Products.objects.get(id=id)
    # finally delete the product
    product.delete()
    # Redirect back to product page with a success message
    messages.success(request, 'Product deleted successfully')
    return redirect('products')


@login_required()
def update_product(request, id):
    # select the product to be updated
    product = Products.objects.get(id=id)
    # check if the form has any submitted record to receive them
    if request.method == "POST":
        updated_name = request.POST.get('jina')
        updated_quantity = request.POST.get('kiasi')
        updated_price = request.POST.get('bei')

        # Update the selected product above with the received data
        product.prod_name = updated_name
        product.prod_quantity = updated_quantity
        product.prod_price = updated_price

        # Return the upload data back to the database
        product.save()

        # Redirect back to the product page with a success message
        messages.success(request, 'Product Updated successfully')
        return redirect('products')
    return render(request, 'update-product.html', {'product': product})


def auth_success(request):
    token = cl.access_token()
    return JsonResponse(token, safe=False)


@login_required()
def payment(request, id):
    # select the product being paid
    product = Products.objects.get(id=id)
    # check if the form being submitted has a post method
    if request.method == "POST":
        phone_number = request.POST.get('nambari')
        amount = request.POST.get('bei')
        amount = int(amount)
        # proceed with the payment by launching mpesa ST
        account_ref = 'JJIBRAH'
        transaction_description = 'Payment for a product'
        call_back_url = stk_push_callback_url
        stk = cl.stk_push(phone_number, amount, account_ref,
                          transaction_description, stk_push_callback_url)
        mpesa_response = stk.response_description
        messages.success(request, mpesa_response)
        return JsonResponse(mpesa_response, safe=False)
    return render(request, 'payment.html', {'product': product})

# password=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 (new)
