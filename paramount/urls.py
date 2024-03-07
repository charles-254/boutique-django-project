from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/',Dashboard.as_view(),name='dashboard'),
    path('login/',LoginView.as_view(), name='login'),
    path('products/',Products.as_view(), name='products'),
    path('sales/', SalesDataView.as_view(), name='sales' ),
    path('search/', Search_view, name='search')
]
