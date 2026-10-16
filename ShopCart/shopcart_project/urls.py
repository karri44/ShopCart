from django.contrib import admin
from django.urls import path,include
from products import views as products
from cart import views as cart
from orders import views as orders
urlpatterns = [path('admin/',admin.site.urls),path('',products.home,name='home'),path('products/',products.catalog,name='catalog'),path('products/<slug:slug>/',products.detail,name='product_detail'),path('api/products/',products.api_products,name='api_products'),path('cart/',cart.cart,name='cart'),path('cart/<int:pk>/',cart.change,name='cart_change'),path('checkout/',orders.checkout,name='checkout'),path('orders/',orders.history,name='orders'),path('orders/<uuid:reference>/',orders.detail,name='order_detail'),path('accounts/',include('users.urls'))]
