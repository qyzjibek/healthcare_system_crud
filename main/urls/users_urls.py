from django.urls import path
from ..views import user_list, user_form, user_delete
urlpatterns = [
    path('', user_list, name='user_list'),
    path('new/', user_form, name='user_form'),  # Create new user
    path('<str:user_id>/edit/', user_form, name='user_form'),  # Edit existing user by email
    path('<str:user_id>/delete/', user_delete, name='user_delete'),  # Delete user
]
