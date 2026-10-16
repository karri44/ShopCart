from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product, Category

def catalog_query(request):
    products = Product.objects.filter(active=True).select_related('category')
    q = request.GET.get('q','').strip()[:120]
    category = request.GET.get('category','')
    if q: products = products.filter(Q(name__icontains=q)|Q(brand__icontains=q)|Q(category__name__icontains=q))
    if category: products = products.filter(category__slug=category)
    sort = request.GET.get('sort','featured')
    products = products.order_by({'price_low':'price','price_high':'-price','name':'name'}.get(sort,'-featured'),'id')
    return products, q, category, sort

def home(request):
    return render(request,'home.html',{'categories':Category.objects.all(),'products':Product.objects.filter(active=True,featured=True)[:8]})
def catalog(request):
    products,q,category,sort = catalog_query(request)
    page = Paginator(products,12).get_page(request.GET.get('page'))
    params = request.GET.copy(); params.pop('page',None)
    return render(request,'catalog.html',{'page':page,'q':q,'selected_category':category,'sort':sort,'categories':Category.objects.all(),'params':params.urlencode()})
def detail(request,slug):
    product = get_object_or_404(Product,slug=slug,active=True)
    return render(request,'detail.html',{'product':product,'products':Product.objects.filter(category=product.category,active=True).exclude(pk=product.pk)[:4]})
def api_products(request):
    products,_,_,_ = catalog_query(request)
    page = Paginator(products,12).get_page(request.GET.get('page'))
    return JsonResponse({'count':page.paginator.count,'page':page.number,'pages':page.paginator.num_pages,'results':[{'id':p.id,'name':p.name,'slug':p.slug,'price':str(p.price),'category':p.category.name,'stock':p.stock} for p in page]})
