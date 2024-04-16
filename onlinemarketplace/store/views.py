from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import OrderForm
# Create your views here.


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('index')

def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action in ['increase', 'decrease']:
        quantity = 1 if action == 'increase' else -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)

    return redirect('cart_view')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request,'store/cart_view.html',{
        'cart': cart
    })

@login_required
def checkout(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            total_price = 0
            
            for item in cart:
                total_price += item['product'].price * item['quantity']
            
            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()
            
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                price = product.price * quantity
                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            
            cart.clear()
            return redirect('account_detail')
    else:
        form = OrderForm()
 
    return render(request,'store/checkout.html',{
        'cart': cart,
        'form': form,
    })

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'store/search.html',{
        'query': query,
        'products': products
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()

    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'store/product_detail.html',{
        'product': product
    })