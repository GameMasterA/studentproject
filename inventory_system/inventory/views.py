from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ItemForm
from .models import Item


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'inventory/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    items = Item.objects.order_by('-updated_at')[:5]
    total_items = Item.objects.count()
    total_quantity = sum((item.quantity for item in Item.objects.all()), 0)
    total_value = sum((item.price * item.quantity for item in Item.objects.all()), Decimal('0.00'))
    low_stock_count = Item.objects.filter(quantity__lte=F('low_stock_threshold')).count()

    context = {
        'items': items,
        'total_items': total_items,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'inventory/dashboard.html', context)


@login_required
def stock_view(request):
    query = request.GET.get('q', '').strip()
    items = Item.objects.all().order_by('name')

    if query:
        items = items.filter(name__icontains=query) | items.filter(sku__icontains=query)

    context = {'items': items, 'query': query}
    return render(request, 'inventory/stock.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'{item.name} was added to inventory.')
            return redirect('stock')
    else:
        form = ItemForm()

    return render(request, 'inventory/add_product.html', {'form': form, 'editing': False})


@login_required
def edit_product(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'{item.name} was updated successfully.')
            return redirect('stock')
    else:
        form = ItemForm(instance=item)

    return render(request, 'inventory/add_product.html', {'form': form, 'editing': True, 'item': item})


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item_name = item.name
    item.delete()
    messages.success(request, f'{item_name} was removed from inventory.')
    return redirect('stock')