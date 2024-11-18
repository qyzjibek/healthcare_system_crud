from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('countries/', include('main.urls.countries_urls')),  # Includes the countries URLs
    path('users/', include('main.urls.users_urls')),  # Add a separate path for users
    path('records/', include('main.urls.records_urls')),  # Add a separate path for records
    path('', views.home, name='home'),  # This handles the empty path (root URL)
]
