import uuid
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction,IntegrityError
from django.db.models import F
from products.models import Product
from cart.services import get_cart
from .forms import CheckoutForm
from .models import Order,OrderItem

@login_required
def checkout(request):
    items,total = get_cart(request)
    if not items:
        messages.info(request,'Add something to your bag before checkout.'); return redirect('catalog')
    token = request.session.setdefault('checkout_token',str(uuid.uuid4()))
    form = CheckoutForm(request.POST or None,initial={'full_name':request.user.get_full_name(),'email':request.user.email,'checkout_token':token})
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        if str(data['checkout_token']) != token:
            form.add_error(None,'This checkout has expired. Refresh the page and try again.')
        else:
            try:
                with transaction.atomic():
                    existing = Order.objects.filter(checkout_token=data['checkout_token'],user=request.user).first()
                    if existing: return redirect('order_detail',reference=existing.reference)
                    # Conditional stock updates prevent overselling, including on SQLite.
                    for item in items:
                        changed = Product.objects.filter(pk=item['product'].pk,active=True,price=item['product'].price,stock__gte=item['quantity']).update(stock=F('stock')-item['quantity'])
                        if not changed: raise ValueError(f"{item['product'].name} changed or has insufficient stock. Review your bag.")
                    order = Order.objects.create(user=request.user,total=total,**data)
                    OrderItem.objects.bulk_create([OrderItem(order=order,product=i['product'],name=i['product'].name,price=i['product'].price,quantity=i['quantity']) for i in items])
                request.session['cart'] = {}
                request.session.pop('checkout_token',None)
                messages.success(request,'Order placed! You can follow its progress here.')
                return redirect('order_detail',reference=order.reference)
            except ValueError as exc: form.add_error(None,str(exc))
            except IntegrityError: form.add_error(None,'This order may already have been submitted. Check My orders before trying again.')
    return render(request,'checkout.html',{'form':form,'items':items,'total':total})
@login_required
def history(request):
    return render(request,'orders.html',{'orders':Order.objects.filter(user=request.user)})
@login_required
def detail(request,reference):
    order = get_object_or_404(Order.objects.prefetch_related('items'),reference=reference,user=request.user)
    return render(request,'order_detail.html',{'order':order})
