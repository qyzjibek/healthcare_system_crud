from django.urls import path
from ..views import country_list, country_create, country_update, country_delete

urlpatterns = [
    path('', country_list, name='country_list'),
    path('new/', country_create, name='country_create'),
    path('<str:cname>/edit/', country_update, name='country_update'),
    path('<str:cname>/delete/', country_delete, name='country_delete'),
]
