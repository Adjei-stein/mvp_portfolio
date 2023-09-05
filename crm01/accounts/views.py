from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import Group
import json
import datetime
from .models import *
from . utils import cookieCart, cartData, guestOrder
from .forms import ProdForm, CreateUserForm, CustomerForm
from .filters import *

# Create your views here.

def login(request):

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)

		if user is not None:
			auth_login(request, user)

			return redirect('home')

		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render (request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def register(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)

		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')

			group = Group.objects.get(name='Customer')
			user.groups.add(group)
			Customer.objects.create(
				user=user, name=username, email=email,
				)

			messages.success(request, 'Account was created for ' + username)



			return redirect('login')



	context = {'form':form}
	return render (request, 'accounts/register.html', context)

def profile_settings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save

	context = {'form':form}
	return render (request, 'accounts/profile_settings.html', context)

def home(request):
	data = cartData(request)
	cartItems = data['cartItems']
	items = data['items']
	order = data['order']
	products = Product.objects.all()
	filt = ProdForm()

	if request.method == 'POST':
		if request.POST.get('customization'):
			customer=request.user.customer
			#productid=request.POST.get('product')
			customization=request.POST.get('customization')

			filt = ProdForm(request.POST)
			if filt.is_valid():
				user = filt.save()
				product = filt.cleaned_data.get('product')

			

			#product = Product.objects.get(id=productid)
			post = Customization.objects.create(customer=customer, product=product, customization=customization)
			post.save()


	
	context = {'products':products, 'cartItems': cartItems, 'filt':filt}
	return render (request, 'accounts/products.html', context)



def cart(request):

	data = cartData(request)
	items = data['items']
	order = data['order']
	cartItems = data['cartItems']


	context = {'items':items, 'order':order}
	return render (request,'accounts/cart.html', context)

def checkout(request):
	data = cartData(request)
	items = data['items']
	order = data['order']
	cartItems = data['cartItems']


	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render (request,'accounts/checkout.html', context)

def dashboard(request):
	data = cartData(request)
	cartItems = data['cartItems']
	items = data['items']
	order = data['order']


	customerpk=request.user.customer.pk
	customer = Customer.objects.get(id=customerpk)
	customizations = Customization.objects.all()
	custcount = customizations.count()

	myFilter = CustomizationFilter(request.GET, queryset=customizations)
	customizations = myFilter.qs

	products = Product.objects.all()
	total_prod = products.count()

	orders = Order.objects.all()
	total_orders = orders.count()

	customers = Customer.objects.all()
	total_customer = customers.count()
	context = {'cartItems': cartItems, 'total_customer':total_customer, 
	'customizations':customizations, 'myFilter':myFilter, 'custcount':custcount, 
	'total_prod':total_prod, 'total_orders':total_orders}
	return render(request, 'accounts/dashboard.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('productId:', productId)

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


	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transacttion_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)


		if order.shipping == True:
			ShippingAddress.objects.create(
				customer = customer,
				order = order,
				address = data['shipping']['address'],
				city = data['shipping']['city'],
				state = data['shipping']['state'],
				zipcode = data['shipping']['zipcode'],
			)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transacttion_id = transacttion_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
			customer = customer,
			order = order,
			address = data['shipping']['address'],
			city = data['shipping']['city'],
			state = data['shipping']['state'],
			zipcode = data['shipping']['zipcode'],
		)

	return JsonResponse('Payment complete!', safe=False)