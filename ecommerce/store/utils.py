import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print("Cart:", cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            # Iterăm prin elementele coșului de cumpărături și calculăm totalul și numărul de produse
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total                
            order['get_cart_items'] += cart[i]["quantity"]

            # Creăm un dicționar pentru fiecare element din coș pentru a-l adăuga la lista de elemente
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)

            if not product.digital:
                order['shipping'] = True
        except:
            pass
    
    # Returnăm un dicționar care conține informații despre coșul de cumpărături
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        # Dacă utilizatorul este autentificat, obținem informațiile despre coș din baza de date
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Dacă utilizatorul nu este autentificat, folosim funcția cookieCart() pentru a obține informațiile
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    # Returnăm un dicționar care conține informații despre coș și comanda asociată
    return {'order': order, 'items': items, 'cartItems': cartItems }

def guestOrder(request, data):
    print("User is not logged in...")
    print('COOKIES:', request.COOKIES)
    
    name = data['form']['name']
    email = data['form']['email']
    
    # Folosim funcția cookieCart() pentru a obține informațiile despre coș
    cookieData = cookieCart(request)
    items = cookieData['items']

    # Creăm sau obținem un obiect Customer asociat cu adresa de e-mail furnizată
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    # Creăm un obiect Order asociat cu clientul
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    # Iterăm prin elementele din coș și creăm obiecte OrderItem asociate cu produsele
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    
    # Returnăm obiectele Customer și Order pentru a le utiliza în continuare
    return customer, order
