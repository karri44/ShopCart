from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .services import get_cart

def cart(request):
    items,total = get_cart(request)
    return render(request,'cart.html',{'items':items,'total':total})
@require_POST
def change(request,pk):
    product = get_object_or_404(Product,pk=pk,active=True)
    cart = request.session.get('cart',{})
    if not isinstance(cart,dict): cart = {}
    action = request.POST.get('action','add')
    try: quantity = int(request.POST.get('quantity',1))
    except (ValueError,TypeError):
        messages.error(request,'Enter a whole-number quantity.'); return redirect('cart')
    if action == 'remove': cart.pop(str(pk),None)
    else:
        quantity = quantity + int(cart.get(str(pk),0)) if action == 'add' else quantity
        if quantity < 1 or quantity > min(product.stock,99):
            messages.error(request,f'Choose between 1 and {min(product.stock,99)} available items.'); return redirect('cart')
        cart[str(pk)] = quantity
        messages.success(request,'Your bag has been updated.')
    request.session['cart'] = cart
    return redirect('checkout' if request.POST.get('buy_now') else 'cart')
