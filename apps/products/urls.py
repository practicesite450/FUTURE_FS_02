from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('products1/', views.products1, name='products1'),
]
