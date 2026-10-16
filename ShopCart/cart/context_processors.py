from .services import get_cart
def cart_count(request):
    items,_ = get_cart(request)
    return {'cart_count':sum(i['quantity'] for i in items)}
