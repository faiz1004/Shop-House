from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from .models import *
from django.contrib.auth.hashers import check_password ,make_password
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        product_id = request.POST.get('cartid')
        remove = request.POST.get('remove')
        
        cart_id = request.session.get('cart')
        
        if cart_id:
            quantity = cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                            cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity - 1
                else:
                    cart_id[product_id] = quantity + 1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] = 1
            
        
        request.session['cart'] = cart_id
        

    category_obj = Category.objects.all()
    cat_id = request.GET.get('category_id')

    if cat_id:
        product_obj = Product.objects.filter(Product_category=cat_id)
    else:
        product_obj = Product.objects.all()

    context={
        'category_obj': category_obj,
        'product_obj':product_obj
    }

    return render(request, 'home.html',context=context)



def contact(request):
    return render(request, 'contact.html')

def signup(request):
    if request.method == "POST":
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
       
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')        

        c_obj = Signup (
            first_name = f_name,
            last_name = l_name,
            email =email,
            password =make_password(password),
            mobile = mobile,
            gender  =gender,

        )
        c_obj.save()
        return redirect('home')
    

def login(request):
    if request.method == "POST":
        email_id = request.POST.get("emailid")
        password = request.POST.get("password")

        try:
            fetch_email = Signup.objects.get(email = email_id)
            if check_password(password,fetch_email.password):
                # return HttpResponse("Login successfull")
                request.session['name']= fetch_email.first_name
                request.session['customer_id']= fetch_email.id
                
                return redirect('home')
            else:
                error_message = "Wrong Password" 
        except:
            error_message = "User Does not Exist."
    return render(request, 'base.html', {'error_message': error_message})
        


def logout(request):
    request.session.clear()
    return redirect('home')

def cart_details(request):

    ids = list(request.session.get('cart').keys())
    
    cart_obj = Product.objects.filter(id__in=ids)
    return render(request,'cart.html',{'cart_obj':cart_obj})

def check_cart(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        customer_id = request.session.get('customer_id')
        messages.success(request,"order successfully created")
 
    
        if not customer_id:
            return HttpResponse("PLease Login........")
    
        cart = request.session.get('cart')
        product_details = Product.objects.filter(id__in=list(cart.keys()))

        for pro in product_details:
            order_details = Order(
                address = address,
                mobile = mobile,
                customer = Signup(id=customer_id),
                product = pro,
                price = pro.Product_price,
                quantity = cart.get(str(pro.id))
                
            )
            order_details.save()
        return redirect('cart')
        # messages.success(request,"order successfully created")    

        # return HttpResponse("order successfully created")


def order_details(request):

    customer_id = request.session.get('customer_id')
    fetch_order = Order.objects.filter(customer=customer_id)
    tp = 0
    for i in fetch_order:
        tp = tp + (i.price * i.quantity)

    context = {
        'fetch_order': fetch_order,
        'tp': tp
    }
    return render(request, 'order.html', context=context)

from rest_framework import routers, serializers, viewsets
from .serializations import SignUpSerializer
class UserViewSet(viewsets.ModelViewSet):
    queryset = Signup.objects.all()
    serializer_class = SignUpSerializer