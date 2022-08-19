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
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cat_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'product.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cat_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cat_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'items': items, 'order': order}
    context = {}
    return render(request, 'checkout.html')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('item added successfully', safe=False)


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
