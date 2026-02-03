from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from products.models import Product, Category
from orders.models import Order, OrderItem, Coupon
from delivery.models import DeliveryTracking, DeliveryStatusUpdate

def is_admin(user):
    return user.is_staff and user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    pending_orders = Order.objects.filter(status='PLACED').count()
    recent_orders = Order.objects.all()[:10]
    
    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'adminpanel/dashboard.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def manage_products(request):
    products = Product.objects.all()
    
    context = {'products': products}
    return render(request, 'adminpanel/products.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def add_product(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        product = Product.objects.create(
            category_id=request.POST.get('category'),
            name=request.POST.get('name'),
            slug=request.POST.get('name').lower().replace(' ', '-'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            discount_price=request.POST.get('discount_price') or None,
            stock=request.POST.get('stock'),
            image=request.FILES.get('image'),
            is_trending=request.POST.get('is_trending', False)
        )
        return redirect('manage_products')
    
    context = {'categories': categories}
    return render(request, 'adminpanel/add_product.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        product.category_id = request.POST.get('category')
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.discount_price = request.POST.get('discount_price') or None
        product.stock = request.POST.get('stock')
        product.is_trending = request.POST.get('is_trending', False)
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        
        product.save()
        return redirect('manage_products')
    
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'adminpanel/edit_product.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
@require_POST
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return JsonResponse({'success': True})

@login_required(login_url='login')
@user_passes_test(is_admin)
def manage_categories(request):
    categories = Category.objects.all()
    
    context = {'categories': categories}
    return render(request, 'adminpanel/categories.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        Category.objects.create(
            name=request.POST.get('name'),
            slug=request.POST.get('name').lower().replace(' ', '-'),
            description=request.POST.get('description'),
            icon=request.POST.get('icon', 'fas fa-box')
        )
        return redirect('manage_categories')
    
    return render(request, 'adminpanel/add_category.html')

@login_required(login_url='login')
@user_passes_test(is_admin)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.icon = request.POST.get('icon')
        category.save()
        return redirect('manage_categories')
    
    context = {'category': category}
    return render(request, 'adminpanel/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
@require_POST
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return JsonResponse({'success': True})

@login_required(login_url='login')
@user_passes_test(is_admin)
def manage_orders(request):
    orders = Order.objects.all().select_related('user', 'address')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'statuses': Order.STATUS_CHOICES,
    }
    return render(request, 'adminpanel/orders.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        
        # Create delivery tracking if not exists
        if not hasattr(order, 'tracking'):
            DeliveryTracking.objects.create(order=order)
        
        # Add status update to tracking
        DeliveryStatusUpdate.objects.create(
            tracking=order.tracking,
            status=new_status,
            location=request.POST.get('location', ''),
            notes=request.POST.get('notes', '')
        )
        
        return redirect('manage_orders')
    
    context = {
        'order': order,
        'order_items': order_items,
        'statuses': Order.STATUS_CHOICES,
    }
    return render(request, 'adminpanel/order_update.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
@require_POST
def update_order_status(request):
    order_id = request.POST.get('order_id')
    new_status = request.POST.get('status')
    location = request.POST.get('location', '')
    notes = request.POST.get('notes', '')
    
    order = get_object_or_404(Order, id=order_id)
    order.status = new_status
    order.save()
    
    # Create or update tracking
    tracking, created = DeliveryTracking.objects.get_or_create(order=order)
    tracking.current_location = location
    tracking.notes = notes
    tracking.save()
    
    # Add status update
    DeliveryStatusUpdate.objects.create(
        tracking=tracking,
        status=new_status,
        location=location,
        notes=notes
    )
    
    return JsonResponse({'success': True})

@login_required(login_url='login')
@user_passes_test(is_admin)
def manage_coupons(request):
    coupons = Coupon.objects.all()
    
    context = {'coupons': coupons}
    return render(request, 'adminpanel/coupons.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def add_coupon(request):
    if request.method == 'POST':
        Coupon.objects.create(
            code=request.POST.get('code').upper(),
            discount_percent=request.POST.get('discount_percent'),
            valid_from=request.POST.get('valid_from'),
            valid_to=request.POST.get('valid_to'),
            is_active=request.POST.get('is_active', True)
        )
        return redirect('manage_coupons')
    
    return render(request, 'adminpanel/add_coupon.html')

@login_required(login_url='login')
@user_passes_test(is_admin)
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    
    if request.method == 'POST':
        coupon.code = request.POST.get('code').upper()
        coupon.discount_percent = request.POST.get('discount_percent')
        coupon.valid_from = request.POST.get('valid_from')
        coupon.valid_to = request.POST.get('valid_to')
        coupon.is_active = request.POST.get('is_active', False)
        coupon.save()
        return redirect('manage_coupons')
    
    context = {'coupon': coupon}
    return render(request, 'adminpanel/edit_coupon.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
@require_POST
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    coupon.delete()
    return JsonResponse({'success': True})
