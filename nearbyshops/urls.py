

from django.contrib import admin
from django.urls import path

from shops.views import Home, home

urlpatterns = [
    path("", Home.as_view(), name='home'),
    path("find_shops/", Home.as_view(), name='find_shops'),
    path("admin/", admin.site.urls),
]
