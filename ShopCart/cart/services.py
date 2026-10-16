from decimal import Decimal
from products.models import Product

def get_cart(request):
    raw = request.session.get('cart',{})
    if not isinstance(raw,dict): raw = {}
    products = Product.objects.filter(pk__in=[int(k) for k in raw if str(k).isdigit()],active=True)
    items = []
    for product in products:
        try: quantity = max(1,min(int(raw[str(product.pk)]),99))
        except (ValueError,TypeError): continue
        items.append({'product':product,'quantity':quantity,'subtotal':product.price*quantity})
    return items, sum((i['subtotal'] for i in items),Decimal('0.00'))
