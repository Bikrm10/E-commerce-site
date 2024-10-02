from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views import View
from .models import Customer,Cart, OrderPlaced,Product
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
 def get(self, request):
  topwear = Product.objects.filter(category = "TW")
  bottomwear = Product.objects.filter(category = "BW")
  mobile = Product.objects.filter(category = "M")
  return render(request,"app/home.html",{"topwear":topwear,"bottomwear":bottomwear,
                                         "mobile":mobile,})

# def home(request):
#  return render(request, 'app/home.html')

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
@method_decorator(decorator=login_required,name='dispatch')
class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk = pk)
  item_already_in_cart = False
  item_already_in_cart = Cart.objects.filter(Q(product=product.id)&Q(user= request.user)).exists()

  return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})
 
# this is view is used add product to the cart and redirect the navigation
@login_required
def add_to_cart(request):
 user = request.user
 print(Cart.product)
 product_id = request.GET.get('prod_id')
 
 product  = Product.objects.get(id = product_id)
 Cart(user = user,product = product).save()
 return redirect('/cart')

# this functino is used to  render the car items 
@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  carts = Cart.objects.filter(user =user)
  amount = 0.0
  total_amount =0.0 
  shipping = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  # cart_size = (len(cart_product))
  if cart_product:
    for cart in cart_product:
      tempamount = cart.quantity * cart.product.discounted_price
      amount += tempamount
    total_amount = amount + shipping
    if amount == 0.0:
     shipping = 0.0
    return render(request, 'app/addtocart.html',{'carts':carts, 'total_amount':total_amount,'amount':amount,'shipping':shipping})
  else:
   return render(request,'app/emptycart.html')

# this is used to increment the item in the cart
@login_required
def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user ))
  print(c.quantity)
  c.quantity += 1
  c.save()
  amount = 0.0
  total_amount =0.0 
  shipping = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user  == request.user]
  for cart in cart_product:
    tempamount = cart.quantity * cart.product.discounted_price
    amount += tempamount
  total_amount = amount + shipping
  data  = {
     'quantity' :c.quantity,
     'amount':amount,
     'totalamount':total_amount
    }
  return JsonResponse(data)

# this is used to decrement the item in the cart list
@login_required
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user ))
  print(c.quantity)
  if c.quantity > 1 :
   c.quantity -= 1
   c.save()
  amount = 0.0
  total_amount =0.0 
  shipping = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user  == request.user]
  for cart in cart_product:
    tempamount = cart.quantity * cart.product.discounted_price
    amount += tempamount
  total_amount = amount + shipping
  data  = {
     'quantity' :c.quantity,
     'amount':amount,
     'totalamount':total_amount
    }
  return JsonResponse(data)
# this is used to remove item from the cart list
#
@login_required
def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user ))
  c.delete()
   
  
  amount = 0.0
  total_amount =0.0 
  shipping = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user  == request.user]
  for cart in cart_product:
    tempamount = cart.quantity * cart.product.discounted_price
    amount += tempamount
  total_amount = amount + shipping
  print(amount)
  data  = {
     'quantity' :c.quantity,
     'amount':amount,
     'totalamount':total_amount
    }
  return JsonResponse(data)
 
# this is used for buying the item 
@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def profile(request):
 return render(request, 'app/profile.html')

@login_required
def address(request):
 add = Customer.objects.filter(user = request.user)
 print(add)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 ordered_products = OrderPlaced.objects.filter(user = request.user)
 return render(request, 'app/orders.html',{'ordered_products':ordered_products})
@login_required
def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data =None):
 if data == None:
  mobiles = Product.objects.filter(category ="M")
  
 elif data == "Redmi" or data == "Samsung":
  mobiles = Product.objects.filter(category="M").filter(brand=data)
 elif data == "below":
  mobiles = Product.objects.filter(category="M").filter(discounted_price__lt = 10000)
 elif data == "above":
  mobiles = Product.objects.filter(category="M").filter(discounted_price__gt = 10000)

 return render(request,'app/mobile.html',{'mobiles':mobiles})

# class based  view for customer registration that use built in form for register
class CustomerRegistrationView(View):
 def get(self,request):
  form  = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html',{'form':form})
 def post(self,request):
  form  = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations ! Successfully Registered ')
   form.save()
  return render(request, 'app/customerregistration.html',{'form':form})
 
# placing order views
@login_required
def checkout(request):
 
 if request.user.is_authenticated:
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  amount =0.0
  shipping = 70.0
  totalamount = 0.0
  for cart in cart_product:
   amount += cart.quantity* cart.product.discounted_price
  totalamount += amount+shipping
  adresses = Customer.objects.filter(user = request.user)
   
   

 return render(request, 'app/checkout.html',
               {'carts':cart_product,'address':adresses,'total_amount':totalamount})
@login_required
def payment_done(request):
 user =  request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id = custid)
 cart = Cart.objects.filter(user = user)
 if cart:
  for c in cart:
   OrderPlaced(user = user , customer = customer,product = c.product,quantity = c.quantity).save()
   c.delete()
  return redirect('/orders')
@method_decorator( decorator=login_required,name='dispatch')
class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   zipcode = form.cleaned_data['zipcode']
   state = form.cleaned_data['state']
   reg = Customer(user = usr,name=name,locality = locality,city = city,zipcode = zipcode,state = state)
   messages.success(request,'Congratulations !! Profile Updated Successfully')
   reg.save()
   return redirect('/profile')

  #  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  
