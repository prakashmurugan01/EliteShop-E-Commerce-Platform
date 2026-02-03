from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category

def home(request):
    categories = Category.objects.all()
    trending_products = Product.objects.filter(is_trending=True)[:6]
    featured_products = Product.objects.all()[:8]
    
    context = {
        'categories': categories,
        'trending_products': trending_products,
        'featured_products': featured_products,
    }
    return render(request, 'home.html', context)

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Filtering
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Searching
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

def search_suggestions(request):
    import json
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:5]
    
    suggestions = [
        {'id': p.id, 'name': p.name, 'slug': p.slug} 
        for p in products
    ]
    
    return JsonResponse(suggestions, safe=False)