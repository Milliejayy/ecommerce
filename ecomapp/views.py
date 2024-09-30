# from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,User,UserProfile
from . forms import UserForm
from django.contrib import messages
from .models import Cart, CartItem


# Create your views here.
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def shop(request):
   latest_product_uploaded = Product.objects.all()
   context = {"latest_product_uploaded": latest_product_uploaded}
    
   return render(request,"shop.html", context)

def signup(request):
    return render(request, "signup.html")

# def cart(request):
#     return render(request, "cart.html")

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'cart': cart})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product,price = product.price)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_view')

def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    cart_item.delete()
    
    return redirect('cart_view')

def update_cart_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    
    if 'quantity' in request.POST:
        quantity = int(request.POST['quantity'])
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart_view')

def login(request):
    return render(request, "login.html")

def detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "detail.html", {"product": product})

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserForm  # Your form class

def userForm(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        
        if form.is_valid():
            user = User.objects.create(
                email = form.cleaned_data['email'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                username = form.cleaned_data['username'],


                
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user = user,phone = form.cleaned_data['phone'])
            return redirect("home")
        else:
            return render(request, 'signup.html', {'form': form})
            
    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})



def cart_view(request):
    cart = request.session.get('cart', {})
    
    cart_items = []
    subtotal = 0

    # Calculate total for each item and the cart's subtotal
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.price * quantity
        subtotal += total_price

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })
    
    total = subtotal  # Add tax/shipping calculation if needed
    
    # Pass the cart details to the template
    context = {
        'cart': {
            'items': cart_items,
            'subtotal': subtotal,
            'total': total,
        }
    }
    
    return render(request, 'cart.html', context)



from django.views.decorators.http import require_POST

@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Update the cart in session
    cart = request.session.get('cart', {})
    
    if quantity > 0:
        cart[product_id] = quantity  # Set the new quantity for the product
    else:
        del cart[product_id]  # Remove the product if quantity is 0

    request.session['cart'] = cart  # Save updated cart in session

    return redirect('cart_view')
