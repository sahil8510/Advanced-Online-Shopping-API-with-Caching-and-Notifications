from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
import uuid

# Create your models here.
class User(AbstractUser):
    phone_no = models.CharField(max_length = 20, blank= True)
    address= models.CharField(max_length= 100, blank=True)
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

    
class Product(models.Model):
    name= models.CharField(max_length=200)
    description= models.TextField()
    price= models.DecimalField(max_digits=10, decimal_places=2)
    stock= models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null= False, related_name="products")

    def __str__(self):
        return self.name
    
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING="pending"
        SHIPPED="shipped"
        DELIVERED="delivered"
        CANCELLED="cancelled"
        CONFIRMED='confirmed'
    order_id= models.UUIDField(primary_key= True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status= models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    products= models.ManyToManyField(Product, through="OrderItem", related_name="orders")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"order{self.order_id} by {self.user.username}"

class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField()


    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} X {self.product} in order{self.order.order_id}"






