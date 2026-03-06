from django.urls import path
from . import views


urlpatterns=[
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    path('categorylist/', views.CategoryListCreateAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),     
    path('user-orders/', views.UserOrderListAPIView.as_view()),
    path('users/', views.UserListAPIView.as_view()),     
    path('signup/', views.CreateUserAPIView.as_view())      
]


