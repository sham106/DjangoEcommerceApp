from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages, auth
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
import datetime
from .models import Customer
from . forms import CreateUserForm, LoginUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import DetailView

# Create your views here.


def HomeView(request):
    products = Product.objects.all()[:4]
    products2 = Product.objects.all()[3:6]
    context = {"products": products, "products2": products2, }
    return render(request, "main.html", context)


def registerpage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            Customer.objects.create(
                user=user,
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            Customer.save

            user = form.cleaned_data.get('username')
            messages.success(
                request, 'Account was successfully created for ' + user)
            return redirect('store:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            customer = request.user.customer
            return redirect('store:home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutuser(request):
    auth.logout(request)
    return redirect('login')


def why_us(request):
    context = {}
    return render(request, 'why.html')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'



def about(request):
    context = {}
    return render(request, 'about.html')


def product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
        cartitems = cart.cartitems_set.all()
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products, 'cart':cart})



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
        cartitems = cart.cartitems_set.all()
    else:
        cartitems = []
        cart = {"get_cart_total": 0, "get_itemtotal": 0}


    return render(request, 'cart.html', {'cartitems' : cartitems, 'cart':cart})

    


def checkout(request):
    return render(request, 'checkout.html', {})

def updateCart(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    product = Product.objects.get(id=productId)
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
    cartitem, created = Cartitems.objects.get_or_create(cart = cart, product = product)

    if action == 'add':
	    cartitem.quantity = (cartitem.quantity + 1)
    elif action == 'remove':
        cartitem.quantity = (cartitem.quantity - 1)
    

    cartitem.save()

    if cartitem.quantity <= 0:

        cartitem.delete()

    return JsonResponse("Cart Updated", safe = False)

def updateQuantity(request):
    data = json.loads(request.body)
    quantityFieldValue = data['qfv']
    quantityFieldProduct = data['qfp']
    product = Cartitems.objects.filter(product__name = quantityFieldProduct).last()
    product.quantity = quantityFieldValue
    product.save()
    return JsonResponse("Quantity updated", safe = False)
   

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    else:
        print('user is not logged in')
    return JsonResponse('payment complete', safe=False)
