from rest_framework import serializers
from productmanagement.models import Product, Category, Order, OrderItem, User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model= User
        fields=['username', 'first_name', 'last_name', 'email','phone_no', 'address', 'password']


class ProductSerializer(serializers.ModelSerializer):
    # category= serializers.CharField(source='category.name')
    class Meta:
        model= Product
        fields= [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category'
        ]

    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value
    

class CategorySerializer(serializers.ModelSerializer):
    products=ProductSerializer(
        many=True,
          read_only= True)
    print(products)
    class Meta:
        model=Category
        fields= [
            'id',
            'name',
            'description',
            'products'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product_name= serializers.CharField(source='product.name')
    product_price=serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price'
    )
    class Meta:
        model=OrderItem
        fields=[
            'id',
            'quantity',
            'product_name',
            'product_price'
        ]

class OrderSerializer(serializers.ModelSerializer):
    total_price=serializers.SerializerMethodField()
    items=OrderItemSerializer(many=True, read_only=True) 
    class Meta:
        model= Order
        fields=[
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price'
        ]
    def get_total_price(self, obj):
        order_items=obj.items.all()
        totalprice=sum(order_item.item_subtotal for order_item in order_items)
        return totalprice

class ProductInfoSerializer(serializers.Serializer):
    products= ProductSerializer(many=True)
    count= serializers.IntegerField()
    max_price=serializers.FloatField()
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
    def get_password(self, obj):
        pas=obj


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]