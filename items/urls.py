from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.item_list, name='item_list'),
    # Add other URL patterns as needed
]
