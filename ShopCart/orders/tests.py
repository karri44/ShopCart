import uuid
from decimal import Decimal
from django.test import TestCase,Client
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Category,Product
from .models import Order
class ShoppingFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('buyer','buyer@example.com','SafePassword!427')
        self.category = Category.objects.create(name='Mobiles',slug='mobiles',image='images/mobiles.png')
        self.product = Product.objects.create(name='Test Phone',brand='Test',slug='test-phone',category=self.category,price='1000',stock=3,image='images/iphone16.png')
    def add(self,quantity=1):
        return self.client.post(reverse('cart_change',args=[self.product.pk]),{'quantity':quantity,'price':'1'})
    def data(self):
        self.client.get(reverse('checkout'))
        return {'full_name':'Test Buyer','email':'buyer@example.com','phone':'9876543210','address':'123 Sample Street','city':'Hyderabad','postcode':'500072','checkout_token':self.client.session['checkout_token']}
    def test_pages_search_and_api(self):
        for url in ['/', '/products/','/products/test-phone/','/cart/','/accounts/login/','/accounts/signup/']:
            self.assertEqual(self.client.get(url).status_code,200,url)
        self.assertContains(self.client.get('/products/?q=phone'),'Test Phone')
        self.assertContains(self.client.get('/products/?q=missing'),'No matches')
        self.assertEqual(self.client.get('/api/products/').json()['results'][0]['price'],'1000.00')
    def test_cart_mutations_and_price_tampering(self):
        self.assertEqual(self.client.get(reverse('cart_change',args=[self.product.pk])).status_code,405)
        self.add(2)
        self.assertEqual(self.client.session['cart'][str(self.product.pk)],2)
        self.assertContains(self.client.get('/cart/'),'2,000')
        self.add(10)
        self.assertEqual(self.client.session['cart'][str(self.product.pk)],2)
        self.client.post(reverse('cart_change',args=[self.product.pk]),{'action':'remove'})
        self.assertEqual(self.client.session['cart'],{})
    def test_checkout_login_required(self):
        self.add(); self.assertEqual(self.client.get('/checkout/').status_code,302)
    def test_order_persists_decrements_stock_and_is_private(self):
        self.add(2); self.client.force_login(self.user)
        data=self.data(); response=self.client.post('/checkout/',data)
        order=Order.objects.get()
        self.assertRedirects(response,reverse('order_detail',args=[order.reference]))
        self.assertEqual(order.total,Decimal('2000'))
        self.assertEqual(order.items.get().quantity,2)
        self.product.refresh_from_db(); self.assertEqual(self.product.stock,1)
        self.assertEqual(self.client.session['cart'],{})
        self.client.post('/checkout/',data); self.assertEqual(Order.objects.count(),1)
        self.assertContains(self.client.get('/orders/'),'Order #')
        other=User.objects.create_user('other',password='SafePassword!918')
        self.client.force_login(other)
        self.assertEqual(self.client.get(reverse('order_detail',args=[order.reference])).status_code,404)
    def test_stock_change_rolls_back_entire_order(self):
        second=Product.objects.create(name='Second',slug='second',category=self.category,price=200,stock=2)
        self.add(2)
        self.client.post(reverse('cart_change',args=[second.pk]),{'quantity':2})
        self.client.force_login(self.user); data=self.data()
        second.stock=0; second.save()
        response=self.client.post('/checkout/',data)
        self.assertContains(response,'insufficient stock')
        self.assertFalse(Order.objects.exists())
        self.product.refresh_from_db(); self.assertEqual(self.product.stock,3)
    def test_bad_address_and_invalid_token(self):
        self.add(); self.client.force_login(self.user); data=self.data()
        data['postcode']='123'; self.assertContains(self.client.post('/checkout/',data),'6-digit PIN')
        data['postcode']='500072'; data['checkout_token']=str(uuid.uuid4())
        self.assertContains(self.client.post('/checkout/',data),'expired')
        self.assertFalse(Order.objects.exists())
    def test_csrf_required(self):
        client=Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(reverse('cart_change',args=[self.product.pk]),{'quantity':1}).status_code,403)
    def test_registration_password_hashing_login_and_logout(self):
        self.add()
        response=self.client.post('/accounts/signup/',{'first_name':'Demo','username':'newbuyer','email':'new@example.com','password1':'SecureNew!422','password2':'SecureNew!422'})
        self.assertEqual(response.status_code,302)
        user=User.objects.get(username='newbuyer')
        self.assertNotEqual(user.password,'SecureNew!422'); self.assertTrue(user.check_password('SecureNew!422'))
        self.assertEqual(self.client.session['cart'][str(self.product.pk)],1)
        self.assertEqual(self.client.get('/accounts/logout/').status_code,405)
        self.client.post('/accounts/logout/')
        self.assertNotIn('_auth_user_id',self.client.session)
        self.assertTrue(self.client.login(username='newbuyer',password='SecureNew!422'))
    def test_out_of_stock_and_negative_quantity(self):
        self.add(-1); self.assertNotIn(str(self.product.pk),self.client.session.get('cart',{}))
        self.product.stock=0; self.product.save(); self.add()
        self.assertNotIn(str(self.product.pk),self.client.session.get('cart',{}))
    def test_order_price_snapshot_survives_catalog_edit(self):
        self.add(); self.client.force_login(self.user); self.client.post('/checkout/',self.data())
        self.product.price=2000; self.product.save()
        self.assertEqual(Order.objects.get().items.get().price,Decimal('1000'))
