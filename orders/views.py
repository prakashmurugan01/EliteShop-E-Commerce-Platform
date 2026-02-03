from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem, Coupon
from .forms import CheckoutForm
from cart.models import CartItem
from accounts.models import Address
import random

@login_required(login_url='login')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        return redirect('view_cart')
    
    addresses = Address.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'addresses': addresses,
        'total_price': total_price,
    }
    return render(request, 'orders/checkout.html', context)

@login_required(login_url='login')
@require_POST
def apply_coupon(request):
    coupon_code = request.POST.get('coupon_code')
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    
    try:
        coupon = Coupon.objects.get(
            code=coupon_code,
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_to__gte=timezone.now()
        )
        discount = (total_price * coupon.discount_percent) / 100
        final_total = total_price - discount
        
        return JsonResponse({
            'success': True,
            'discount': float(discount),
            'final_total': float(final_total),
            'coupon_code': coupon_code
        })
    except Coupon.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid coupon'})

@login_required(login_url='login')
@require_POST
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        return JsonResponse({'success': False, 'message': 'Cart is empty'})
    
    address_id = request.POST.get('address_id')
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    # Calculate total
    total_amount = sum(item.total_price for item in cart_items)
    
    # Apply coupon if exists
    coupon_code = request.POST.get('coupon_code')
    discount_amount = 0
    
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            discount_amount = (total_amount * coupon.discount_percent) / 100
            total_amount -= discount_amount
        except Coupon.DoesNotExist:
            pass
    
    # Create order
    order_number = f"ORD{random.randint(100000, 999999)}"
    
    order = Order.objects.create(
        user=request.user,
        order_number=order_number,
        address=address,
        total_amount=total_amount,
        discount_amount=discount_amount,
        coupon_code=coupon_code,
        estimated_delivery=timezone.now().date() + timedelta(days=4)
    )
    
    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.current_price,
            total=item.total_price
        )
        
        # Update stock
        item.product.stock -= item.quantity
        item.product.save()
    
    # Clear cart
    cart_items.delete()
    
    return JsonResponse({
        'success': True,
        'order_number': order_number,
        'redirect_url': f'/orders/order-confirmation/{order.id}/'
    })

@login_required(login_url='login')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {'order': order}
    return render(request, 'orders/order_confirmation.html', context)

@login_required(login_url='login')
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    
    context = {'orders': orders}
    return render(request, 'orders/order_list.html', context)

@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'orders/order_detail.html', context)