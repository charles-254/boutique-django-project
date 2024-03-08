from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(),name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', Products.as_view(), name='products'),
    path('sales/', SalesDataView.as_view(), name='sales'),
    path('search/', Search_view, name='search'),
    path('your-profile/', YourProfile.as_view(), name='your-profile'),
    path('edit-details/<int:pk>', EditPersonalDetails.as_view(), name='edit-details'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)