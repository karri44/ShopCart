from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from products.models import Category,Product
CATEGORIES = [('Mobiles','mobiles','mobiles.png'),('Laptops','laptops','laptops.png'),('Televisions','tvs','tv.png'),('Air conditioners','acs','ac.png'),('Fashion','fashion','fashion.png')]
PRODUCTS = [
('iPhone 16','Apple','mobiles',69900,'iphone16.png',True,'An everyday companion for photos, conversations and entertainment. Explore the familiar iPhone experience in a compact design.'),
('Galaxy S25','Samsung','mobiles',74999,'samsungs25.png',True,'A versatile smartphone for your everyday apps, creativity and entertainment.'),
('OnePlus 10R','OnePlus','mobiles',29999,'oneplus10r.png',False,'A streamlined smartphone for staying connected, working on the go and unwinding.'),
('Redmi Note 15 Pro','Redmi','mobiles',24999,'redminot15pro.png',False,'A practical smartphone option for everyday browsing, photography and messaging.'),
('Realme 16 Pro','Realme','mobiles',27999,'realme16pro.png',False,'Bring your everyday essentials together with this featured smartphone.'),
('Galaxy S26 Ultra','Samsung','mobiles',129999,'samsungs26ultra.png',False,'A premium smartphone entry in the ShopCart demonstration catalogue.'),
('Pavilion Laptop','HP','laptops',54999,'hp.png',True,'From coursework to your next creative idea, a laptop for everyday productivity.'),
('Inspiron Laptop','Dell','laptops',58999,'dell.png',False,'A comfortable everyday workspace for studying, browsing and getting things done.'),
('IdeaPad Laptop','Lenovo','laptops',47999,'lenovo.png',False,'An everyday laptop for your notes, projects and favourite entertainment.'),
('Vivobook Laptop','ASUS','laptops',52999,'asusbook.png',True,'Make room for your ideas with a laptop built around everyday work and play.'),
('Gaming Laptop','ASUS','laptops',84999,'asusgaming.png',False,'Explore a performance-focused laptop from our gaming collection.'),
('Smart TV 42 inch','Samsung','tvs',28999,'samsung42inch.png',False,'Make your living room a place for movie nights and everyday entertainment.'),
('Smart TV 55 inch','Samsung','tvs',49999,'samsung55inch.png',False,'A larger screen for sharing your favourite entertainment at home.'),
('Smart Television','LG','tvs',42999,'lgsmart.png',True,'Settle in for a new series or a family movie night with this home entertainment pick.'),
('Bravia Television','Sony','tvs',64999,'sonybravia.png',False,'An entertainment centrepiece for your living space.'),
('Smart Television','Mi','tvs',26999,'mismart.png',False,'Everyday entertainment for your home, from the ShopCart TV collection.'),
('Smart Television','OnePlus','tvs',32999,'oneplustv.png',False,'A home entertainment option for all your favourite viewing moments.'),
('Split Air Conditioner','LG','acs',36999,'lgac.png',False,'Bring everyday comfort home. This sample listing does not include installation or a real delivery service.'),
('Split Air Conditioner','Daikin','acs',42999,'daikin.png',True,'A considered upgrade for a more comfortable room. Demo catalogue item; installation is not included.'),
('Split Air Conditioner','Voltas','acs',32999,'voltas.png',False,'A cooling option for your living space. Sample listing without installation.'),
('Split Air Conditioner','Samsung','acs',39999,'samsungac.png',False,'An addition to your home comfort setup. Demo listing; no installation service.'),
('Split Air Conditioner','Mitsubishi','acs',52999,'mitsubishi.png',False,'Explore the home comfort collection. Demo item without installation.'),
('Everyday T-shirt','ShopCart Studio','fashion',799,'tshirts.png',True,'An easygoing essential for your everyday wardrobe. Demo listing in one standard sample variant.'),
('Classic Denim Jeans','ShopCart Studio','fashion',1499,'jeans.png',False,'A timeless wardrobe staple. One sample variant is available in this demonstration store.'),
('Everyday Sneakers','ShopCart Studio','fashion',2299,'shoes.png',True,'A casual finishing touch to your everyday look. Demo catalogue item with one sample variant.'),
('Everyday Watch','ShopCart Studio','fashion',1999,'watchs.png',False,'A simple accessory for your everyday routine. One sample variant in the demo catalogue.')]
class Command(BaseCommand):
    help = 'Create missing demo catalogue items; preserves existing prices, stock and edits.'
    @transaction.atomic
    def handle(self,*args,**options):
        categories = {}
        for name,slug,image in CATEGORIES:
            categories[slug],_ = Category.objects.get_or_create(slug=slug,defaults={'name':name,'image':'images/'+image})
        created = 0
        for name,brand,category,price,image,featured,description in PRODUCTS:
            _,new = Product.objects.get_or_create(slug=slugify(brand+' '+name),defaults={'name':name,'brand':brand,'category':categories[category],'price':price,'image':'images/'+image,'featured':featured,'description':description,'stock':15})
            created += new
        self.stdout.write(self.style.SUCCESS(f'Catalogue ready: {created} products created.'))
