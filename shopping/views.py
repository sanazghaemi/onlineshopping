from django.shortcuts import render
from .models import Product,Feature,Review,CheckoutDetail,Order,OrderItem
from account.models import UserProfile
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .utils import cartData
import json
from django.http import JsonResponse
import datetime
# Create your views here.

def index(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    products=Product.objects.all()
    return render (request,'shopping/index.html',{'products':products,'cartItems':cartItems})

@ login_required
def product_view(request, myid):
    product = Product.objects.filter(id=myid).first()
    feature = Feature.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    if request.method=="POST":
        content = request.POST['content']
        review = Review(customer=request.user.userprofile, content=content, product=product)
        review.save()
        return redirect(f"/product_view/{product.id}")
    return render(request, "shopping/product_view.html", {'product':product,'cartItems':cartItems,'feature':feature, 'reviews':reviews})

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
 
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
 
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
 
            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]
 
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)
        except:
            pass
    return render(request, "shopping/cart.html", {'items':items, 'order':order, 'cartItems':cartItems})

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    total = order.get_cart_total
    if request.method == "POST":
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        phone_number = request.POST['phone_number']
        shipping_adress = CheckoutDetail.objects.create(address=address, city=city, phone_number=phone_number, state=state, zipcode=zipcode, customer=request.user.userprofile, total_amount=total, order=order)
        shipping_adress.save()
        transaction_id = datetime.datetime.now().timestamp()
        if total == order.get_cart_total:
            order.complete = True
        order.transaction_id=transaction_id
        order.save()  
        alert = True
        return render(request, "shopping/checkout.html", {'alert':alert})
    return render(request, "shopping/checkout.html", {'items':items, 'order':order, 'cartItems':cartItems})

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.userprofile
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)