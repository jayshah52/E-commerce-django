
# Create your views here.
import json
import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *


def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0,'get_cart_items':0}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {"products":products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0}
		cartItems = order['get_cart_items']
	context = {"items":items,"order":order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0}
		cartItems = order['get_cart_items']
	context = {"items": items, "order": order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)


@csrf_exempt
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	# print("DATA", data)
	customer = request.user.customer
	product = Product.objects.get(id = productId)
	order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse("Hello World", safe=False)

@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
		total = float(data['userData']['total'])
		order.transaction_id = transaction_id
		if total == order.get_cart_total:
			order.is_complete = True
		order.save()

		ShippingAddress.objects.create(
			customer=customer,
			order = order,
			address=data['shipping']['address'],
			city = data['shipping']['city'],
			state = data['shipping']['state'],
			zipcode = data['shipping']['zipcode']

		)
	else:
		print("user not logged in ")
	print("DAYA", request.body)
	return JsonResponse("Payment Complete", safe=False)