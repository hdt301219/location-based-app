from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from shops.views import Home
from register.views import register
from login.views import login

urlpatterns = [
    path("admin/", admin.site.urls),
    path('jet/', include('jet.urls', 'jet')), 
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path("", login, name='login'),  # Mapping root URL to login view
    path("home/", Home.as_view(), name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login_redirect'),
    path('shops/', include('shops.urls')), 
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
