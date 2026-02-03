from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import CartItem
from products.models import Product

@login_required(login_url='login')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)

@login_required(login_url='login')
@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = get_object_or_404(Product, id=product_id)
    
    if product.stock < quantity:
        return JsonResponse({'success': False, 'message': 'Insufficient stock'})
    
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    
    return JsonResponse({'success': True, 'message': 'Added to cart'})

@login_required(login_url='login')
@require_POST
def update_cart(request):
    cart_item_id = request.POST.get('cart_item_id')
    quantity = int(request.POST.get('quantity'))
    
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    
    if quantity <= 0:
        cart_item.delete()
    else:
        if cart_item.product.stock < quantity:
            return JsonResponse({'success': False, 'message': 'Insufficient stock'})
        
        cart_item.quantity = quantity
        cart_item.save()
    
    return JsonResponse({'success': True})

@login_required(login_url='login')
@require_POST
def remove_from_cart(request):
    cart_item_id = request.POST.get('cart_item_id')
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    
    return JsonResponse({'success': True})

@login_required(login_url='login')
def get_cart_count(request):
    count = CartItem.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})