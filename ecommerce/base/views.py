from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
# Create your views here.
import json
import datetime
from .utils import cookieCart,cartData
from django.db.models import Q
from .forms import ProductForm

def store(request):
    products = Product.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html',context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html',context)

# @csrf_exempt
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('action:',action)
    print('Product:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quabtity = (orderItem.quabtity + 1)
    elif action == 'remove':
        orderItem.quabtity = (orderItem.quabtity - 1)
    orderItem.save()

    if orderItem.quabtity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    ordereditems = OrderItem.objects.all()
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        ordereditems.delete()
        if total == order.get_total_cart:
            order.complete = True
        order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )
    print('Data:', request.body)
    return JsonResponse('Payment Completed!', safe=False)



def admin_panel(request):
    context = {}
    return render(request,'store/index.html', context)


def admin_panel_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/admin_panel_list/')
    form = ProductForm()
    context ={'form':form}
    return render(request,'store/add_product.html', context)


def admin_panel_edit(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/admin_panel_list/')
    context = {'form':form}

    return render(request,'store/edit_product.html', context)


def admin_panel_list(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'store/list_products.html', context)


def admin_panel_delete(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('/admin_panel_list/')


def admin_panel_search(request):
    search_text = request.GET.get('search_text')
    products = Product.objects.filter(
        Q(name__icontains=search_text)|
        Q(category__name__icontains=search_text)
    )
    context = {'products':products}
    return render(request, 'store/list_products.html',context)


def admin_panel_search2(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    search_text = request.GET.get('search_text')
    products = Product.objects.filter(
        Q(name__icontains=search_text)|
        Q(category__name__icontains=search_text)
    )
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'products':products}
    return render(request, 'store/store.html',context)
