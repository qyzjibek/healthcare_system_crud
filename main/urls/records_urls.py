from django.urls import path
from ..views import records_list, record_create, record_update, record_delete

urlpatterns = [
    path('', records_list, name='record_list'),
    path('new/', record_create, name='record_create'),
    path('<int:record_pkey>/edit/', record_update, name='record_update'),
    path('<int:record_pkey>/delete/', record_delete, name='record_delete'),
]
