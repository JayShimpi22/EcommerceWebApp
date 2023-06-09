from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from myapp.models import *
import json,datetime
from math import ceil
from .utils import cookieData,cartData
# Create your views here.
def home(request):
    current_user = request.user
    # print(current_user)
    allProducts = []

    catProducts = Product.objects.values("category")
    cats = {item['category'] for item in catProducts}


    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)

        nSlides = n//4+ ceil((n/4)-(n//4))
        allProducts.append([prod,range(1,nSlides),nSlides])

    data = cartData(request)

    cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']

    context = {"allProds":allProducts,'cartItems':cartItems}
    return render(request,'index.html',context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'cart.html',context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'checkout.html',context)



def updateItem(request):
    data = json.loads(request.body)
    print(data)
    prodId = data['productId']
    action = data['action']

    user = request.user
    product = Product.objects.get(product_id=prodId)

    order,created = Order.objects.get_or_create(user=user,complete=False)

    orderitem,created = OrderItem.objects.get_or_create(order=order,product=product)

    
    if action=='add':
        orderitem.quantity = orderitem.quantity+1

    elif action=='remove':
        orderitem.quantity = orderitem.quantity-1
    
    orderitem.save()

    if orderitem.quantity<=0:
        orderitem.delete()
    

    return JsonResponse("Item Added",safe=False)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order,created = Order.objects.get_or_create(user=user,complete=False)
    
    else:
        print("Login First...")
        name = data['form']['name']
        email = data['form']['email']
        print("Data:",data)

        cartdata = cartData(request)
        items = cartdata['items']

        user,created = User.objects.get_or_create(name = email,email=email)
        user.save()

        order = Order.objects.create(
            user=user,
            complete=False,
        )

        for item in items:
            product = Product.objects.get(product_id = item['product']['product_id'])

            orderItem = OrderItem.objects.create(product=product,
                                                 order=order,
                                                 quantity=item['quantity']
                                                )
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total==float(order.get_cart_total):
        order.complete = True
    order.save()
        
    
    ShippingAddress.objects.create(
        user = user,
        order = order,
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        state = data['shipping']['state'],
        zip_code = data['shipping']['zipcode'],
    )
    return JsonResponse("Payment Complete",safe=False)
        

