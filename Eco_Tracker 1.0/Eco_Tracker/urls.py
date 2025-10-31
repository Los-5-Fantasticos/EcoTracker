
from django.contrib import admin
from django.urls import path, include
from EcoTracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # /login, /logout, etc.
    path('accounts/', include('EcoTracker.urls')),           # /signup
    path('', views.home, name='home'),
]
