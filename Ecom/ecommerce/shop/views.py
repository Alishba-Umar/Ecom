from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Category, Product
from .forms import CategoryForm, ProductForm
from decimal import Decimal


def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'shop/admin_dashboard.html', {'categories': categories, 'products': products})

@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CategoryForm()
    return render(request, 'shop/add_category.html', {'form': form})

@user_passes_test(is_admin)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'shop/edit_category.html', {'form': form})

@user_passes_test(is_admin)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_dashboard')
    return render(request, 'shop/delete_category.html', {'category': category})

@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

@user_passes_test(is_admin)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_dashboard')
    return render(request, 'shop/delete_product.html', {'product': product})



def index(request):
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {'categories': categories})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category_products.html', {'category': category, 'products': products})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {
                'name': product.name,
                'price': str(product.price),  # Convert to string for JSON serialization
                'quantity': quantity
            }
        request.session['cart'] = cart
        return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    for product_id, product in cart.items():
        product['price'] = Decimal(product['price'])  # Convert back to Decimal
        product['total_price'] = product['price'] * product['quantity']
    return render(request, 'shop/view_cart.html', {'cart': cart})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')