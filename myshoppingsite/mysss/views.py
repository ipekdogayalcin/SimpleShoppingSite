import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ProductForm, PurchaseForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Purchase, Customer
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    return redirect('logout')

@login_required
@transaction.atomic
def update_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.item_type = request.POST.get('item_type')
        product.color = request.POST.get('color')
        product.material = request.POST.get('material')
        product.stock = request.POST.get('stock')
        product.price = request.POST.get('price')
        try:
            product.save()
            return JsonResponse({'success': True, 'message': 'Product updated successfully', 'product': product.serialize()})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method Not Allowed'}, status=405)


@login_required
@transaction.atomic
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        item_type = request.POST.get('item_type')
        color = request.POST.get('color')
        material = request.POST.get('material')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        product.item_type = item_type
        product.color = color
        product.material = material
        product.stock = stock
        product.price = price
        try:
            product.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'product_details.html', {'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('shop')

def register_view(request):
    authenticated = request.user.is_authenticated
    message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            message = "Username is already taken. Please choose a different one."
        else:
            if not re.match("^[a-zA-Z0-9_]+$", username):
                message = "Invalid username format. Use only letters, numbers, and underscores."
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect("shop")
    return render(request, "register.html", {"message": message, 'authenticated': authenticated})

def login_view(request):
    authenticated = False
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("shop")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "login.html", {'authenticated': authenticated})

@login_required
def shop(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({
                'image_url': product.image_url,
                'material': product.material,
                'color': product.color,
                'item_type': product.item_type,
                'price': product.price,
            })
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = ProductForm()
        products = Product.objects.filter(user=request.user)
        context = {'form': form, 'products': products}
        return render(request, 'shop.html', context)


@login_required
@transaction.atomic
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer, created = Customer.objects.get_or_create(user=request.user)


    if product in customer.cart.all():

        product = customer.cart.get(id=product.id)
        product.quantity += 1
    else:

        product.quantity = 1
        customer.cart.add(product)

    product.save()
    messages.success(request, f'{product.name} added to cart!')
    return redirect('shop')


@login_required
@transaction.atomic
def remove_from_cart_view(request, product_id):
    product = Product.objects.get(id=product_id)
    request.user.customer.cart.remove(product)
    return redirect('my_cart')


@login_required
def my_cart_view(request):
    try:
        cart_products = request.user.customer.cart.all()
        total_price = sum(product.price * product.quantity for product in cart_products)
    except ObjectDoesNotExist:
        cart_products = []
        total_price = 0

    context = {
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'my_cart.html', context)


@login_required
@transaction.atomic
def purchases_view(request):
    try:
        customer = request.user.customer
        if request.method == 'POST':
            form = PurchaseForm(request.POST, user=request.user)
            if form.is_valid():
                shipping_address = form.cleaned_data['shipping_address']
                card_credentials = form.cleaned_data['card_credentials']
                expiry_month = form.cleaned_data['expiry_month']
                expiry_year = form.cleaned_data['expiry_year']
                cvc = form.cleaned_data['cvc']
                product_ids = request.POST.getlist('products')

                total_price = 0
                out_of_stock_products = []
                for product_id in product_ids:
                    product = get_object_or_404(Product, id=product_id)
                    total_price += product.price * product.quantity
                    if product.stock < product.quantity:
                        out_of_stock_products.append(product.name)

                if out_of_stock_products:
                    messages.error(request, f'Sorry, the following item(s) in your cart does not have enough stock: {", ".join(out_of_stock_products)}. Purchase failed.')
                    return redirect('my_cart')

                for product_id in product_ids:
                    product = get_object_or_404(Product, id=product_id)
                    product.stock -= product.quantity
                    product.save()

                purchase = Purchase.objects.create(
                    customer=customer,
                    shipping_address=shipping_address,
                    card_credentials=card_credentials,
                    expiry_month=expiry_month,
                    expiry_year=expiry_year,
                    cvc=cvc,
                    total_price=total_price,
                )
                purchase.products.add(*product_ids)

                request.user.customer.cart.clear()

                messages.success(request, 'Purchase successful!')
                return redirect('purchases')

            else:
                messages.error(request, 'Invalid form data. Please check your input.')

        else:
            form = PurchaseForm(user=request.user)
    except ObjectDoesNotExist:
        customer = None
        form = None

    purchases = Purchase.objects.filter(customer=customer).order_by('-purchase_date')
    context = {'form': form, 'purchases': purchases, 'customer': customer}
    return render(request, 'purchases.html', context)
