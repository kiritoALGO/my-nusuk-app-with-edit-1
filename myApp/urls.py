from django.urls import path
from .views import add_customer, homepage, edit_customer, get_customer_detail, delete_customer, create_card, create_tasreh, test, success_view

urlpatterns = [
    path('test/', test, name='test'),
    path('', homepage, name='homepage'),
    path('success/', success_view, name='success'),
    path('customer/add/', add_customer, name='add_customer'),
    path('customer/get/<int:pk>/', get_customer_detail, name='get_customer'),
    path('customer/edit/<int:pk>/', edit_customer, name='edit_customer'),
    path('customer/delete/<int:pk>/', delete_customer, name='delete_customer'),
    path('customer/create_card/<int:pk>/', create_card, name='card_customer'),
    path('customer/create_tasreh/<int:pk>/', create_tasreh, name='tasreh_customer'),
]
