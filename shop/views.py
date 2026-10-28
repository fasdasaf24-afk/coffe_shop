from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Location, Review
from .forms import OrderForm, SupportForm, ReviewForm

def home(request):
    return render(request, 'shop/home.html')

def all_menu(request, category_slug=None):
    if category_slug:
        products = Product.objects.filter(category=category_slug)
    else:
        products = Product.objects.all()
    return render(request, 'shop/menu.html', {'products': products, 'current_category': category_slug})

def new_items(request):
    products = Product.objects.filter(is_new=True)
    return render(request, 'shop/new.html', {'products': products})

# ИСПРАВЛЕНИЕ: Защита от спама в отзывах
def locations(request):
    locs = Location.objects.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            location_id = request.POST.get('location_id')
            # Проверка, не оставлял ли этот пользователь отзыв этой локации в текущей сессии
            session_key = f'reviewed_{location_id}'
            if request.session.get(session_key):
                messages.error(request, "Вы уже оставляли отзыв этой локации недавно.")
            else:
                review = form.save(commit=False)
                if location_id:
                    review.location_id = location_id
                    review.save()
                    request.session[session_key] = True # Запоминаем в сессии
                    messages.success(request, "Спасибо! Отзыв опубликован.")
            return redirect('locations')
    else:
        form = ReviewForm()
    return render(request, 'shop/locations.html', {'locations': locs, 'form': form})

# ИСПРАВЛЕНИЕ: Защита от пустой корзины и N+1 запросов
def delivery(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    if cart:
        products = Product.objects.in_bulk(cart.keys())
        for product_id, quantity in cart.items():
            product = products.get(int(product_id))
            if product:
                item_total = product.price * quantity
                total_price += item_total
                cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})

    if request.method == 'POST':
        if not cart_items:
            messages.error(request, "Ваша корзина пуста.")
            return redirect('delivery')

        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            summary = ", ".join([f"{item['product'].name} x{item['quantity']}" for item in cart_items])
            order.items_summary = summary
            order.save()
            request.session['cart'] = {}
            messages.success(request, "Заказ принят!")
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'shop/delivery.html', {
        'form': form, 'support_phone': settings.SUPPORT_PHONE, 'cart_items': cart_items, 'total_price': total_price
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'menu'))

def decrease_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]
        request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'menu'))

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    if cart:
        products = Product.objects.in_bulk(cart.keys())
        for product_id, quantity in cart.items():
            product = products.get(int(product_id))
            if product:
                item_total = product.price * quantity
                total_price += item_total
                cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def send_support_message(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
