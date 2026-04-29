"""URL patterns per l'app Pharmacy."""
from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('search/', views.product_search, name='product-search'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
]
