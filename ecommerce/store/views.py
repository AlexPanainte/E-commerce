from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .utils import cartData, guestOrder

import json
import datetime

def store(request):
    # Obținem informațiile despre coș și produsele disponibile
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    # Obținem informațiile despre coș, comanda și elementele din coș
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'order': order, 'items': items, 'cartItems': cartItems }
    return render(request, 'store/cart.html', context)

def checkout(request):
    # Obținem informațiile despre coș, comanda și elementele din coș
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'order': order, 'items': items, 'cartItems': cartItems }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    # Actualizăm cantitatea unui produs în coș
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print("Action", action)
    print("productId", productId)

    customer = request.user.customer
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

    return JsonResponse("Item was added", safe=False)

def processOrder(request):
    # Procesăm o comandă (creare comandă, actualizare stării comenzii, etc.)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        # Dacă utilizatorul este autentificat, folosim comanda existentă sau creăm una nouă
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        # Dacă utilizatorul nu este autentificat, creăm o comandă pentru un utilizator oaspete
        customer, order = guestOrder(request, data)

    # Setăm ID-ul tranzacției și actualizăm starea comenzii
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    # Dacă există informații de livrare, le salvăm în baza de date
    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            county=data['shipping']['county'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse("Payment complete!", safe=False)
