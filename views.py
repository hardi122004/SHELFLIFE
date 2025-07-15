from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import *
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import GroceryItem, Cart
from datetime import date, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def homepage(request):
    return render(request,'template/home.html')

def user_login(request):
    if request.method=='POST':
        phone=request.POST.get('uname')
        pwd=request.POST.get('pwd')
        print(phone)
        print(pwd)

        if not User.objects.filter(phone_number=phone).exists():
            msg='Invalid Username'
            Flage=True
            return render(request,'template/login.html',{'msg':msg,'Flage':Flage})
        
        user = authenticate(phone_number=phone, password=pwd)

        print(user)
        if user is not None:
            login(request,user)
            return redirect('grocery_dashboard')
        else:
            msg='Incorrect username or password'
            Flage=True
            return render(request,'template/home.html', {'msg': msg, 'Flage': Flage})
    return render(request,'template/login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('uname')  # This will be stored in 'name' field
        phone_number = request.POST.get('phone')
        email = request.POST.get('email')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')

        if User.objects.filter(phone_number=phone_number).exists():
            msg = "Phone number already registered!"
            Flage = True
            return render(request, 'template/signup.html', {'msg': msg, 'Flage': Flage})

        if pwd1 != pwd2:
            msg = "Password1 and Password2 don't match"
            Flage = True
            return render(request, 'template/signup.html', {'msg': msg, 'Flage': Flage})

        user = User.objects.create_user(
            phone_number=phone_number,
            name=name,
            email=email,
            password=pwd1
        )

        msg = "Account created successfully!"
        Flage = True
        return redirect('homepage')

    return render(request, 'template/signup.html')


def grocery_dashboard(request):
    items = GroceryItem.objects.all().order_by('expiry_date')
    today = date.today()
    return render(request, 'template/grocery_dashboard.html', {
        'items': items,
        'today': today
    })

def add_to_cart(request, item_id):
    item = get_object_or_404(GroceryItem, id=item_id)
    cart = request.session.get('cart', [])

    if item_id not in cart:
        cart.append(item_id)
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('grocery_dashboard')

def view_cart(request):
    cart = request.session.get('cart', [])
    items = GroceryItem.objects.filter(id__in=cart)
    return render(request, 'template/cart.html', {'items': items})

def order_placed(request):
    cart = request.session.get('cart', [])
    cart_items = GroceryItem.objects.filter(id__in=cart)
    total_price = sum(getattr(item, 'price', 0) for item in cart_items)

    email_to_send = None
    if request.method == 'POST':
        # Use provided email or fallback to user's email
        email_input = request.POST.get('email')
        if email_input:
            email_to_send = email_input
        elif request.user.is_authenticated and request.user.email:
            email_to_send = request.user.email

        if email_to_send:
            subject = "Your Grocery Order & Expiry Summary"
            message = render_to_string('template/email_order_summary.html', {
                'user': request.user if request.user.is_authenticated else None,
                'cart_items': cart_items,
                'total_price': total_price
            })

            try:
                send_mail(
                    subject,
                    '',
                    settings.DEFAULT_FROM_EMAIL,
                    [email_to_send],
                    html_message=message
                )
            except Exception as e:
                print(f"Error sending email: {e}")

        # Clear cart session
        request.session['cart'] = []

        return render(request, 'template/order_placed.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'email_sent_to': email_to_send
        })

    # In case user visits this page without POST
    return redirect('view_cart')

def dashboard(request):
    return render(request, 'template/dashboard.html') 
# Create your views here.
