from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_item, name='remove_item'),
    path('increment/<int:product_id>/', views.increment_item, name='increment_item'),
    path('decrement/<int:product_id>/', views.decrement_item, name='decrement_item'),
    path('clear/', views.clear_cart, name='clear_cart'),
     path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    
]
