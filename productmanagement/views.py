from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from productmanagement.models import Product, Category, Order,OrderItem, User
from productmanagement.serializers import ProductSerializer,CategorySerializer, OrderItemSerializer, OrderSerializer, ProductInfoSerializer, UserSerializer, CreateUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from productmanagement.filters import ProductFilter, InStockFilterBackend
from django_filters.rest_framework import DjangoFilterBackend


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend,
                        filters.SearchFilter,
                        filters.OrderingFilter,
                        InStockFilterBackend]
    
    search_fields = ['=name', 'description']
    ordering_fields= ['name', 'price', 'stock']


    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

# class ProductCreateAPIView(generics.CreateAPIView):
#     model=Product
#     serializer_class=ProductSerializer

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class UserListAPIView(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class CreateUserAPIView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=CreateUserSerializer

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_url_kwarg='product_id'
    
    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method in ['PUT','PATCH','DELETE']:
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()

class OrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product').all()
    serializer_class=OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product').all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(user=self.request.user)

class ProductInfoAPIView(APIView):
    def get(self, request):
        products=Product.objects.all()
        serializer=ProductInfoSerializer({
            'products':products,
            'count':len(products),
            'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
        return Response(serializer.data)
# @api_view(['GET'])
# def product_list(request):
#     products= Product.objects.all()
#     serializer= ProductSerializer(products, many=True)
#     return Response(serializer.data)
#     # return JsonResponse(
#     #     {
#     #     'data':serializer.data
#     #     }
#     # )

# @api_view(['GET'])
# def product_detail(request, pk):
#     product= get_object_or_404(Product, pk=pk)
#     serializer= ProductSerializer(product)
#     print(product)
#     print(serializer)
#     return Response(serializer.data)

# @api_view(['GET'])
# def category_list(request):
#     Categories= Category.objects.all()
#     serializer = CategorySerializer(Categories, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def order_list(request):
#     orders= Order.objects.prefetch_related('items__product').all()
#     serializer=OrderSerializer(orders, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def product_info(request):
#     products=Product.objects.all()
#     serializer=ProductInfoSerializer({
#         'products':products,
#         'count':len(products),
#         'max_price':products.aggregate(max_price=Max('price'))['max_price']
#     })

#     return Response(serializer.data)



