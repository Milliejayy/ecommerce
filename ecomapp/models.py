from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', default='Ads_infringe.PNG')  # New field for image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    # first_name= models.CharField(max_length=50)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile",null = True)
    phone= models.IntegerField()
    
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","phone","username"]
    def __str__(self):
        return f'{self.firstname} {self.lastname}'

# cart model represents the entire shopping cart as a whole   
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0.00)

    def __str__(self):
        return self.user

# cart item tracks individual item added to the cart; quantity,color,etc
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def get_total_price(self):
        return self.quantity * self.price
    

class Order(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    customer= models.ForeignKey(User, on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)
    address= models.CharField(max_length=100)
    phone= models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now_add=True) 
    status= models.BooleanField(default=False) 
    def __str__(self):
        return self.customer

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=50)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
