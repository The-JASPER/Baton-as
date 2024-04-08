from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order
from .forms import OrderForm
from django.contrib.auth.models import User

def index(request):
    products = Product.objects.all()
    return render(request, 'batcore/index.html', {'products': products})

def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)  
        if form.is_valid():
          
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            return redirect('order_confirmation')  
        form = OrderForm() 

    return render(request, 'batcore/checkout.html', {'form': form})  

def order_confirmation(request):
    return render(request, 'batcore/order_confirmation.html')

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create()
    CartItem.objects.create(cart=cart, product=product)
    return redirect('index')

def remove_from_cart(request, cart_item_id):
    CartItem.objects.get(pk=cart_item_id).delete()
    return redirect('view_cart')

def view_cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            return redirect('order_confirmation')
    else:
        form = OrderForm()
    return render(request, 'batcore/place_order.html', {'form': form})