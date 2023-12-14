# shops/urls.py
from django.urls import path
from . import views

app_name = 'shops'  # Only if you're using URL namespaces

urlpatterns = [
    # ... other URL patterns ...
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
]
