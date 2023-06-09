from .models import *
import json

def cookieData(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    # print("cart:",cart)

    items = [] 
    cartItems = 0  
    order = {'get_cart_total':0,'get_cart_items':0}

    for i in cart:
        try:
            cartItems+=cart[i]['quantity']
            product = Product.objects.get(product_id = i)
            total = product.price*cart[i]['quantity']
            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]['quantity']

            item = {
                'product':{
                    'product_id':product.product_id,
                    'product_name':product.product_name,
                    'price':product.price,
                    'image':product.image,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)
        except Exception as e:
            pass
        # print(items)
    return {'cartItems':cartItems,'order':order,'items':items}

def cartData(request):
    if request.user.is_authenticated:             
        print(request.user)
        user = request.user
        order,created = Order.objects.get_or_create(user=user,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieDt = cookieData(request)
        cartItems = cookieDt['cartItems']
        order = cookieDt['order']
        items = cookieDt['items']

    return {'cartItems':cartItems,'order':order,'items':items}